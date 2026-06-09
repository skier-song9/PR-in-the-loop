#!/usr/bin/env sh
set -eu

if root="$(git rev-parse --show-toplevel 2>/dev/null)"; then
  in_git_repo=1
else
  root="$(pwd -P)"
  in_git_repo=0
fi

gitignore="$root/.gitignore"
memory_dir="$root/.memory/open-issue"
memory_file=".memory/open-issue/work-context.md"

mkdir -p "$memory_dir"

if [ ! -f "$gitignore" ]; then
  printf ".memory/\n" > "$gitignore"
else
  if ! grep -Eq '^[[:space:]]*/?\.memory(/|\*\*)?[[:space:]]*(#.*)?$' "$gitignore"; then
    if [ -s "$gitignore" ] && [ "$(tail -c 1 "$gitignore" | wc -l | tr -d ' ')" = "0" ]; then
      printf "\n" >> "$gitignore"
    fi
    printf ".memory/\n" >> "$gitignore"
  fi
fi

if [ "$in_git_repo" -eq 1 ]; then
  if ! git -C "$root" check-ignore -q "$memory_file"; then
    printf "error: %s is still not ignored by git\n" "$memory_file" >&2
    printf "check .gitignore negation rules and rerun this script\n" >&2
    exit 1
  fi
fi

printf "ok: .memory/ is ignored by git\n"
