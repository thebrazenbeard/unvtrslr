"""Known-human-language runtime contracts; mocks stand only for external Argos objects."""
import io
import json
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

from unvtrslr.known_language_runtime import (
    KnownLanguageError,
    direct_routes,
    translate_known_text,
)
from unvtrslr.known_language_cli import main


def backend(*pairs, fail=None, invalid=None):
    codes = sorted({item for pair in pairs for item in pair})
    langs = {code: SimpleNamespace(code=code, translations_from=[]) for code in codes}

    class Direct:
        def __init__(self, frm, to):
            self.from_lang, self.to_lang = langs[frm], langs[to]

        def translate(self, text):
            if (self.from_lang.code, self.to_lang.code) == fail:
                raise RuntimeError("unexpected model runtime problem")
            if (self.from_lang.code, self.to_lang.code) == invalid:
                return ""
            return f"{self.to_lang.code}[{text}]"

    for frm, to in pairs:
        langs[frm].translations_from.append(Direct(frm, to))
    return SimpleNamespace(PackageTranslation=Direct, get_installed_languages=lambda: list(langs.values()))


def test_known_language_cli_exposes_a_real_entrypoint():
    result = subprocess.run(
        [sys.executable, "-m", "unvtrslr.known_language_cli", "--help"],
        cwd=Path(__file__).parents[1], text=True, capture_output=True, timeout=30,
    )
    assert result.returncode == 0, result.stderr
    assert "--from-lang" in result.stdout
    assert "--to-lang" in result.stdout


def test_direct_translation_never_claims_native_grounded_meaning():
    result = translate_known_text("en", "fr", "Turn off the light", provider=backend(("en", "fr")))
    assert result.translated_text == "fr[Turn off the light]"
    assert result.route == ("en", "fr")
    assert result.status == "EXTERNAL_MODEL_OUTPUT_UNVERIFIED"
    assert result.provenance == "ARGOS_EXTERNAL_NOT_UNVTRSLR_NATIVE"


def test_direct_routes_are_only_installed_edges_not_implicit_pivots():
    b = backend(("en", "fr"), ("fr", "de"))
    assert direct_routes(provider=b) == (("en", "fr"), ("fr", "de"))
    with pytest.raises(KnownLanguageError, match="pivoting requires"):
        translate_known_text("en", "de", "Hello", provider=b)


def test_explicit_pivot_runs_only_real_edges_in_order():
    b = backend(("en", "fr"), ("fr", "de"))
    result = translate_known_text("en", "de", "Hello", allow_pivot=True, provider=b)
    assert result.route == ("en", "fr", "de")
    assert result.translated_text == "de[fr[Hello]]"


def test_explicit_pivot_does_not_invent_missing_reverse():
    b = backend(("en", "fr"), ("fr", "de"))
    with pytest.raises(KnownLanguageError, match="No installed translation route"):
        translate_known_text("de", "en", "Hallo", allow_pivot=True, provider=b)


def test_uninstalled_code_errors_instead_of_hallucinating_translation():
    b = backend(("en", "fr"))
    with pytest.raises(KnownLanguageError, match="installed Argos packages"):
        translate_known_text("en", "sw", "Hello", provider=b)


@pytest.mark.parametrize("code", ["EN", "../en", "en-US", "", "en fr", 7])
def test_invalid_language_code_is_rejected(code):
    with pytest.raises(KnownLanguageError, match="lower-case"):
        translate_known_text(code, "fr", "Hello", provider=backend(("en", "fr")))


@pytest.mark.parametrize("text", ["", " ", "x" * 8193, None])
def test_empty_oversized_and_nontext_inputs_are_rejected(text):
    with pytest.raises(KnownLanguageError):
        translate_known_text("en", "fr", text, provider=backend(("en", "fr")))


def test_same_language_is_not_falsely_reported_as_translation():
    with pytest.raises(KnownLanguageError, match="same"):
        translate_known_text("en", "en", "Hello", provider=backend(("en", "fr")))


def test_failed_or_empty_external_inference_must_not_be_reported_successfully():
    for arg in ("fail", "invalid"):
        bad = backend(("en", "fr"), **{arg: ("en", "fr")})
        with pytest.raises(KnownLanguageError, match="inference failed|invalid output"):
            translate_known_text("en", "fr", "Hello", provider=bad)


def test_cli_json_result_has_route_and_provenance(capsys, monkeypatch):
    monkeypatch.setattr(sys, "stdin", io.StringIO("Hello!"))
    assert main(["--from-lang", "en", "--to-lang", "fr", "--json"], provider=backend(("en", "fr"))) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["translated_text"] == "fr[Hello!]"
    assert output["route"] == ["en", "fr"]
    assert output["status"] == "EXTERNAL_MODEL_OUTPUT_UNVERIFIED"


def test_cli_exposes_installed_routes_and_does_not_invent_other_pairs(capsys):
    assert main(["--list-routes", "--json"], provider=backend(("en", "fr"), ("fr", "de"))) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["direct_routes"] == [{"source": "en", "target": "fr"}, {"source": "fr", "target": "de"}]


def test_cli_missing_reverse_returns_nonzero_without_fake_output(capsys):
    code = main(["--from-lang", "fr", "--to-lang", "en", "--text", "bonjour"],
                provider=backend(("en", "fr")))
    captured = capsys.readouterr()
    assert code == 2
    assert captured.out == ""
    assert "not installed" in captured.err




