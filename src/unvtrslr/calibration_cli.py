from __future__ import annotations

import argparse
import json
from pathlib import Path

from .calibration import FingerprintObservation, calibrate_feature_information


def _load(path: str) -> list[FingerprintObservation]:
    rows: list[FingerprintObservation] = []
    with Path(path).open("r", encoding="utf-8") as handle:
        for line_number, raw in enumerate(handle, 1):
            raw = raw.strip()
            if not raw:
                continue
            obj = json.loads(raw)
            try:
                rows.append(
                    FingerprintObservation(
                        observation_id=str(obj["observation_id"]),
                        system_id=str(obj["system_id"]),
                        source_id=str(obj["source_id"]),
                        content_id=None if obj.get("content_id") is None else str(obj["content_id"]),
                        family_id=None if obj.get("family_id") is None else str(obj["family_id"]),
                        fingerprint=obj["fingerprint"],
                    )
                )
            except KeyError as exc:
                raise ValueError(f"line {line_number}: missing field {exc.args[0]!r}") from exc
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Rank acoustic fingerprint dimensions by nuisance-conditioned information."
    )
    parser.add_argument(
        "observations",
        help="JSONL observations with metadata and an Acoustic Fingerprint V1 object",
    )
    parser.add_argument(
        "--nuisance",
        action="append",
        default=None,
        help="nuisance field; repeatable (default: source_id)",
    )
    parser.add_argument("--permutations", type=int, default=128)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()

    nuisances = tuple(args.nuisance) if args.nuisance else ("source_id",)
    report = calibrate_feature_information(
        _load(args.observations),
        nuisance_fields=nuisances,
        permutations=args.permutations,
        seed=args.seed,
    )
    print(json.dumps(report.to_dict(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
