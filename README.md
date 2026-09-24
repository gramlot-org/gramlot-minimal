# Gramlot Standalone

Build one JavaScript Gramlot Page into a single HTML file that opens from disk.
The Page runs in a dedicated Worker using the real Gramlot Host. It is not executed
at build time, and there is no Python-to-JavaScript compilation.

After installing all four locally prepared npm archives (core, NodeJS adapter,
standalone exporter and Hello World example) into a local consumer directory,
run from that directory:

```sh
npx --no-install gramlot-standalone build node_modules/gramlot-example-app/js/pages/index.js -o build/hello-world.html
```

Open the generated file in the browser. Node is needed to build it, not to open it.
The current local dependency artifacts must be installed until the owning packages
are available upstream; the command above does not imply registry publication.

Applications import Page from `@gramlot/native-html/page`. The same page can run on
Node, Bun or standalone if it uses only browser-compatible imports. The exporter
bundles a classic Worker and the Gramlot browser runtime, and uses HtmlBuilder to
produce the HTML shell. `main` and marked `source` methods execute in the Worker.

Scope: one JS Page, native HTML and live Source, empty Page.css, no database,
Data binding, recipes, data import/export or multipage navigation. The old Python
CLI, compiler provider, complete-v1 profile and TOML configuration are retired;
there is no compatibility wrapper. The command takes the JS page file directly.

[Usage](docs/010-usage.md) · [Architecture](docs/005-architecture.md) ·
[Verification](docs/020-verification.md).

`examples/showcase` and `showcase.zip` are historical PoC artifacts, not output from
this exporter and not evidence for its supported features. They are unchanged.
