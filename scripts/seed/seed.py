# /// script
# requires-python = ">=3.13"
# dependencies = ["asyncpg==0.30.0", "argon2-cffi==25.1.0"]
# ///
"""Generate deterministic, related load-test data in migrated PostgreSQL databases."""

import argparse
import asyncio
import hashlib
import json
import os
import random
import sys
import uuid
from collections import defaultdict
from contextlib import AsyncExitStack
from dataclasses import asdict, dataclass
from datetime import UTC, datetime, timedelta
from itertools import islice

import asyncpg
from argon2 import PasswordHasher
from content import (
    BIO,
    DISPLAY_NAME,
    SUBJECTS,
    TOPICS,
    generate_post_text,
    generate_reply_text,
)

START = datetime(2026, 1, 1, tzinfo=UTC)
PASSWORD = "CampusSeed42!"
TABLE_KEYS = {
    "users": "id",
    "user_profiles": "id",
    "follows": "follower_id, followee_id",
    "posts": "id",
    "likes": "user_id, post_id",
}


@dataclass(frozen=True)
class Volumes:
    users: int = 100
    follows: int = 5_000
    posts: int = 2_000
    replies: int = 2_000
    likes: int = 7_000

    def validate(self):
        """Reject impossible volumes before opening either database."""
        if any(value < 0 for value in asdict(self).values()):
            raise ValueError("Los volúmenes no pueden ser negativos.")
        if self.users > 10**10:
            raise ValueError("El volumen de usuarios excede el formato de los handles.")
        if self.follows > self.users * (self.users - 1):
            raise ValueError("No hay suficientes pares de usuarios para esos seguimientos.")
        if self.posts and not self.users:
            raise ValueError("Los posts requieren usuarios.")
        if self.replies and not self.posts:
            raise ValueError("Las respuestas requieren posts originales.")
        if self.likes > self.users * (self.posts + self.replies):
            raise ValueError("No hay suficientes pares usuario/publicación para esos likes.")


def unique_pairs(count, left, right, rng, choose, initial=()):
    """Yield unique pairs with bounded rejection, including dense datasets."""
    seen = set()
    for a, b in initial:
        if len(seen) == count:
            return
        seen.add(a * right + b)
        yield a, b
    for _ in range(count * 10):
        if len(seen) == count:
            return
        a, b = choose()
        key = a * right + b
        if key not in seen:
            seen.add(key)
            yield a, b
    offset = rng.randrange(left * right) if left * right else 0
    for i in range(left * right):
        if len(seen) == count:
            return
        key = (i + offset) % (left * right)
        if key not in seen:
            seen.add(key)
            yield divmod(key, right)


def post_id(seed, index, at):
    """Keep deterministic UUIDv7 identifiers ordered by publication time."""
    milliseconds = int(at.timestamp() * 1000)
    tail = int.from_bytes(hashlib.sha256(f"{seed}:post:{index}".encode()).digest()[:10])
    return uuid.UUID(
        int=(milliseconds << 80)
        | (7 << 76)
        | (((tail >> 62) & 0xFFF) << 64)
        | (2 << 62)
        | (tail & ((1 << 62) - 1))
    )


def generate_users(users, password_hash):
    for i, user in enumerate(users):
        yield dict(
            id=user,
            email=f"seed{i:010d}@example.com",
            handle=f"@seed{i:010d}",
            password_hash=password_hash,
            must_change_password=False,
            is_email_verified=True,
            terms_accepted=True,
            terms_accepted_at=START,
            display_name=DISPLAY_NAME.format(number=i + 1),
            bio=BIO.format(topic=TOPICS[i % len(TOPICS)][0]),
            created_at=START,
        )


def generate_profiles(users):
    for i, user in enumerate(users):
        yield dict(id=user, handle=f"@seed{i:010d}")


def generate_follows(users, count, seed, followers):
    """Record follower indices for subsequent interactions as rows are consumed."""
    rng = random.Random(f"{seed}:follows")

    def choose_pair():
        follower = int(rng.random() ** 2 * len(users))
        followee = int(rng.random() ** 2 * (len(users) - 1))
        if followee >= follower:
            followee += 1
        return follower, (followee - follower - 1) % len(users)

    backbone = ((i, 0) for i in range(len(users)))
    for follower, offset in unique_pairs(
        count,
        len(users),
        max(0, len(users) - 1),
        rng,
        choose_pair,
        backbone if len(users) > 1 else (),
    ):
        followee = (follower + offset + 1) % len(users)
        followers[followee].append(follower)
        yield dict(
            follower_id=users[follower],
            followee_id=users[followee],
            created_at=START + timedelta(seconds=rng.randrange(86400)),
        )


