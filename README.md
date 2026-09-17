# Gramlot Standalone

## Try the unified showcase

Download or copy [showcase.zip](showcase.zip), extract the whole archive and open
`showcase/index.html`. The original shared showcase shell and lessons are included,
with local runtime, Source viewer and Inspector. The RPC lesson reports that a
Python backend is unavailable; other lessons run locally. See
[offline showcase](docs/030-showcase.md) and [verification](examples/showcase/VERIFICATION.md).
This PoC-based directory export is separate from the pending generic single-file
compiler integration described below.

`gramlot-standalone` is the offline packaging layer for Python-authored Gramlot
projects. Its intended command is:

```console
gramlot-standalone build ./my-site -o my-site.html
```

This repository implements project discovery, input containment, local CSS/resource
embedding, deterministic single-file HTML assembly, a versioned `application_data`
envelope, provenance/notices, provider validation and atomic output. It does not
contain a replacement Gramlot runtime.

The clean core does not yet expose the compiler/runtime integration needed to turn
Python Pages into an offline browser application. Until the bounded ports in
[GS-015](docs/015-core-port-requirements.md) are accepted, the default command exits
with a precise missing-provider error and writes no HTML. The hidden explicit
provider option supports contract development only; it is a proposal, not a core API.

## Project layout

```text
my-site/
  pages/
    index.py
    reports.py
  style.css                 # optional bounded CSS subset
  styles/                   # optional additional CSS
  resources/                # optional local files embedded as data URLs
  gramlot-standalone.toml   # optional metadata
```

See [usage](docs/010-usage.md), [architecture and verified status](docs/005-architecture.md),
and [required core ports](docs/015-core-port-requirements.md).

## Development

```console
PYTHONPATH=src:tests python -m unittest discover -s tests -v
python -m build --no-isolation
```

The tests use a fixture provider which is not a Gramlot runtime or demo. No package
publication, release, remote repository, deployment, direct PDF generator, or
fillable PDF support is part of this work.
