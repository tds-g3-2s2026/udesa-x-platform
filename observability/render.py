"""Render Grafana Cloud API payloads without connecting to Grafana."""

import argparse
import json
import re
from pathlib import Path

SOURCE = Path(__file__).resolve().parent


def substitute(value, replacements):
    """Replace deployment values while retaining Grafana's query variables."""
    if isinstance(value, str):
        for token, replacement in replacements.items():
            value = value.replace("${" + token + "}", replacement)
        return value
    if isinstance(value, list):
        return [substitute(item, replacements) for item in value]
    if isinstance(value, dict):
        return {key: substitute(item, replacements) for key, item in value.items()}
    return value


def render(metrics_uid, tempo_uid, loki_uid, folder_uid, contact_point):
    """Return dashboard, alert-rule and datasource-correlation API payloads."""
    for uid in (metrics_uid, tempo_uid, loki_uid, folder_uid):
        if not re.fullmatch(r"[A-Za-z0-9_-]{1,40}", uid):
            raise ValueError("Datasource and folder UIDs must contain 1–40 letters, digits, _ or -")
    if not contact_point.strip() or any(ord(char) < 32 for char in contact_point):
        raise ValueError("An existing contact point name is required")
    replacements = {
        "METRICS_UID": metrics_uid,
        "TEMPO_UID": tempo_uid,
        "LOKI_UID": loki_uid,
        "FOLDER_UID": folder_uid,
        "CONTACT_POINT": contact_point,
    }
    dashboard = substitute(json.loads((SOURCE / "dashboard.json").read_text()), replacements)
    alerts = substitute(json.loads((SOURCE / "alerts.yaml").read_text()), replacements)["rules"]
    correlation = substitute(json.loads((SOURCE / "correlation.json").read_text()), replacements)
    return {
        "dashboard": {"dashboard": dashboard, "folderUid": folder_uid, "overwrite": False},
        "alerts": alerts,
        "correlation": correlation,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--metrics-uid", required=True)
    parser.add_argument("--tempo-uid", required=True)
    parser.add_argument("--loki-uid", required=True)
    parser.add_argument("--folder-uid", required=True)
    parser.add_argument("--contact-point", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        payloads = render(
            args.metrics_uid, args.tempo_uid, args.loki_uid, args.folder_uid, args.contact_point
        )
        args.output.mkdir(parents=True, exist_ok=False)
    except (ValueError, FileExistsError) as error:
        parser.error(str(error))
    (args.output / "alerts").mkdir()
    for name in ("dashboard", "correlation"):
        (args.output / f"{name}.json").write_text(
            json.dumps(payloads[name], ensure_ascii=False, indent=2) + "\n"
        )
    for rule in payloads["alerts"]:
        (args.output / "alerts" / f"{rule['uid']}.json").write_text(
            json.dumps(rule, ensure_ascii=False, indent=2) + "\n"
        )
    print(args.output)


if __name__ == "__main__":
    main()
