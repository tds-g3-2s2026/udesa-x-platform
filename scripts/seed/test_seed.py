"""Determinism and relational invariants, with optional migrated PostgreSQL databases."""

import asyncio
import json
import os
import unittest
from collections import Counter
from dataclasses import replace
from datetime import timedelta
from unittest.mock import patch

import asyncpg
from argon2 import PasswordHasher
from content import SUBJECTS
from seed import PASSWORD, START, Volumes, generate_data, seed_databases

SMALL = Volumes(users=12, follows=40, posts=30, replies=25, likes=100, retweets=20, deleted_posts=3)


def collect(volumes=SMALL, seed=42):
    tables = {}
    for table, records in generate_data(volumes, seed, "test-hash"):
        tables.setdefault(table, []).extend(records)
    return tables


class GenerationTests(unittest.TestCase):
    def test_same_seed_produces_identical_ids_dates_content_and_relationships(self):
        self.assertEqual(collect(), collect())
        self.assertNotEqual(collect(), collect(seed=43))

    def test_every_reference_resolves_and_events_follow_their_targets(self):
        tables = collect()
        users = {u["id"] for u in tables["users"]}
        self.assertEqual(users, {p["id"] for p in tables["user_profiles"]})
        posts = {p["id"]: p for p in tables["posts"]}
        for follow in tables["follows"]:
            self.assertIn(follow["follower_id"], users)
            self.assertIn(follow["followee_id"], users)
            self.assertNotEqual(follow["follower_id"], follow["followee_id"])
        for post in posts.values():
            self.assertIn(post["author_id"], users)
            self.assertGreater(post["created_at"], START + timedelta(hours=23))
            self.assertEqual(post["id"].version, 7)
            self.assertLessEqual(len(post["content"]), 280)
            if post["parent_id"]:
                parent = posts[post["parent_id"]]
                self.assertIsNone(parent["parent_id"])
                self.assertGreater(post["created_at"], parent["created_at"])
        for table in ("likes", "retweets"):
            for reaction in tables[table]:
                self.assertIn(reaction["user_id"], users)
                target = posts[reaction["post_id"]]
                self.assertGreater(reaction["created_at"], target["created_at"])
                self.assertIsNone(target["deleted_at"])

    def test_requested_counts_exclude_replies_from_originals(self):
        tables = collect()
        self.assertEqual(len(tables["users"]), SMALL.users)
        self.assertEqual(len(tables["follows"]), SMALL.follows)
        self.assertEqual(len(tables["likes"]), SMALL.likes)
        self.assertEqual(len(tables["retweets"]), SMALL.retweets)
        self.assertEqual(
            sum(p["deleted_at"] is not None for p in tables["posts"]), SMALL.deleted_posts
        )
        self.assertEqual(sum(p["parent_id"] is None for p in tables["posts"]), SMALL.posts)
        self.assertEqual(sum(p["parent_id"] is not None for p in tables["posts"]), SMALL.replies)
        for table, keys in (
            ("follows", ("follower_id", "followee_id")),
            ("likes", ("user_id", "post_id")),
            ("retweets", ("user_id", "post_id")),
        ):
            pairs = [tuple(row[key] for key in keys) for row in tables[table]]
            self.assertEqual(len(pairs), len(set(pairs)))

    def test_backbone_gives_every_user_a_follow_and_an_original(self):
        tables = collect()
        users = {u["id"] for u in tables["users"]}
        self.assertEqual(users, {f["follower_id"] for f in tables["follows"]})
        self.assertEqual(users, {p["author_id"] for p in tables["posts"] if not p["parent_id"]})

    def test_replies_match_the_parent_topic(self):
        tables = collect()
        posts = {p["id"]: p for p in tables["posts"]}
        for post in posts.values():
            if post["parent_id"]:
                parent = posts[post["parent_id"]]
                matches = [
                    subject
                    for subjects in SUBJECTS
                    for subject in subjects
                    if subject in parent["content"]
                ]
                self.assertTrue(matches)
                self.assertTrue(any(subject in post["content"] for subject in matches))

    def test_zero_single_user_and_saturated_relationships_terminate_with_exact_counts(self):
        for volumes in (
            Volumes(0, 0, 0, 0, 0, 0, 0),
            Volumes(1, 0, 1, 1, 2, 2, 0),
            Volumes(4, 12, 3, 2, 20, 20, 0),
        ):
            with self.subTest(volumes=volumes):
                tables = collect(volumes)
                self.assertEqual(len(tables["follows"]), volumes.follows)
                self.assertEqual(len(tables["likes"]), volumes.likes)
                self.assertEqual(len(tables["retweets"]), volumes.retweets)
                self.assertEqual(
                    len({(f["follower_id"], f["followee_id"]) for f in tables["follows"]}),
                    volumes.follows,
                )
                self.assertEqual(
                    len({(x["user_id"], x["post_id"]) for x in tables["likes"]}), volumes.likes
                )

    def test_impossible_volumes_are_rejected(self):
        for volumes in (
            replace(SMALL, users=-1),
            replace(SMALL, follows=145),
            replace(SMALL, deleted_posts=31),
            replace(SMALL, likes=625),
            replace(SMALL, retweets=625),
            Volumes(0, 0, 1, 0, 0, 0, 0),
            Volumes(1, 0, 0, 1, 0, 0, 0),
            Volumes(1, 0, 1, 0, 2, 0, 0),
        ):
            with self.subTest(volumes=volumes), self.assertRaises(ValueError):
                collect(volumes)

    def test_adding_likes_does_not_change_users_follows_or_publications(self):
        before = collect()
        after = collect(replace(SMALL, likes=110))
        for table in ("users", "user_profiles", "follows", "posts", "retweets"):
            self.assertEqual(before[table], after[table])

    def test_interactions_prefer_followed_authors_and_activity_is_uneven(self):
        tables = collect(Volumes(100, 1000, 500, 500, 2000, 200, 25))
        follows = {(f["follower_id"], f["followee_id"]) for f in tables["follows"]}
        posts = {p["id"]: p for p in tables["posts"]}
        social = sum(
            (like["user_id"], posts[like["post_id"]]["author_id"]) in follows
            for like in tables["likes"]
        )
        self.assertGreater(social / len(tables["likes"]), 0.6)
        popularity = Counter(f["followee_id"] for f in tables["follows"])
        self.assertGreater(max(popularity.values()), min(popularity.values()) * 2)

    def test_deleted_originals_retain_content_and_replies_before_deletion(self):
        tables = collect(Volumes(2, 2, 1, 2, 4, 4, 1))
        original = tables["posts"][0]
        self.assertTrue(original["content"])
        self.assertIsNone(original["parent_id"])
        self.assertGreater(original["deleted_at"], original["created_at"])
        for reply in tables["posts"][1:]:
            self.assertEqual(reply["parent_id"], original["id"])
            self.assertLess(reply["created_at"], original["deleted_at"])
            self.assertIsNone(reply["deleted_at"])
        for table in ("likes", "retweets"):
            self.assertEqual(len(tables[table]), 4)
            self.assertNotIn(original["id"], {row["post_id"] for row in tables[table]})

    def test_zero_reactions_allow_all_originals_to_be_deleted(self):
        tables = collect(Volumes(2, 2, 2, 0, 0, 0, 2))
        self.assertTrue(all(post["deleted_at"] for post in tables["posts"]))
        self.assertEqual(tables["likes"], [])
        self.assertEqual(tables["retweets"], [])

    def test_retweet_volume_does_not_change_other_entities(self):
        before = collect()
        after = collect(replace(SMALL, retweets=30))
        for table in ("users", "user_profiles", "follows", "posts", "likes"):
            self.assertEqual(before[table], after[table])

    def test_invalid_settings_do_not_open_connections(self):
        with patch("seed.asyncpg.connect") as connect:
            with self.assertRaises(ValueError):
                asyncio.run(seed_databases(SMALL, 42, 0, "users", "posts"))
            with self.assertRaises(ValueError):
                asyncio.run(seed_databases(SMALL, 42, 5, None, None))
            connect.assert_not_called()


