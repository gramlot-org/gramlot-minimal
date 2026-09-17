# 010 · Project and CLI guide

Document ID: **GS-010**.

[Concise counterpart](../docs_llm/010-usage.md).

<a id="gs-010-005"></a>

## 005 · Project discovery

Block ID: **GS-010-005**.

A project has a flat `pages/` directory. Public filenames are lowercase slugs;
underscore files are ignored. Standalone resolves and hashes pages without executing
them. Symlinks for page, style, resource and configuration inputs must remain inside
their owning project directory.

Optional `gramlot-standalone.toml`:

```toml
[site]
id = "my-site"
title = "My Site"
schema_version = 1
initial_page = "index"
```

Without `initial_page`, `index` wins when present, otherwise the first sorted slug.

<a id="gs-010-010"></a>

## 010 · CSS and resources

Block ID: **GS-010-010**.

`style.css` and `styles/**/*.css` are concatenated. `resources/**` files are exposed
to the provider as data URLs. Simple quoted/unquoted CSS `url(...)` references may
target these resources; SVG fragments are retained. Remote URLs, query strings,
path escapes, CSS escapes, HTML style terminators and every `@import` fail with a
diagnostic. This is an explicit bounded subset, not a complete CSS parser.

Page-owned styles remain Gramlot `styleSheet`/`css` declarations. Project CSS is
for the document shell and explicitly shared local resources.

<a id="gs-010-015"></a>

## 015 · Build and failure contract

Block ID: **GS-010-015**.

```console
gramlot-standalone build ./my-site -o my-site.html
```

The output path must end in `.html` or `.htm`. `--build-info receipt.json` writes a
separate hash/provenance receipt. Output is replaced atomically only after project,
provider, complete-profile declarations, offline report, pages, JSON data,
provenance, notices and final HTML pass validation. Missing integration, unsafe CSS
or invalid provider data writes no HTML.

`--provider module:callable` is hidden from normal help. It exists for bounded
integration development and tests; it is not an accepted core API or production
fallback. The default proposed location is `gramlot.standalone:compile_project`.

<a id="gs-010-020"></a>

## 020 · Data envelope limits

Block ID: **GS-010-020**.

Envelope JSON is limited to 10,000,000 UTF-8 bytes and 256 nested container levels.
Duplicate object keys, non-finite numbers, non-JSON values, cycles, mismatched site,
schema or requested codec fail. Construction detaches the payload from caller-owned
mutable dictionaries/lists. These checks do not decode or validate typed Bag
semantics; that remains the provider's responsibility.
