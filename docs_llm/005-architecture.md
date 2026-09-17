# 005 · Architecture and current status

Document ID: **GS-005**.

[Expanded counterpart](../docs/005-architecture.md).

<a id="gs-005-005"></a>

## 005 · Responsibility boundary

Block ID: **GS-005-005**.

Standalone owns validation, embedding, packaging and its envelope. Core owns Source,
Data Bags, logic, resolvers, typed transport and browser behavior. The synchronous
provider callable is a consumer proposal, not an accepted core API.

<a id="gs-005-010"></a>

## 010 · Complete offline profile

Block ID: **GS-005-010**.

The full profile includes pages/navigation, bindings, logic, browser resolvers,
shared Data, atomic import, unified print and updated HTML. It rejects server
behavior. CSP blocks connections and resources are embedded, but provider metadata
is not proof; real blocked-network browser verification remains required.

<a id="gs-005-015"></a>

## 015 · Data boundary

Block ID: **GS-005-015**.

Only `application_data` is exported. Its versioned payload is opaque to standalone
and requires the core typed Bag codec. Complete validation precedes atomic replace;
failure preserves current Data. UI/service state is excluded.

<a id="gs-005-020"></a>

## 020 · Verified and blocked scope

Block ID: **GS-005-020**.

Tests cover standalone-owned contracts with a non-runtime fixture. Clean core lacks
accepted integration ports, so default builds fail without output and no end-to-end
offline/PDF behavior is claimed. See **GS-015**.
