"""Strict provisional seam to the owning Gramlot compiler/runtime."""
from __future__ import annotations
from dataclasses import dataclass
import importlib
import inspect
import json
from typing import Any, Callable, Mapping
from .envelope import DataEnvelope, EnvelopeError
from .errors import ProviderError
from .project import Project

PROTOCOL = "gramlot-standalone-compiler"
PROTOCOL_VERSION = 1
DEFAULT_PROVIDER = "gramlot.standalone:compile_project"
REQUIRED_DECLARATIONS = frozenset({
    "embedded-source-v1", "offline-resolvers-v1", "typed-application-data-v1",
    "atomic-application-data-import-v1", "multipage-lifecycle-v1",
    "unified-print-view-v1", "download-updated-html-v1",
})

@dataclass(frozen=True, slots=True)
class CompiledPage:
    slug: str
    title: str
    source: Any

@dataclass(frozen=True, slots=True)
class CompiledSite:
    pages: tuple[CompiledPage, ...]
    runtime_js: str
    envelope: DataEnvelope
    capability_declarations: frozenset[str]
    offline_report: Mapping[str, Any]
    provenance: Mapping[str, Any]
    notices: tuple[Mapping[str, str], ...]

def load_provider(spec: str = DEFAULT_PROVIDER) -> Callable[[dict[str, Any]], Mapping[str, Any]]:
    module_name, separator, object_name = spec.partition(":")
    if not separator or not module_name or not object_name:
        raise ProviderError("Provider must use module:callable syntax")
    try:
        module = importlib.import_module(module_name)
    except (ImportError, ModuleNotFoundError) as error:
        if spec == DEFAULT_PROVIDER:
            raise ProviderError(
                "Accepted Gramlot standalone compiler is unavailable. The clean core does not "
                "yet provide gramlot.standalone.compile_project; see GS-015 core port requirements."
            ) from error
        raise ProviderError(f"Cannot import provider module {module_name!r}: {error}") from error
    target: Any = module
    for part in object_name.split("."):
        target = getattr(target, part, None)
    if not callable(target):
        raise ProviderError(f"Provider target is not callable: {spec}")
    return target

def compile_project(project: Project, provider: Callable | None = None) -> CompiledSite:
    result = (provider or load_provider())(project.request())
    if inspect.isawaitable(result):
        close = getattr(result, "close", None)
        if callable(close):
            close()
        raise ProviderError("Compiler provider must be synchronous")
    return validate_result(project, result)

def _ensure_json(value: Any, label: str) -> None:
    try:
        json.dumps(value, allow_nan=False, sort_keys=True)
    except (TypeError, ValueError, RecursionError) as error:
        raise ProviderError(f"{label} must be finite JSON data: {error}") from error

def validate_result(project: Project, value: Any) -> CompiledSite:
    if not isinstance(value, Mapping):
        raise ProviderError("Compiler provider must return a mapping")
    required = {"protocol", "version", "capability_declarations", "offline_report",
                "runtime_js", "pages", "application_data", "provenance", "notices"}
    if set(value) != required:
        raise ProviderError(f"Compiler response fields differ; missing={sorted(required-set(value))}, extra={sorted(set(value)-required)}")
    if value["protocol"] != PROTOCOL or type(value["version"]) is not int or value["version"] != PROTOCOL_VERSION:
        raise ProviderError("Unsupported compiler protocol or version")
    raw_declarations = value["capability_declarations"]
    if not isinstance(raw_declarations, list) or not all(isinstance(item, str) for item in raw_declarations):
        raise ProviderError("capability_declarations must be a list of strings")
    declarations = frozenset(raw_declarations)
    missing = sorted(REQUIRED_DECLARATIONS - declarations)
    if missing:
        raise ProviderError(f"Provider does not declare required integration capabilities: {', '.join(missing)}")
    report = value["offline_report"]
    if not isinstance(report, Mapping) or set(report) != {"compiler", "external_imports", "server_declarations"}:
        raise ProviderError("offline_report must contain compiler, external_imports, and server_declarations")
    if not isinstance(report["compiler"], str) or not report["compiler"]:
        raise ProviderError("offline_report.compiler must identify the reporting compiler")
    for name in ("external_imports", "server_declarations"):
        if not isinstance(report[name], list):
            raise ProviderError(f"offline_report.{name} must be a list")
        if report[name]:
            raise ProviderError(f"Offline compiler reported prohibited {name}: {report[name]}")
    runtime_js = value["runtime_js"]
    if not isinstance(runtime_js, str) or not runtime_js.strip():
        raise ProviderError("runtime_js must be a nonempty bundled browser program")
    raw_pages = value["pages"]
    if not isinstance(raw_pages, list):
        raise ProviderError("pages must be a list")
    pages = []
    for item in raw_pages:
        if not isinstance(item, Mapping) or set(item) != {"slug", "title", "source"}:
            raise ProviderError("Each page must contain exactly slug, title, and source")
        if not isinstance(item["slug"], str) or not isinstance(item["title"], str) or not item["title"].strip():
            raise ProviderError("Compiled page slug/title are invalid")
        _ensure_json(item["source"], f"Compiled page {item['slug']!r} source")
        pages.append(CompiledPage(item["slug"], item["title"].strip(), item["source"]))
    expected, actual = [page.slug for page in project.pages], [page.slug for page in pages]
    if actual != expected:
        raise ProviderError(f"Compiled page order/slugs differ: expected {expected}, received {actual}")
    try:
        envelope = DataEnvelope.from_mapping(value["application_data"],
            expected_site_id=project.site_id, expected_schema_version=project.schema_version)
    except EnvelopeError as error:
        raise ProviderError(f"Invalid initial application_data envelope: {error}") from error
    provenance = value["provenance"]
    if not isinstance(provenance, Mapping) or not provenance:
        raise ProviderError("provenance must be a nonempty mapping")
    _ensure_json(provenance, "provenance")
    _ensure_json(report, "offline_report")
    notices_raw = value["notices"]
    if not isinstance(notices_raw, list):
        raise ProviderError("notices must be a list")
    notices = []
    for notice in notices_raw:
        if (not isinstance(notice, Mapping) or set(notice) != {"name", "text"}
                or not all(isinstance(notice[key], str) and notice[key] for key in ("name", "text"))):
            raise ProviderError("Each notice must contain nonempty name and text")
        notices.append({"name": notice["name"], "text": notice["text"]})
    return CompiledSite(tuple(pages), runtime_js, envelope, declarations,
                        dict(report), dict(provenance), tuple(notices))
