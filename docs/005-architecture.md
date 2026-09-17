# 005 · Architecture and current status

Document ID: **GS-005**.

[Concise counterpart](../docs_llm/005-architecture.md).

<a id="gs-005-005"></a>

## 005 · Responsibility boundary

Block ID: **GS-005-005**.

`gramlot-standalone` owns project validation, local resource embedding, HTML
assembly and the portable data envelope. Core owns Python Source construction,
Data Bags, bindings, controllers, resolver semantics, typed transport and browser
behavior. This repository never supplies a substitute runtime.

The provisional integration is one synchronous callable. It returns compiled
pages, one complete browser program, typed initial data, provenance, notices and
capability declarations. It is a consumer proposal, not an accepted core API.

<a id="gs-005-010"></a>

## 010 · Complete offline profile

Block ID: **GS-005-010**.

The requested artifact must start from `file://` without a server. The complete
profile includes multiple pages, navigation, bindings, formulas, controllers,
browser-compatible resolvers, shared Data, atomic import, unified printing and
updated-HTML download. The compiler must report no external imports or server
declarations. `dataRpc` and server resolvers are prohibited in this profile.

The generated HTML sets `connect-src 'none'`, contains no external script or
stylesheet elements, and embeds local resources as data URLs. Provider reports and
capability declarations are metadata, not independent proof of runtime behavior.
A blocked-network real-browser test is required before offline support is verified.

<a id="gs-005-015"></a>

## 015 · Data boundary

Block ID: **GS-005-015**.

Only `application_data` crosses JSON export/import. UI, Source, resolver, service
and subscription state remain internal. The envelope carries site/schema and codec
identity. Its payload is opaque; standalone does not flatten Bags or claim that
plain JSON preserves types, attributes, ordering or nested Bags.

The provider must decode and validate a complete candidate before one atomic branch
replacement. Any failure retains the current branch exactly. Typed Bag and atomic
notification tests belong to the owning core port; this repository tests only the
outer envelope and capability gate.

<a id="gs-005-020"></a>

## 020 · Verified and blocked scope

Block ID: **GS-005-020**.

Tests cover project/config validation, symlink containment, bounded CSS handling,
resource embedding, envelope validation, provider gates, deterministic HTML,
script-safe encoding, atomic output and missing-provider failure. The fixture
provider is neither a demo nor a runtime.

The clean core has no accepted compiler/runtime ports, so the default CLI fails
before writing output. No end-to-end Python Page build, browser `file://` test,
direct PDF generator or fillable PDF claim is present. See **GS-015**.
