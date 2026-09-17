"""Project discovery and local resource embedding."""
from __future__ import annotations
from dataclasses import dataclass
import base64
import hashlib
import mimetypes
from pathlib import Path
import re
import tomllib
from typing import Any
from .errors import ProjectError

_SLUG = re.compile(r"^[a-z][a-z0-9_-]*$")
_TOKEN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
_CSS_URL = re.compile(r"url\(\s*(['\"]?)([^)'\"]+)\1\s*\)", re.IGNORECASE)
_CSS_IMPORT = re.compile(r"@import\b", re.IGNORECASE)

@dataclass(frozen=True, slots=True)
class PageSource:
    slug: str
    path: Path
    sha256: str

@dataclass(frozen=True, slots=True)
class Resource:
    name: str
    media_type: str
    sha256: str
    data_url: str

@dataclass(frozen=True, slots=True)
class Project:
    root: Path
    site_id: str
    title: str
    schema_version: int
    initial_page: str
    pages: tuple[PageSource, ...]
    css: str
    resources: tuple[Resource, ...]

    @classmethod
    def load(cls, directory: str | Path) -> "Project":
        root = Path(directory).expanduser().resolve()
        if not root.is_dir():
            raise ProjectError(f"Project directory not found: {root}")
        config = _read_config(root)
        pages_dir = root / "pages"
        if not pages_dir.is_dir():
            raise ProjectError(f"Pages directory not found: {pages_dir}")
        pages_dir = _contained(pages_dir, root, "Pages directory")
        pages = []
        for path in sorted(pages_dir.glob("*.py")):
            if path.name.startswith("_"):
                continue
            resolved = _contained(path, pages_dir, "Page")
            if not resolved.is_file():
                continue
            if not _SLUG.fullmatch(path.stem):
                raise ProjectError(f"Invalid page filename: {path.name}")
            raw = resolved.read_bytes()
            pages.append(PageSource(path.stem, resolved, hashlib.sha256(raw).hexdigest()))
        if not pages:
            raise ProjectError(f"No public Python pages found in {pages_dir}")
        site = config.get("site", {})
        if not isinstance(site, dict):
            raise ProjectError("[site] must be a TOML table")
        unknown = set(site) - {"id", "title", "schema_version", "initial_page"}
        if unknown:
            raise ProjectError(f"Unknown [site] keys: {', '.join(sorted(unknown))}")
        site_id = site.get("id", root.name)
        title = site.get("title", root.name.replace("-", " ").replace("_", " ").title())
        schema_version = site.get("schema_version", 1)
        slugs = [page.slug for page in pages]
        initial_page = site.get("initial_page", "index" if "index" in slugs else slugs[0])
        if not isinstance(site_id, str) or not _TOKEN.fullmatch(site_id):
            raise ProjectError("site.id must be a stable ASCII token")
        if not isinstance(title, str) or not title.strip():
            raise ProjectError("site.title must be a nonempty string")
        if isinstance(schema_version, bool) or not isinstance(schema_version, int) or schema_version < 1:
            raise ProjectError("site.schema_version must be a positive integer")
        if not isinstance(initial_page, str) or initial_page not in set(slugs):
            raise ProjectError("site.initial_page must be a discovered page slug")
        resources = _resources(root)
        css = _styles(root, {resource.name: resource for resource in resources})
        return cls(root, site_id, title.strip(), schema_version, initial_page,
                   tuple(pages), css, tuple(resources))

    def request(self) -> dict[str, Any]:
        """Return the proposed provider request without executing Page modules."""
        return {"protocol": "gramlot-standalone-compiler", "version": 1,
                "project": {"root": str(self.root), "site_id": self.site_id,
                "title": self.title, "schema_version": self.schema_version,
                "initial_page": self.initial_page,
                "pages": [{"slug": page.slug, "path": str(page.path), "sha256": page.sha256}
                          for page in self.pages],
                "resources": [{"name": item.name, "media_type": item.media_type,
                               "sha256": item.sha256, "data_url": item.data_url}
                              for item in self.resources]}}

def _contained(path: Path, parent: Path, kind: str) -> Path:
    try:
        resolved = path.resolve(strict=True)
    except OSError as error:
        raise ProjectError(f"Cannot resolve {kind.lower()} path {path}: {error}") from error
    if not resolved.is_relative_to(parent.resolve()):
        raise ProjectError(f"{kind} path escapes its project directory: {path}")
    return resolved

def _read_config(root: Path) -> dict[str, Any]:
    path = root / "gramlot-standalone.toml"
    if not path.exists():
        return {}
    resolved = _contained(path, root, "Configuration")
    try:
        value = tomllib.loads(resolved.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, tomllib.TOMLDecodeError) as error:
        raise ProjectError(f"Cannot read {path}: {error}") from error
    unknown = set(value) - {"site"}
    if unknown:
        raise ProjectError(f"Unknown configuration tables: {', '.join(sorted(unknown))}")
    return value

def _resources(root: Path) -> list[Resource]:
    directory = root / "resources"
    if not directory.exists():
        return []
    if not directory.is_dir():
        raise ProjectError(f"Resources path is not a directory: {directory}")
    directory = _contained(directory, root, "Resources directory")
    result = []
    for path in sorted(item for item in directory.rglob("*") if item.is_file()):
        resolved = _contained(path, directory, "Resource")
        raw = resolved.read_bytes()
        media_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        result.append(Resource(path.relative_to(root).as_posix(), media_type,
                               hashlib.sha256(raw).hexdigest(),
                               f"data:{media_type};base64,{base64.b64encode(raw).decode('ascii')}"))
    return result

def _styles(root: Path, resources: dict[str, Resource]) -> str:
    paths = []
    primary = root / "style.css"
    if primary.exists():
        paths.append(primary)
    directory = root / "styles"
    if directory.exists():
        if not directory.is_dir():
            raise ProjectError(f"Styles path is not a directory: {directory}")
        directory = _contained(directory, root, "Styles directory")
        paths.extend(sorted(item for item in directory.rglob("*.css") if item.is_file()))
    chunks = []
    for path in paths:
        resolved = _contained(path, root, "Stylesheet")
        try:
            text = resolved.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            raise ProjectError(f"Cannot read stylesheet {path}: {error}") from error
        if re.search(r"</style", text, re.IGNORECASE):
            raise ProjectError(f"CSS contains an HTML style terminator: {path}")
        if "\\" in text:
            raise ProjectError(f"CSS escapes are outside the supported offline subset: {path}")
        if _CSS_IMPORT.search(text):
            raise ProjectError(f"CSS @import is not supported; inline it explicitly: {path}")
        def replace(match: re.Match[str]) -> str:
            value = match.group(2).strip()
            if value.startswith(("data:", "#")):
                return match.group(0)
            if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", value) or value.startswith("//"):
                raise ProjectError(f"Remote CSS resource is not offline-safe in {path}: {value}")
            if "?" in value:
                raise ProjectError(f"CSS resource query strings are not supported in {path}: {value}")
            marker = value.find("#")
            marker = len(value) if marker < 0 else marker
            clean, suffix = value[:marker], value[marker:]
            if not clean:
                return match.group(0)
            target = (resolved.parent / clean).resolve()
            if not target.is_relative_to(root):
                raise ProjectError(f"CSS resource escapes project directory in {path}: {value}")
            key = target.relative_to(root).as_posix()
            resource = resources.get(key)
            if resource is None:
                raise ProjectError(f"CSS resource must be under resources/: {value} in {path}")
            return f'url("{resource.data_url}{suffix}")'
        chunks.append(_CSS_URL.sub(replace, text).strip() + "\n")
    return "\n".join(chunks)
