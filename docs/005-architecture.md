# 005 · Architecture

Document ID: **GS-005**.

<a id="gs-005-005"></a>
## 005 · Responsibility boundary

Standalone owns build-time bundling, atomic output and HTML packaging. It uses
HtmlBuilder from Builder JS. It does not implement Source, rendering, messaging
or page execution: these belong to Gramlot's WorkerHost, mount and WorkerTransport.

<a id="gs-005-010"></a>
## 010 · Current profile

One JS Page, one classic bundled Worker, one browser runtime and one HTML file.
The module is bundled, not imported/executed by the exporter. At runtime mount
opens the page, prepares Gramlot, calls main and renders the returned typed Source.
Marked Source methods use that same host through messages, without HTTP.

<a id="gs-005-015"></a>
## 015 · Data boundary

Database and application-data import/export are excluded. The former envelope and
complete-v1 provider are removed from the active package, not emulated.

<a id="gs-005-020"></a>
## 020 · Limits

Python pages require Python servers. Node-specific imports fail browser bundling.
Page.css must be empty. CSP blocks network connections; it is not a static proof
that application code never attempts a request. The exporter has no custom runtime,
manual application DOM construction, eval bootstrap or fallback compiler.

Runtime license notices are embedded as inert JSON metadata in the HTML head,
not as a visible panel in the application.
