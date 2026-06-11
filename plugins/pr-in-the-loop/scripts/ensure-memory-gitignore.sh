#!/usr/bin/env sh
set -eu

if root="$(git rev-parse --show-toplevel 2>/dev/null)"; then
  in_git_repo=1
else
  root="$(pwd -P)"
  in_git_repo=0
fi

gitignore="$root/.gitignore"
open_issue_memory_dir="$root/.memory/open-issue"
planning_pr_memory_dir="$root/.memory/planning-pr"
specs_memory_dir="$root/.memory/specs"
open_issue_memory_file=".memory/open-issue/work-context.md"
planning_pr_memory_file=".memory/planning-pr/work-context.md"
specs_memory_file=".memory/specs/example.md"

mkdir -p "$open_issue_memory_dir" "$planning_pr_memory_dir" "$specs_memory_dir"

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
  for memory_file in "$open_issue_memory_file" "$planning_pr_memory_file" "$specs_memory_file"; do
    if ! git -C "$root" check-ignore -q "$memory_file"; then
      printf "error: %s is still not ignored by git\n" "$memory_file" >&2
      printf "check .gitignore negation rules and rerun this script\n" >&2
      exit 1
    fi
  done
fi

printf "ok: .memory/ is ignored by git\n"
