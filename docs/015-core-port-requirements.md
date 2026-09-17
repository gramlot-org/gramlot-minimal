# 015 · Core port requirements

Document ID: **GS-015**.

[Concise counterpart](../docs_llm/015-core-port-requirements.md).

<a id="gs-015-005"></a>

## 005 · Acceptance boundary

Block ID: **GS-015-005**.

These requirements were discovered by a consumer. They are not accepted Gramlot
APIs, port records or amendments. Each requires a bounded core port with contract,
ownership, implementation, meaningful tests, omissions, paired documentation and
destination review before standalone can depend on it.

<a id="gs-015-010"></a>

## 010 · Python Source and embedded hydration

Block ID: **GS-015-010**.

Core must load trusted Python Pages, build each Source, serialize typed ordinary Bag
branches, and hydrate an embedded payload without `fetch`. The contract identifies
page titles, Source format/version, builder, component modules and failures. Browser
controllers/formulas must not execute during Python compilation.

<a id="gs-015-015"></a>

## 015 · Offline declarations and resolvers

Block ID: **GS-015-015**.

Core must classify the offline profile. `dataRpc`, host endpoints and server
resolvers fail with page/node context. Browser resolvers need an accepted typed
Source transport, lifecycle, cancellation, failure and cleanup contract. PoC
`transport.snapshot` currently permits only `RpcResolver`, so it cannot be reused as
evidence that browser resolver descriptions already travel.

<a id="gs-015-020"></a>

## 020 · Browser bundle and provenance

Block ID: **GS-015-020**.

Core must provide a reproducible browser bundle with no external imports or network
startup, plus version/hash, licenses, third-party notices and supported capabilities.
It owns the multi-page/navigation lifecycle, Gramlot-based data controls, unified
print view and updated-HTML export. Site maps and unpublished wheels are evidence,
not accepted distribution inputs.

<a id="gs-015-025"></a>

## 025 · Typed shared application data

Block ID: **GS-015-025**.

Core must define `application_data` ownership across pages and a JSON-compatible
typed Bag codec preserving approved values, nested shape, ordering and required
attributes. It validates the full candidate and replaces one branch atomically,
emitting notifications only after success. Failure retains the exact current branch.
UI, Source, resolver, service and subscription state never enter the envelope.

<a id="gs-015-030"></a>

## 030 · Required real-browser verification

Block ID: **GS-015-030**.

Open the generated file with connections blocked. Navigate pages; edit bindings;
run formulas/controllers and browser resolvers; round-trip typed shared Data; reject
an invalid import without mutation; print every page; download updated HTML; reopen
it and verify embedded Data. Record browser/version and bundle provenance. Passing
packager fixture tests does not satisfy this integration gate.
