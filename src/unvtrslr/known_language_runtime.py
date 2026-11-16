"""Offline known-human-language translation via an EXTERNAL, installed Argos engine.

This is not UNVTRSLR's native semantic learner. This adapter never requests
model downloads or installation; external Argos may fetch missing SBD
resources unless the cache-only preflight succeeds. No quality certification.
"""
from __future__ import annotations

from collections import deque
from dataclasses import asdict, dataclass
import os
import re
from typing import Any


MAX_SOURCE_CHARS = 8192
MAX_OUTPUT_CHARS = 16384


class KnownLanguageError(ValueError):
    """A known-language translation was not safely executable."""


@dataclass(frozen=True)
class KnownLanguageTranslation:
    status: str
    provenance: str
    source_language: str
    target_language: str
    route: tuple[str, ...]
    translated_text: str

    def to_dict(self) -> dict:
        return asdict(self)


def _engine(provider: Any | None, *, no_sbd_download: bool = False) -> Any:
    if provider is not None:
        argos = provider
    else:
        # Select the supported MiniSBD splitter before importing Argos.
        # Cached-model verification below rejects a missing SBD file.
        if no_sbd_download:
            os.environ["ARGOS_CHUNK_TYPE"] = "MINISBD"
        try:
            import argostranslate.translate as argos
        except ImportError as exc:
            raise KnownLanguageError(
                "Argos Translate is not installed. Install the optional known-languages "
                "dependency and model packages deliberately; no automatic downloads."
            ) from exc
        if argos.settings.model_provider != argos.settings.ModelProvider.OPENNMT:
            raise KnownLanguageError(
                "Only the local Argos OpenNMT backend is permitted; remote model provider refused."
            )
    if no_sbd_download:
        settings = getattr(argos, "settings", None)
        types = getattr(settings, "ChunkType", None)
        mini_type = getattr(types, "MINISBD", None)
        if mini_type is None or getattr(settings, "chunk_type", None) != mini_type:
            raise KnownLanguageError(
                "No-SBD-download mode requires active ARGOS_CHUNK_TYPE=MINISBD. "
                "Run in a fresh process with --no-sbd-download; an already-imported "
                "Argos engine may have initialized another sentence splitter."
            )
    return argos


def _installed_graph(provider: Any | None, *, no_sbd_download: bool = False):
    engine = _engine(provider, no_sbd_download=no_sbd_download)
    direct_type = getattr(engine, "PackageTranslation", None)
    if direct_type is None:
        raise KnownLanguageError("Backend lacks the installed-package translation interface.")
    languages = {lang.code: lang for lang in engine.get_installed_languages()}
    edges: dict[tuple[str, str], Any] = {}
    for code, language in languages.items():
        for direct in language.translations_from:
            origin = getattr(getattr(direct, "from_lang", None), "code", None)
            target = getattr(getattr(direct, "to_lang", None), "code", None)
            unwrapped = direct
            cached_type = getattr(engine, "CachedTranslation", None)
            if cached_type is not None and isinstance(unwrapped, cached_type):
                unwrapped = unwrapped.underlying
            if isinstance(unwrapped, direct_type) and origin == code and target in languages and origin != target:
                edges[(code, target)] = direct
    return languages, edges, engine


