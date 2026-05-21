#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
extensions_file="${repo_root}/.vscode/extensions.json"

if [[ ! -f "${extensions_file}" ]]; then
  echo "VS Code extensions file not found: ${extensions_file}" >&2
  exit 1
fi

code_cmd=""
for candidate in code code-insiders code-server; do
  if command -v "${candidate}" >/dev/null 2>&1; then
    code_cmd="${candidate}"
    break
  fi
done

if [[ -z "${code_cmd}" ]]; then
  echo "VS Code CLI was not found. Install the 'code' command and try again." >&2
  exit 1
fi

python_cmd=""
for candidate in python3 python; do
  if command -v "${candidate}" >/dev/null 2>&1; then
    python_cmd="${candidate}"
    break
  fi
done

if [[ -z "${python_cmd}" ]]; then
  echo "Python was not found. Python is required to read ${extensions_file}." >&2
  exit 1
fi

mapfile -t extensions < <(
  "${python_cmd}" - "${extensions_file}" <<'PY'
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
data = json.loads(path.read_text(encoding="utf-8"))
for extension in data.get("recommendations", []):
    print(extension)
PY
)

if [[ "${#extensions[@]}" -eq 0 ]]; then
  echo "No VS Code extension recommendations found."
  exit 0
fi

for extension in "${extensions[@]}"; do
  echo "Installing ${extension}..."
  "${code_cmd}" --install-extension "${extension}" --force
done

echo "VS Code extensions are installed."
