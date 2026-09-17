"""Versioned envelope for the shared ``application_data`` branch.

The payload is opaque. Only an accepted Gramlot codec can preserve and validate
typed Bag semantics; this module validates the surrounding JSON shape.
"""
from __future__ import annotations
from dataclasses import dataclass
import json
import math
import re
from typing import Any, Mapping

FORMAT = "gramlot-standalone-application-data"
VERSION = 1
MAX_JSON_BYTES = 10_000_000
_TOKEN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")

class EnvelopeError(ValueError):
    """An application-data envelope is malformed or belongs elsewhere."""

def _json_value(value: Any) -> None:
    stack = [("application_data", value, 0)]
    seen: set[int] = set()
    while stack:
        path, item, depth = stack.pop()
        if depth > 256:
            raise EnvelopeError(f"{path} exceeds the maximum nesting depth")
        if item is None or isinstance(item, (str, bool, int)):
            continue
        if isinstance(item, float):
            if not math.isfinite(item):
                raise EnvelopeError(f"{path} contains a non-finite number")
            continue
        if isinstance(item, (list, dict)):
            identity = id(item)
            if identity in seen:
                raise EnvelopeError(f"{path} contains a repeated or cyclic container")
            seen.add(identity)
            if isinstance(item, list):
                stack.extend((f"{path}[{index}]", child, depth + 1)
                             for index, child in enumerate(item))
            else:
                for key, child in item.items():
                    if not isinstance(key, str):
                        raise EnvelopeError(f"{path} contains a non-string object key")
                    stack.append((f"{path}.{key}", child, depth + 1))
            continue
        raise EnvelopeError(f"{path} contains a non-JSON value of type {type(item).__name__}")

def _reject_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result = {}
    for key, value in pairs:
        if key in result:
            raise EnvelopeError(f"duplicate JSON object key: {key}")
        result[key] = value
    return result

@dataclass(frozen=True, slots=True)
class DataEnvelope:
    site_id: str
    schema_version: int
    codec: str
    codec_version: int
    application_data: Any

    def __post_init__(self) -> None:
        if not isinstance(self.site_id, str) or not _TOKEN.fullmatch(self.site_id):
            raise EnvelopeError("site_id must be a stable ASCII token")
        if isinstance(self.schema_version, bool) or not isinstance(self.schema_version, int) or self.schema_version < 1:
            raise EnvelopeError("schema_version must be a positive integer")
        if not isinstance(self.codec, str) or not _TOKEN.fullmatch(self.codec):
            raise EnvelopeError("codec must be a stable ASCII token")
        if isinstance(self.codec_version, bool) or not isinstance(self.codec_version, int) or self.codec_version < 1:
            raise EnvelopeError("codec_version must be a positive integer")
        _json_value(self.application_data)
        detached = json.loads(json.dumps(self.application_data, ensure_ascii=False, allow_nan=False))
        object.__setattr__(self, "application_data", detached)

    def as_dict(self) -> dict[str, Any]:
        return {"format": FORMAT, "version": VERSION, "site_id": self.site_id,
                "schema_version": self.schema_version,
                "codec": {"name": self.codec, "version": self.codec_version},
                "application_data": self.application_data}

    def dumps(self, *, pretty: bool = True) -> str:
        options: dict[str, Any] = {"ensure_ascii": False, "allow_nan": False, "sort_keys": True}
        if pretty:
            options["indent"] = 2
        return json.dumps(self.as_dict(), **options) + ("\n" if pretty else "")

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any], *, expected_site_id: str | None = None,
                     expected_schema_version: int | None = None,
                     expected_codec: str | None = None,
                     expected_codec_version: int | None = None) -> "DataEnvelope":
        if not isinstance(value, Mapping):
            raise EnvelopeError("data envelope must be a JSON object")
        fields = {"format", "version", "site_id", "schema_version", "codec", "application_data"}
        if set(value) != fields:
            raise EnvelopeError("data envelope fields do not match version 1")
        if value.get("format") != FORMAT or type(value.get("version")) is not int or value.get("version") != VERSION:
            raise EnvelopeError("unsupported application-data envelope format or version")
        codec = value.get("codec")
        if not isinstance(codec, Mapping) or set(codec) != {"name", "version"}:
            raise EnvelopeError("codec must contain exactly name and version")
        result = cls(value.get("site_id"), value.get("schema_version"), codec.get("name"),
                     codec.get("version"), value.get("application_data"))
        if expected_site_id is not None and result.site_id != expected_site_id:
            raise EnvelopeError("application data belongs to a different site")
        if expected_schema_version is not None and result.schema_version != expected_schema_version:
            raise EnvelopeError("application data uses a different site schema version")
        if expected_codec is not None and result.codec != expected_codec:
            raise EnvelopeError("application data uses a different typed Bag codec")
        if expected_codec_version is not None and result.codec_version != expected_codec_version:
            raise EnvelopeError("application data uses a different typed Bag codec version")
        return result

    @classmethod
    def loads(cls, text: str, **expected: Any) -> "DataEnvelope":
        if not isinstance(text, str):
            raise EnvelopeError("application data must be JSON text")
        if len(text.encode("utf-8")) > MAX_JSON_BYTES:
            raise EnvelopeError(f"application data exceeds {MAX_JSON_BYTES} bytes")
        try:
            value = json.loads(text, object_pairs_hook=_reject_duplicate_pairs)
        except (TypeError, json.JSONDecodeError, RecursionError) as error:
            raise EnvelopeError(f"invalid JSON: {error}") from error
        return cls.from_mapping(value, **expected)
