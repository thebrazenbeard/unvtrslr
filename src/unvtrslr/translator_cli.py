from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from .cli import _read_wav
from .translator import (
    AcousticContextEpisode,
    fit_reference_translator,
    prepare_audio_evidence,
    reference_translator_model_from_dict,
    translate_source_evidence,
)
from .unit_registry import LocalUnitEvidence


def _row(obj: dict) -> LocalUnitEvidence:
    return LocalUnitEvidence(
        recording_id=str(obj["recording_id"]),
        source_id=str(obj["source_id"]),
        local_unit_id=str(obj["local_unit_id"]),
        vector=tuple(float(value) for value in obj["vector"]),
    )


def _load_evidence(path: str) -> list[LocalUnitEvidence]:
    rows: list[LocalUnitEvidence] = []
    with Path(path).open("r", encoding="utf-8") as handle:
        for line_number, raw in enumerate(handle, 1):
            raw = raw.strip()
            if not raw:
                continue
            try:
                rows.append(_row(json.loads(raw)))
            except KeyError as exc:
                raise ValueError(
                    f"line {line_number}: missing field {exc.args[0]!r}"
                ) from exc
    return rows


def _load_episodes(path: str) -> list[AcousticContextEpisode]:
    episodes: list[AcousticContextEpisode] = []
    with Path(path).open("r", encoding="utf-8") as handle:
        for line_number, raw in enumerate(handle, 1):
            raw = raw.strip()
            if not raw:
                continue
            obj = json.loads(raw)
            try:
                evidence = [_row(row) for row in obj["evidence"]]
                episodes.append(
                    AcousticContextEpisode.build(
                        obj["episode_id"],
                        obj["source_id"],
                        obj["context"],
                        evidence,
                    )
                )
            except KeyError as exc:
                raise ValueError(
                    f"line {line_number}: missing field {exc.args[0]!r}"
                ) from exc
    return episodes


def _load_model(path: str):
    obj = json.loads(Path(path).read_text(encoding="utf-8"))
    if "model" in obj:
        obj = obj["model"]
    return reference_translator_model_from_dict(obj)


def _load_renderer(path: str | None) -> dict[str, str] | None:
    if path is None:
        return None
    obj = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(obj, dict) or not all(
        isinstance(key, str) and isinstance(value, str)
        for key, value in obj.items()
    ):
        raise ValueError("renderer must be a JSON object mapping relation IDs to strings")
    return obj


def main() -> None:
    parser = argparse.ArgumentParser(
        description="UNVTRSLR reference translator fit/prepare/translate CLI."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    prepare = subparsers.add_parser(
        "prepare-wav",
        help="convert one PCM WAV into recording-local acoustic evidence",
    )
    prepare.add_argument("wav")
    prepare.add_argument("--recording-id", required=True)
    prepare.add_argument("--source-id", required=True)
    prepare.add_argument("--novelty-threshold", type=float, default=1.15)
    prepare.add_argument("--min-event-s", type=float, default=0.12)
    prepare.add_argument("--event-cluster-distance", type=float, default=1.35)

    fit = subparsers.add_parser(
        "fit",
        help="fit a frozen reference translator from JSONL acoustic/context episodes",
    )
    fit.add_argument("episodes")
    fit.add_argument("--semantic-min-sources", type=int, default=2)
    fit.add_argument("--min-sources", type=int, default=2)
    fit.add_argument("--min-units-per-source", type=int, default=3)
    fit.add_argument("--cluster-distance", type=float, default=0.65)
    fit.add_argument("--match-threshold", type=float, default=None)

    translate = subparsers.add_parser(
        "translate",
        help="translate a prepared one-source evidence batch with a frozen model",
    )
    translate.add_argument("model")
    translate.add_argument("evidence")
    translate.add_argument("--renderer")
    translate.add_argument(
        "--query-recording",
        action="append",
        default=None,
        help="translate only units from this recording ID; repeatable",
    )

    args = parser.parse_args()

    if args.command == "prepare-wav":
        samples, sample_rate = _read_wav(args.wav)
        rows = prepare_audio_evidence(
            args.recording_id,
            args.source_id,
            samples,
            sample_rate,
            novelty_threshold=args.novelty_threshold,
            min_event_s=args.min_event_s,
            cluster_distance=args.event_cluster_distance,
        )
        for row in rows:
            print(json.dumps(asdict(row), sort_keys=True))
        return

    if args.command == "fit":
        model, registry = fit_reference_translator(
            _load_episodes(args.episodes),
            semantic_min_sources=args.semantic_min_sources,
            min_sources=args.min_sources,
            min_units_per_source=args.min_units_per_source,
            cluster_distance=args.cluster_distance,
            match_threshold=args.match_threshold,
        )
        print(
            json.dumps(
                {
                    "model": model.to_dict(),
                    "training_registry": registry.to_dict(),
                },
                indent=2,
                sort_keys=True,
            )
        )
        return

    model = _load_model(args.model)
    evidence = _load_evidence(args.evidence)
    query_keys = None
    if args.query_recording:
        allowed = set(args.query_recording)
        query_keys = [
            (row.recording_id, row.source_id, row.local_unit_id)
            for row in evidence
            if row.recording_id in allowed
        ]
        if not query_keys:
            raise ValueError("no evidence rows matched --query-recording")

    result = translate_source_evidence(
        model,
        evidence,
        query_keys=query_keys,
        renderer=_load_renderer(args.renderer),
    )
    print(json.dumps(asdict(result), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
