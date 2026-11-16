"""Offline known-human-language translation via an EXTERNAL, installed Argos engine.

This is not UNVTRSLR's native semantic learner. No model downloads, installs,
language inference, quality certification, or network calls occur here.
"""
from __future__ import annotations

from collections import deque
from dataclasses import asdict, dataclass
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


def _engine(provider: Any | None) -> Any:
    if provider is not None:
        return provider
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
    return argos


def _installed_graph(provider: Any | None):
    engine = _engine(provider)
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
    return languages, edges


def direct_routes(*, provider: Any | None = None) -> tuple[tuple[str, str], ...]:
    """Only directly installed pairs; never imply a pivot was independently trained."""
    return tuple(sorted(_installed_graph(provider)[1]))


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

    languages, edges = _installed_graph(provider)
    if source_language not in languages or target_language not in languages:
        raise KnownLanguageError(
            f"Both languages need installed Argos packages: {source_language}, {target_language}."
        )
    route = _route(source_language, target_language, edges, allow_pivot=allow_pivot)
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
