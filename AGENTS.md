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
