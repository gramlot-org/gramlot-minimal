"""Deterministic single-file HTML assembly.

The supplied browser program owns Gramlot behavior. This module only embeds its
validated inputs and enforces a no-connect Content Security Policy.
"""
from __future__ import annotations
import base64
import hashlib
import html
import json
from typing import Any
from .project import Project
from .provider import CompiledSite

def _json_script(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, allow_nan=False, sort_keys=True,
                      separators=(",", ":")).replace("<", "\\u003c").replace("&", "\\u0026")

def build_html(project: Project, compiled: CompiledSite) -> tuple[str, dict[str, Any]]:
    pages = [{"slug": item.slug, "title": item.title, "source": item.source}
             for item in compiled.pages]
    resources = {item.name: {"media_type": item.media_type, "sha256": item.sha256,
                             "data_url": item.data_url} for item in project.resources}
    build = {"protocol": 1, "site_id": project.site_id,
             "schema_version": project.schema_version, "initial_page": project.initial_page,
             "capability_declarations": sorted(compiled.capability_declarations),
             "offline_report": dict(compiled.offline_report),
             "provenance": dict(compiled.provenance)}
    notices = "\n\n".join(f"{item['name']}\n{item['text']}" for item in compiled.notices)
    artifact = f"""<!doctype html>
<html lang="en" data-gramlot-standalone="1">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src 'unsafe-inline' 'unsafe-eval' blob:; style-src 'unsafe-inline'; img-src data: blob:; font-src data:; connect-src 'none'; media-src data: blob:; object-src 'none'; frame-src 'none'; base-uri 'none'; form-action 'none'">
<title>{html.escape(project.title)}</title>
<style>{project.css}</style>
</head>
<body>
<main id="gramlot-standalone-root"></main>
<details><summary>Licenses and build provenance</summary><pre>{html.escape(notices)}</pre></details>
<script type="application/json" id="gramlot-pages">{_json_script(pages)}</script>
<script type="application/json" id="gramlot-resources">{_json_script(resources)}</script>
<script type="application/json" id="gramlot-application-data">{_json_script(compiled.envelope.as_dict())}</script>
<script type="application/json" id="gramlot-build-info">{_json_script(build)}</script>
<script>(0,eval)(new TextDecoder().decode(Uint8Array.from(atob("{base64.b64encode(compiled.runtime_js.encode('utf-8')).decode('ascii')}"),c=>c.charCodeAt(0))));</script>
</body>
</html>
"""
    encoded = artifact.encode("utf-8")
    info = {"bytes": len(encoded), "sha256": hashlib.sha256(encoded).hexdigest(),
            "pages": [page.slug for page in compiled.pages],
            "resources": len(project.resources), "provider": dict(compiled.provenance),
            "offline_report": dict(compiled.offline_report)}
    return artifact, info
