# 010 · Project and CLI guide

Document ID: **GS-010**.

[Expanded counterpart](../docs/010-usage.md).

<a id="gs-010-005"></a>

## 005 · Project discovery

Block ID: **GS-010-005**.

Use flat public Python files in `pages/`; underscore files are ignored. Optional
TOML sets site ID/title, positive schema version and initial page. `index` is the
default when present. Input symlinks may not leave their owning directories.

<a id="gs-010-010"></a>

## 010 · CSS and resources

Block ID: **GS-010-010**.

Root/style-directory CSS is embedded; `resources/**` becomes data URLs. A bounded
simple `url(...)` subset supports local resources and fragments. Remote/query/path
escape URLs, CSS escapes, style terminators and `@import` fail. Page styles remain
Gramlot declarations.

<a id="gs-010-015"></a>

## 015 · Build and failure contract

Block ID: **GS-010-015**.

`gramlot-standalone build ./my-site -o my-site.html` validates everything before an
atomic output replacement. Missing provider or unsafe/invalid input writes no HTML.
The hidden provider option and default module location are provisional integration
surfaces, not accepted APIs.

<a id="gs-010-020"></a>

## 020 · Data envelope limits

Block ID: **GS-010-020**.

Envelope text is limited to 10 MB/256 levels and rejects duplicate keys, non-finite
or non-JSON data, cycles and identity mismatches. Payloads are detached. Typed Bag
validation remains core-owned.