def generate_posts(users, count, seed, publications, topics):
    """Record publication references and topics for subsequent replies and likes."""
    rng = random.Random(f"{seed}:posts")
    for i in range(count):
        author = i if i < len(users) else int(rng.random() ** 2 * len(users))
        topic = rng.randrange(len(TOPICS))
        subject = rng.choice(SUBJECTS[topic])
        content = generate_post_text(rng, topic, subject, i)
        at = START + timedelta(days=1, seconds=rng.randrange(60 * 86400))
        identifier = post_id(seed, i, at)
        topics.append((topic, subject))
        publications.append((identifier, author, at))
        yield dict(
            id=identifier,
            author_id=users[author],
            parent_id=None,
            content=content,
            created_at=at,
        )


def choose_participant(author, followers, user_count, rng):
    candidates = followers[author]
    if candidates and rng.random() < 0.8:
        return rng.choice(candidates)
    return rng.randrange(user_count)


def generate_replies(users, count, seed, followers, publications, topics):
    """Append reply references after the originals so likes can target either."""
    rng = random.Random(f"{seed}:replies")
    original_count = len(publications)
    for i in range(count):
        parent = int(rng.random() ** 2 * original_count)
        parent_id, parent_author, parent_at = publications[parent]
        author = choose_participant(parent_author, followers, len(users), rng)
        topic, subject = topics[parent]
        content = generate_reply_text(rng, topic, subject)
        at = parent_at + timedelta(seconds=1 + rng.randrange(7 * 86400))
        identifier = post_id(seed, original_count + i, at)
        publications.append((identifier, author, at))
        yield dict(
            id=identifier,
            author_id=users[author],
            parent_id=parent_id,
            content=content,
            created_at=at,
        )


def generate_reactions(users, count, seed, followers, publications, kind):
    rng = random.Random(f"{seed}:{kind}")

    def choose_pair():
        post = int(rng.random() ** 2 * len(publications))
        author = publications[post][1]
        return choose_participant(author, followers, len(users), rng), post

    for user, post in unique_pairs(count, len(users), len(publications), rng, choose_pair):
        identifier, _, at = publications[post]
        yield dict(
            user_id=users[user],
            post_id=identifier,
            created_at=at + timedelta(seconds=1 + rng.randrange(7 * 86400)),
        )


def generate_data(volumes, seed, password_hash):
    """Consume each table fully before advancing to its dependents."""
    volumes.validate()
    users = [
        uuid.uuid5(uuid.NAMESPACE_URL, f"campus-seed:{seed}:user:{i}") for i in range(volumes.users)
    ]
    followers = defaultdict(list)
    publications = []
    topics = []

    yield "users", generate_users(users, password_hash)
    yield "user_profiles", generate_profiles(users)
    yield "follows", generate_follows(users, volumes.follows, seed, followers)
    yield "posts", generate_posts(users, volumes.posts, seed, publications, topics)
    yield "posts", generate_replies(users, volumes.replies, seed, followers, publications, topics)
    yield "likes", generate_reactions(users, volumes.likes, seed, followers, publications, "likes")


async def prepare(connection, tables):
    """Lock existing tables and refuse nonempty or unmigrated databases."""
    if not await connection.fetchval("SELECT to_regclass('alembic_version')"):
        raise ValueError("Aplicá las migraciones antes de ejecutar el seed.")
    if not await connection.fetchval("SELECT count(*) FROM alembic_version"):
        raise ValueError("La base no tiene una revisión de Alembic aplicada.")
    for table in tables:
        await connection.execute(f'LOCK TABLE "{table}" IN EXCLUSIVE MODE')
        if await connection.fetchval(f'SELECT EXISTS (SELECT 1 FROM "{table}" LIMIT 1)'):
            raise ValueError(f"La tabla {table} no está vacía; el seed no borra datos.")


