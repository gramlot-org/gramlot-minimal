# Gramlot standalone repository instructions

Read `../gramlot/docs/00-constitution.md`, `../gramlot/docs/01-overview.md`,
`../gramlot/ports/README.md`, and `../gramlot/docs/005-documentation-policy.md`
before changing this repository. The Gramlot constitution is authoritative.

- Keep code and maintained documentation in English.
- This repository owns project validation and offline packaging. It does not own
  Gramlot Source, Data Bags, or their browser runtime.
- Never ship a substitute runtime. Fail if an accepted integration is unavailable.
- Offline builds reject `dataRpc` and server resolvers. Browser resolvers require
  an accepted core transport contract.
- Only `application_data` crosses the JSON boundary through a typed Bag codec.
- Pair `docs` and `docs_llm` guides and preserve GS document/block IDs.
- Do not publish, release, deploy, push, or change visibility without authorization.


## Accepted native profile — 2026-09-24

Owner accepted the clean-core native 0.1.0 and GitHub archive delivery. Use the
current native APIs and paired guides. Earlier PoC-only runtime/compiler/data
envelope instructions describe historical work; they do not override the native
Host/Page/Worker contract. No registry publication or deployment is authorized.
