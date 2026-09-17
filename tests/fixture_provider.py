"""Contract fixture only; not a Gramlot runtime or application example."""
DECLARATIONS = [
    "embedded-source-v1", "offline-resolvers-v1", "typed-application-data-v1",
    "atomic-application-data-import-v1", "multipage-lifecycle-v1",
    "unified-print-view-v1", "download-updated-html-v1",
]
def compile_project(request):
    project = request["project"]
    return {
        "protocol": "gramlot-standalone-compiler", "version": 1,
        "capability_declarations": DECLARATIONS,
        "offline_report": {"compiler": "test-fixture", "external_imports": [],
                           "server_declarations": []},
        "runtime_js": 'globalThis.fixture="</ScRiPt><img src=x>";',
        "pages": [{"slug": item["slug"], "title": item["slug"].title(),
                   "source": {"fixture": item["sha256"], "text": "</script>"}}
                  for item in project["pages"]],
        "application_data": {"format": "gramlot-standalone-application-data",
            "version": 1, "site_id": project["site_id"],
            "schema_version": project["schema_version"],
            "codec": {"name": "fixture-only", "version": 1},
            "application_data": None},
        "provenance": {"name": "test-fixture", "version": "0"},
        "notices": [{"name": "Fixture", "text": "Not a distributable runtime."}],
    }
