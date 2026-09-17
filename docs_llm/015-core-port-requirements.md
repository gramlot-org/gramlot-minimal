# 015 · Core port requirements

Document ID: **GS-015**.

[Expanded counterpart](../docs/015-core-port-requirements.md).

<a id="gs-015-005"></a>

## 005 · Acceptance boundary

Block ID: **GS-015-005**.

These are consumer requirements, not accepted APIs/amendments. Core must prepare,
review, test, document and accept bounded ports.

<a id="gs-015-010"></a>

## 010 · Python Source and embedded hydration

Block ID: **GS-015-010**.

Compile trusted Python Pages to typed embedded Source and hydrate without fetch.
Declare page/builder/component metadata and keep browser logic in the browser.

<a id="gs-015-015"></a>

## 015 · Offline declarations and resolvers

Block ID: **GS-015-015**.

Reject RPC/endpoints/server resolvers with context. Define browser-resolver transport
and lifecycle; the PoC RPC-only snapshot is inadequate.

<a id="gs-015-020"></a>

## 020 · Browser bundle and provenance

Block ID: **GS-015-020**.

Provide a reproducible no-import/no-network-startup bundle, provenance/notices and
core-owned page/data/print/updated-HTML lifecycle. Preview artifacts are evidence.

<a id="gs-015-025"></a>

## 025 · Typed shared application data

Block ID: **GS-015-025**.

Define shared branch ownership and a typed JSON codec. Validate fully and replace
atomically; failure preserves Data. Exclude UI/service/runtime state.

<a id="gs-015-030"></a>

## 030 · Required real-browser verification

Block ID: **GS-015-030**.

A blocked-network browser test must cover pages, bindings, logic, browser resolvers,
typed round trip, failed-import retention, print and reopened updated HTML.