def _require_cached_sbd(engine: Any, route: tuple[str, ...], edges) -> None:
    """Refuse known MiniSBD first-use downloads on every selected direct hop."""
    sbd = getattr(engine, "sbd", None)
    splitter_type = getattr(sbd, "MiniSBDSentencizer", None)
    models = getattr(sbd, "minisbd_models", None)
    cache_dir = getattr(models, "cache_dir", None)
    catalog = getattr(models, "MODELS", None)
    if splitter_type is None or not isinstance(catalog, dict) or not isinstance(cache_dir, (str, os.PathLike)):
        raise KnownLanguageError("MiniSBD cache cannot be verified; refusing cache-only translation.")

    cached_type = getattr(engine, "CachedTranslation", None)
    for source, target in zip(route, route[1:]):
        direct = edges[(source, target)]
        if cached_type is not None and isinstance(direct, cached_type):
            direct = direct.underlying
        splitter = getattr(direct, "sentencizer", None)
        if not isinstance(splitter, splitter_type):
            raise KnownLanguageError("Installed route does not use verifiable MiniSBD sentence splitting.")
        model = getattr(splitter, "lang", None)
        if not isinstance(model, str) or not model:
            raise KnownLanguageError("MiniSBD source model path is unavailable.")
        if model in catalog:
            candidate = os.path.join(cache_dir, catalog[model])
        elif os.path.isabs(model):
            candidate = model
        else:
            candidate = ""
        if not candidate or not os.path.isfile(candidate) or os.path.getsize(candidate) == 0:
            raise KnownLanguageError(
                f"MiniSBD model is not cached for {source}->{target}; "
                "prepare its model during setup, or disable cache-only mode."
            )


def direct_routes(*, provider: Any | None = None, no_sbd_download: bool = False) -> tuple[tuple[str, str], ...]:
    """Only directly installed pairs; never imply a pivot was independently trained."""
    return tuple(sorted(_installed_graph(provider, no_sbd_download=no_sbd_download)[1]))


def _route(source: str, target: str, edges, *, allow_pivot: bool) -> tuple[str, ...]:
    if (source, target) in edges:
        return source, target
    if not allow_pivot:
        raise KnownLanguageError(
            f"Direct translation {source}->{target} not installed; "
            "pivoting requires --allow-pivot and installed directed routes."
        )
    queue = deque([(source,)])
    visited = {source}
    while queue:
        route = queue.popleft()
        for next_code in sorted(to for frm, to in edges if frm == route[-1]):
            if next_code in visited:
                continue
            candidate = (*route, next_code)
            if next_code == target:
                return candidate
            visited.add(next_code)
            queue.append(candidate)
    raise KnownLanguageError(f"No installed translation route {source}->{target}")


def translate_known_text(
    source_language: str,
    target_language: str,
    source_text: str,
    *,
    allow_pivot: bool = False,
    provider: Any | None = None,
    no_sbd_download: bool = False,
) -> KnownLanguageTranslation:
    """Translate source text using explicit installed direct edges and record every hop."""
    if any(
        type(code) is not str or not re.fullmatch(r"[a-z]{2,8}", code)
        for code in (source_language, target_language)
    ):
        raise KnownLanguageError("Provide explicit lower-case Argos language codes.")
    if source_language == target_language:
        raise KnownLanguageError("Source and target are the same; no translation performed.")
    if type(source_text) is not str or not source_text.strip():
        raise KnownLanguageError("Nonempty text is required.")
    if len(source_text) > MAX_SOURCE_CHARS:
        raise KnownLanguageError(f"Source text exceeds {MAX_SOURCE_CHARS} characters.")

    languages, edges, engine = _installed_graph(provider, no_sbd_download=no_sbd_download)
    if source_language not in languages or target_language not in languages:
        raise KnownLanguageError(
            f"Both languages need installed Argos packages: {source_language}, {target_language}."
        )
    route = _route(source_language, target_language, edges, allow_pivot=allow_pivot)
    if no_sbd_download:
        _require_cached_sbd(engine, route, edges)
    candidate = source_text
    for origin, target in zip(route, route[1:]):
        try:
            candidate = edges[(origin, target)].translate(candidate)
        except Exception as exc:
            raise KnownLanguageError(f"External model inference failed at {origin}->{target}.") from exc
        if type(candidate) is not str or not candidate.strip() or len(candidate) > MAX_OUTPUT_CHARS:
            raise KnownLanguageError(f"External model gave invalid output at {origin}->{target}.")
    return KnownLanguageTranslation(
        status="EXTERNAL_MODEL_OUTPUT_UNVERIFIED",
        provenance="ARGOS_EXTERNAL_NOT_UNVTRSLR_NATIVE",
        source_language=source_language,
        target_language=target_language,
        route=route,
        translated_text=candidate,
    )