def test_vendor_synthesized_composite_must_not_be_falsely_listed_as_direct():
    b = backend(("en", "fr"), ("fr", "de"))
    langs = {lang.code: lang for lang in b.get_installed_languages()}

    class Composite:
        from_lang, to_lang = langs["en"], langs["de"]

        def translate(self, text):
            return "invented-direct"

    langs["en"].translations_from.append(Composite())
    assert ("en", "de") not in direct_routes(provider=b)
    with pytest.raises(KnownLanguageError, match="pivoting requires"):
        translate_known_text("en", "de", "Hello", provider=b)


def test_real_argos_cached_wrapper_is_direct_only_when_wrapping_package_translation():
    b = backend(("en", "fr"))
    langs = {lang.code: lang for lang in b.get_installed_languages()}

    class Cached:
        def __init__(self, underlying):
            self.underlying = underlying
            self.from_lang, self.to_lang = underlying.from_lang, underlying.to_lang

        def translate(self, text):
            return self.underlying.translate(text)

    raw = langs["en"].translations_from.pop()
    langs["en"].translations_from.append(Cached(raw))
    b.CachedTranslation = Cached
    assert direct_routes(provider=b) == (("en", "fr"),)
    assert translate_known_text("en", "fr", "Hi", provider=b).translated_text == "fr[Hi]"


def test_json_escapes_non_ascii_for_windows_stdout_without_losing_unicode(capsys):
    assert main(["--from-lang", "en", "--to-lang", "fr", "--text", "caf\u00e9", "--json"],
                provider=backend(("en", "fr"))) == 0
    raw = capsys.readouterr().out
    assert "\\u00e9" in raw
    assert json.loads(raw)["translated_text"] == "fr[caf\u00e9]"


def cached_minisbd_backend(tmp_path, *, has_cache=True, configured="MINISBD"):
    b = backend(("en", "fr"))
    b.settings = SimpleNamespace(
        ChunkType=SimpleNamespace(MINISBD="MINISBD"), chunk_type=configured,
        ModelProvider=SimpleNamespace(OPENNMT="OPENNMT"), model_provider="OPENNMT",
    )

    class MiniSBDSentencizer:
        def __init__(self, lang):
            self.lang = lang

    b.sbd = SimpleNamespace(
        MiniSBDSentencizer=MiniSBDSentencizer,
        minisbd_models=SimpleNamespace(
            cache_dir=str(tmp_path), MODELS={"en": "en.onnx"},
        ),
    )
    lang = next(l for l in b.get_installed_languages() if l.code == "en")
    lang.translations_from[0].sentencizer = MiniSBDSentencizer("en")
    if has_cache:
        (tmp_path / "en.onnx").write_bytes(b"local-model")
    return b


def test_no_sbd_download_mode_refuses_other_active_splitter(tmp_path):
    b = cached_minisbd_backend(tmp_path, configured="NONE")
    with pytest.raises(KnownLanguageError, match="active ARGOS_CHUNK_TYPE=MINISBD"):
        translate_known_text(
            "en", "fr", "Hello", provider=b, no_sbd_download=True,
        )


def test_no_sbd_download_mode_requires_cached_model(tmp_path):
    b = cached_minisbd_backend(tmp_path, has_cache=False)
    with pytest.raises(KnownLanguageError, match="MiniSBD model is not cached"):
        translate_known_text(
            "en", "fr", "Hello", provider=b, no_sbd_download=True,
        )


def test_no_sbd_download_mode_accepts_cached_model_and_preserves_provenance(capsys, tmp_path):
    b = cached_minisbd_backend(tmp_path)
    code = main([
        "--from-lang", "en", "--to-lang", "fr", "--text", "Hello",
        "--no-sbd-download", "--json",
    ], provider=b)
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["route"] == ["en", "fr"]
    assert payload["translated_text"] == "fr[Hello]"
    assert payload["status"] == "EXTERNAL_MODEL_OUTPUT_UNVERIFIED"


def test_no_sbd_download_mode_refuses_unverifiable_provider_settings():
    b = backend(("en", "fr"))
    with pytest.raises(KnownLanguageError, match="active ARGOS_CHUNK_TYPE=MINISBD"):
        translate_known_text(
            "en", "fr", "Hello", provider=b, no_sbd_download=True,
        )


def test_no_sbd_configures_minisbd_before_argos_import(monkeypatch, tmp_path):
    import builtins
    import os

    b = cached_minisbd_backend(tmp_path)
    original_import = builtins.__import__
    observed = []

    def fake_import(name, globals=None, locals=None, fromlist=(), level=0):
        if name == "argostranslate.translate":
            observed.append(os.environ.get("ARGOS_CHUNK_TYPE"))
            return SimpleNamespace(translate=b)
        return original_import(name, globals, locals, fromlist, level)

    monkeypatch.setenv("ARGOS_CHUNK_TYPE", "NONE")
    monkeypatch.setattr(builtins, "__import__", fake_import)
    result = translate_known_text(
        "en", "fr", "Hello", no_sbd_download=True,
    )
    assert observed == ["MINISBD"]
    assert result.translated_text == "fr[Hello]"
