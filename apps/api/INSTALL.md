# Installation Instructions

## Step 1: Install stravavis from source

First, install the local stravavis package from the root directory:

```bash
# From the root of the project (strava_py/)
cd ../..  # Go to root
pip install -e .
```

This installs the `stravavis` package in editable mode.

## Step 2: Install API dependencies

Then install the API dependencies:

```bash
# From apps/api/
pip install -r requirements.txt
```

Or install in editable mode:

```bash
pip install -e .
```

## Alternative: Install everything at once

From the root directory:

```bash
# Install stravavis
pip install -e .

# Install API
pip install -e apps/api
```

## Verify installation

```bash
python -c "import stravavis; print('stravavis OK')"
python -c "import app; print('app OK')"
```


