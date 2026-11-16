# Known human-language translation (external Argos adapter)

**Evidence ceiling:** offline neural translation by separately installed Argos models,
not UNVTRSLR-native semantic learning, universal translation, or a certified translation.
This entry point does not improve the native held-out multilingual score or establish
translation adequacy. It is an ordinary known-language usability route.

## Run

Install the explicitly optional Python engine in your own isolated environment:

```powershell
python -m pip install -e ".[known-languages]"
$env:ARGOS_PACKAGES_DIR = "D:\path\to\previously-installed\argos\packages"
$env:ARGOS_CHUNK_TYPE = "MINISBD"
$env:ARGOS_DEVICE_TYPE = "cpu"
$env:PYTHONIOENCODING = "utf-8"
python -m unvtrslr.known_language_cli --list-routes
python -m unvtrslr.known_language_cli --from-lang en --to-lang fr --text "Hello" --json
python -m unvtrslr.known_language_cli --from-lang en --to-lang fr --text "Hello" --json --no-sbd-download
"Turn off the light" | python -m unvtrslr.known_language_cli --from-lang en --to-lang de --json
```

Use only model packages obtained and installed separately after checking their
source, license, file integrity, and resource requirements. This CLI implements no index updates, model downloads or installations and
refuses Argos API model providers. **MINISBD alone does not guarantee an
offline first run**: if a MiniSBD model is not bundled or cached, Argos can
download it on first inference. Either prepare and test the sentence splitter
while connected, then rerun with networking disabled, or use
`--no-sbd-download` (sets `ARGOS_CHUNK_TYPE=NONE` before Argos import
and verifies the effective mode). This disables sentence splitting and
can degrade multi-sentence or long-text output. If Argos was already imported
with another setting, this mode fails closed; run it in a fresh process.
It prevents the known automatic SBD-download path, **not** all possible
network access by dependencies; a network-disabled host or sandbox is needed
for a hard offline guarantee.
If the local Argos engine or requested model is absent, it fails rather than
inventing a translation. `--list-routes` lists only independently installed
direct directions, not automatically synthesized paths. `--allow-pivot`
explicitly permits multi-hop translation only along installed direct edges,
with the complete ordered route recorded in the output. A reverse direction
requires its own model or a real directed path. For personal text, prefer stdin
rather than putting content on the command line.

Plain-text mode emits translation on stdout and an external/uncertified
provenance warning on stderr. JSON mode preserves source/target, path,
`EXTERNAL_MODEL_OUTPUT_UNVERIFIED` status and the
`ARGOS_EXTERNAL_NOT_UNVTRSLR_NATIVE` provenance label. JSON emits ASCII-escaped
Unicode for dependable Windows console transport; decoding JSON restores text.
Input is limited to 8192 Unicode code points; each inference hop rejects
empty/nontext/oversized output (16384 code points). Inference failure exits
nonzero, with no replacement pretending to be a translation.

## Verified scope and limitations

The implementation was exercised using the previously installed Argos
1.11.0 CPU environment and its four English-to-German, French, Swahili,
and Turkish model packages. A French sentence translated in live inference;
a French-to-English request correctly failed because no reverse package was
installed. This is functional integration, **not** a new adequate-quality
measurement. See the prior fixed external-model benchmark and its known
Swahili error in `research/ARGOS_REAL_SOURCE_ONLY_20261027.md`. No human
ratings have yet qualified adequacy; do not use without review for medical,
legal, safety-critical, or high-stakes content.

The previously recorded Argos benchmark pinned engine 1.11.0. The
current documentation is for 1.11.1; the minor-version range is included
as an optional installation convenience, **not** a claim that 1.11.1
was tested here. Argos source: https://argos-translate.readthedocs.io/en/latest/
Argos offline caveats: https://argos-translate.readthedocs.io/en/latest/source/troubleshooting.html

Alternatives were considered but not silently adopted: NLLB-200-distilled-600M
(https://huggingface.co/facebook/nllb-200-distilled-600M) is a research
checkpoint subject to CC-BY-NC-4.0 terms; its model card cautions against
production, documents and specialized high-stakes tasks, and Transformers 5
requires direct model use instead of the former translation pipeline.
Model size and language count do not establish universal semantic grounding.
