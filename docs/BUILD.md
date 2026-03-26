# Build and Release Guide (uv)

This document describes how to build, validate, and publish `tasmota-http` using `uv`.

## Prerequisites

- Python 3.10+
- `uv` installed and available in PATH
- Repository cloned locally

Check tools:

```bash
python3 --version
uv --version
```

## Build package artifacts

From the project root:

```bash
cd /mnt/NetworkBackupShare/api_doc/tasmota-http
uv build
```

Expected outputs in `dist/`:
- `tasmota_http-<version>.tar.gz` (source distribution)
- `tasmota_http-<version>-py3-none-any.whl` (wheel)

## Validate before release

### 1) Run tests

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

### 2) (Optional) Inspect built artifacts

```bash
ls -la dist/
```

## Release workflow (Git + tag)

Typical release steps:

```bash
# 1) Ensure clean tree
git status --short

# 2) Commit release-related changes (if any)
git add -A
git commit -m "Prepare release vX.Y.Z"

# 3) Push branch
git push

# 4) Create annotated tag
git tag -a vX.Y.Z -m "Release vX.Y.Z"

# 5) Push tag
git push origin vX.Y.Z
```

## Publish to PyPI (optional)

If you want to publish package artifacts from `dist/`:

```bash
uv publish dist/*
```

You need valid PyPI credentials/token configured in your environment.
