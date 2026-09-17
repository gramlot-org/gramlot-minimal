# 020 · Verification status

Document ID: **GS-020**.

[Concise counterpart](../docs_llm/020-verification.md).

<a id="gs-020-005"></a>

## 005 · Standalone-owned checks

Block ID: **GS-020-005**.

Verified on 2026-09-16:

- 13 `unittest` cases pass under the staged source tree.
- Python source and tests compile successfully.
- `pyproject.toml` parses and all four maintained guide pairs share document IDs.
- Tests cover missing provider/no output, unsafe CSS/no output, page/resource symlink
  escape, bounded CSS diagnostics, envelope duplicates/cycles/depth/detachment,
  site/schema/codec checks, provider profile and finite JSON, deterministic HTML,
  raw-text-safe runtime/source embedding, output/receipt collision and atomic replace.

<a id="gs-020-010"></a>

## 010 · Distribution checks

Block ID: **GS-020-010**.

Using CPython 3.12.9 with local build dependencies and no network, `python -m build
--no-isolation` produced an sdist and a `py3-none-any` wheel. An isolated `-I`
zip-import check loaded the wheel's CLI and envelope modules, round-tripped an
envelope, and reported CLI version `0.0.0.dev0`.

Build outputs are verification artifacts outside the repository and are excluded by
`.gitignore`; they are not releases or publications.

A packaging-only JSDOM smoke opened the fixture HTML at a `file://` URL with an
offline resource loader and throwing `fetch`. The base64 runtime containing a
mixed-case `</ScRiPt>` sequence executed as text, embedded JSON reconstructed its
`</script>` value, no image injection occurred, and no request or JSDOM error was
recorded. This verifies HTML encoding/bootstrapping only, not CSP or Gramlot runtime
behavior. The fixture HTML remains outside the repository.

<a id="gs-020-015"></a>

## 015 · Deliberately unverified integration

Block ID: **GS-020-015**.

The fixture provider validates packaging contracts only. It is not a Gramlot runtime
or application. No accepted core provider exists, so Python Source hydration,
bindings, formulas, controllers, resolver behavior, page navigation, atomic Bag
replacement, unified print and updated-HTML download remain unverified. A fixture
JSDOM smoke can check HTML/base64 decoding but cannot change that status. The real
blocked-network browser gate remains **GS-015-030**.
