#!/usr/bin/env bash
# Create the GitHub repository and push the initial commit.
# Prerequisite: authenticate once with  ->  gh auth login
set -euo pipefail

REPO_NAME="reflex-charts"
VISIBILITY="--public"   # change to --private if you prefer

cd "$(dirname "$0")/.."

if ! gh auth status >/dev/null 2>&1; then
  echo "Not authenticated with gh. Run first:  gh auth login"
  exit 1
fi

# Create the repo under your account, use the current directory as source, push.
gh repo create "$REPO_NAME" $VISIBILITY \
  --source=. \
  --remote=origin \
  --description "Chart.js for Reflex — a pure-Python custom component wrapping react-chartjs-2" \
  --push

echo "Done: repository created and pushed."
gh repo view --web