@unittest.skipUnless(
    os.getenv("TEST_SEED_USERS_DATABASE_URL") and os.getenv("TEST_SEED_POSTS_DATABASE_URL"),
    "Requiere dos bases locales descartables migradas a head",
)
class DatabaseTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.users_url = os.environ["TEST_SEED_USERS_DATABASE_URL"]
        self.posts_url = os.environ["TEST_SEED_POSTS_DATABASE_URL"]
        self.users = await asyncpg.connect(self.users_url)
        self.posts = await asyncpg.connect(self.posts_url)
        await self.clear()

    async def clear(self):
        await self.posts.execute("TRUNCATE user_profiles CASCADE")
        await self.users.execute("TRUNCATE users CASCADE")

    async def asyncTearDown(self):
        await self.clear()
        await self.users.close()
        await self.posts.close()

    async def seed(self, batch_size=7, seed=42):
        return await seed_databases(SMALL, seed, batch_size, self.users_url, self.posts_url)

    async def snapshot(self):
        result = {}
        for connection, table, order in (
            (self.users, "users", "id"),
            (self.posts, "user_profiles", "id"),
            (self.posts, "posts", "id"),
            (self.posts, "follows", "follower_id, followee_id"),
            (self.posts, "likes", "user_id, post_id"),
            (self.posts, "retweets", "user_id, post_id"),
        ):
            result[table] = [
                dict(row)
                for row in await connection.fetch(f'SELECT * FROM "{table}" ORDER BY {order}')
            ]
        return json.dumps(result, default=str, sort_keys=True)

    async def test_database_contents_and_report_are_reproducible_across_batch_sizes(self):
        first = await self.seed()
        snapshot = await self.snapshot()
        await self.clear()
        second = await self.seed(batch_size=23)
        self.assertEqual(first, second)
        self.assertEqual(snapshot, await self.snapshot())
        self.assertEqual(first["counts"]["posts"], SMALL.posts + SMALL.replies)
        self.assertEqual(
            first["counts"]["interactions"], SMALL.likes + SMALL.replies + SMALL.retweets
        )
        self.assertEqual(first["counts"]["retweets"], SMALL.retweets)
        self.assertEqual(first["counts"]["deleted_posts"], SMALL.deleted_posts)
        await self.clear()
        third = await self.seed(seed=43)
        self.assertNotEqual(first["sample_sha256"], third["sample_sha256"])

    async def test_counters_match_actual_relationships_and_passwords_verify(self):
        await self.seed()
        for sql in (
            "SELECT count(*) FROM user_profiles p WHERE followers_count <> "
            "(SELECT count(*) FROM follows f WHERE f.followee_id=p.id) OR following_count <> "
            "(SELECT count(*) FROM follows f WHERE f.follower_id=p.id)",
            "SELECT count(*) FROM posts p WHERE likes_count <> "
            "(SELECT count(*) FROM likes l WHERE l.post_id=p.id) OR replies_count <> "
            "(SELECT count(*) FROM posts r WHERE r.parent_id=p.id)",
            "SELECT count(*) FROM posts p WHERE retweets_count <> "
            "(SELECT count(*) FROM retweets r WHERE r.post_id=p.id)",
            "SELECT count(*) FROM retweets r JOIN posts p ON p.id=r.post_id "
            "WHERE r.created_at <= p.created_at OR p.deleted_at IS NOT NULL",
            "SELECT count(*) FROM likes l JOIN posts p ON p.id=l.post_id "
            "WHERE l.created_at <= p.created_at OR p.deleted_at IS NOT NULL",
        ):
            self.assertEqual(await self.posts.fetchval(sql), 0)
        password_hash = await self.users.fetchval("SELECT password_hash FROM users LIMIT 1")
        self.assertTrue(PasswordHasher().verify(password_hash, PASSWORD))
        self.assertEqual(
            await self.users.fetchval(
                "SELECT count(*) FROM users WHERE NOT is_email_verified OR must_change_password "
                "OR NOT terms_accepted OR status <> 'active'"
            ),
            0,
        )

    async def test_deleted_originals_keep_replies_and_have_no_reactions(self):
        await seed_databases(Volumes(2, 2, 1, 2, 4, 4, 1), 42, 1, self.users_url, self.posts_url)
        original = await self.posts.fetchrow("SELECT * FROM posts WHERE parent_id IS NULL")
        self.assertTrue(original["content"])
        self.assertGreater(original["deleted_at"], original["created_at"])
        self.assertEqual(original["likes_count"], 0)
        self.assertEqual(original["retweets_count"], 0)
        self.assertEqual(original["replies_count"], 2)
        self.assertEqual(
            await self.posts.fetchval(
                "SELECT count(*) FROM posts WHERE parent_id=$1 AND created_at < $2",
                original["id"],
                original["deleted_at"],
            ),
            2,
        )
        for table in ("likes", "retweets"):
            self.assertEqual(
                await self.posts.fetchval(
                    f"SELECT count(*) FROM {table} WHERE post_id=$1", original["id"]
                ),
                0,
            )

    async def test_nonempty_database_is_rejected_without_changing_existing_data(self):
        await self.seed()
        before = await self.snapshot()
        with self.assertRaises(ValueError):
            await self.seed()
        self.assertEqual(before, await self.snapshot())
        await self.users.execute("TRUNCATE users CASCADE")
        with self.assertRaises(ValueError):
            await self.seed()
        self.assertEqual(await self.users.fetchval("SELECT count(*) FROM users"), 0)

    async def test_insert_failure_rolls_back_both_databases(self):
        with (
            patch("seed.update_counters", side_effect=ValueError("forced failure")),
            self.assertRaises(ValueError),
        ):
            await self.seed()
        self.assertEqual(await self.users.fetchval("SELECT count(*) FROM users"), 0)
        self.assertEqual(await self.posts.fetchval("SELECT count(*) FROM posts"), 0)


if __name__ == "__main__":
    unittest.main()
