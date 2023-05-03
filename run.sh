#!/bin/bash
set -euo pipefail
cd "${0%/*}"
exec pipenv run uvicorn todos:app --reload --reload-dir=todos --reload-include='todos/*'
