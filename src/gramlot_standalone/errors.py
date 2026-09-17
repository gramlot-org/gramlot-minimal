"""User-facing standalone build failures."""

class BuildError(Exception):
    """The requested artifact could not be built safely."""

class ProjectError(BuildError):
    """The source directory violates the project contract."""

class ProviderError(BuildError):
    """The Gramlot compiler/runtime provider is unavailable or invalid."""