async def update_counters(connection):
    for target, counter, source, foreign_key in (
        ("user_profiles", "followers_count", "follows", "followee_id"),
        ("user_profiles", "following_count", "follows", "follower_id"),
        ("posts", "likes_count", "likes", "post_id"),
        ("posts", "replies_count", "posts", "parent_id"),
    ):
        await connection.execute(f"""
            UPDATE {target} p SET {counter} = c.total
            FROM (SELECT {foreign_key} AS id, count(*) AS total FROM {source}
                  WHERE {foreign_key} IS NOT NULL GROUP BY {foreign_key}) c
            WHERE p.id = c.id
        """)


async def report(users, posts, volumes):
    counts = {}
    digest = hashlib.sha256()
    for table, order in TABLE_KEYS.items():
        connection = users if table == "users" else posts
        counts[table] = await connection.fetchval(f'SELECT count(*) FROM "{table}"')
        rows = await connection.fetch(f'SELECT * FROM "{table}" ORDER BY {order} LIMIT 100')
        digest.update(table.encode())
        digest.update(json.dumps([dict(row) for row in rows], default=str, sort_keys=True).encode())
    counts["originals"] = await posts.fetchval("SELECT count(*) FROM posts WHERE parent_id IS NULL")
    counts["replies"] = counts["posts"] - counts["originals"]
    counts["interactions"] = counts["likes"] + counts["replies"]
    expected = dict(asdict(volumes), user_profiles=volumes.users, originals=volumes.posts)
    expected["posts"] += volumes.replies
    expected["interactions"] = volumes.likes + volumes.replies
    if counts != expected:
        raise ValueError(f"Conteos inesperados: {counts}")
    return {"counts": counts, "sample_sha256": digest.hexdigest()}


async def insert_batches(connection, table, records, batch_size):
    while batch := list(islice(records, batch_size)):
        columns = tuple(batch[0])
        await connection.copy_records_to_table(
            table,
            columns=columns,
            records=[tuple(row[column] for column in columns) for row in batch],
        )


async def seed_databases(volumes, seed, batch_size, users_url, posts_url):
    volumes.validate()
    if batch_size < 1:
        raise ValueError("El tamaño de lote debe ser positivo.")
    if not users_url or not posts_url:
        raise ValueError("Definí SEED_USERS_DATABASE_URL y SEED_POSTS_DATABASE_URL.")
    password_hash = PasswordHasher().hash(
        PASSWORD, salt=hashlib.sha256(f"campus-seed:{seed}:password".encode()).digest()[:16]
    )
    async with AsyncExitStack() as connections:
        users = await asyncpg.connect(users_url)
        connections.push_async_callback(users.close)
        posts = await asyncpg.connect(posts_url)
        connections.push_async_callback(posts.close)

        async with users.transaction(), posts.transaction():
            await prepare(users, ("users",))
            await prepare(posts, ("user_profiles", "follows", "posts", "likes"))
            for table, records in generate_data(volumes, seed, password_hash):
                connection = users if table == "users" else posts
                await insert_batches(connection, table, records, batch_size)
            await update_counters(posts)
            result = await report(users, posts, volumes)

        await users.execute("ANALYZE users")
        for table in ("user_profiles", "follows", "posts", "likes"):
            await posts.execute(f'ANALYZE "{table}"')

    return {"seed": seed, "volumes": asdict(volumes), **result}


def parse_arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    for name, default in asdict(Volumes()).items():
        parser.add_argument(f"--{name}", type=int, default=default)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--batch-size", type=int, default=5000)
    return parser.parse_args()


def main():
    args = parse_arguments()
    volumes = Volumes(
        users=args.users,
        follows=args.follows,
        posts=args.posts,
        replies=args.replies,
        likes=args.likes,
    )
    try:
        result = asyncio.run(
            seed_databases(
                volumes,
                args.seed,
                args.batch_size,
                os.getenv("SEED_USERS_DATABASE_URL"),
                os.getenv("SEED_POSTS_DATABASE_URL"),
            )
        )
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    except (asyncpg.PostgresError, OSError) as exc:
        print(
            f"No se pudo completar el seed ({type(exc).__name__}). "
            "Revisá las conexiones y las migraciones.",
            file=sys.stderr,
        )
        return 1
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
