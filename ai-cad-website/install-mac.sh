#!/usr/bin/env bash
#
# MakeItOurs — Mac setup script
#
# Installs the command-line tools MakeItOurs needs to manage projects locally:
# git, Python 3.12 or 3.13, Homebrew, and OpenCode. Safe to re-run — each
# step checks what's already installed and skips it.
#
# Review this script before running it, then from Terminal:
#   chmod +x install-mac.sh
#   ./install-mac.sh
#
# Or run it directly:
#   curl -fsSL https://bengesoftwarellc.com/ai-cad-website/install-mac.sh | bash

set -euo pipefail

info() { printf '\n\033[1;34m==>\033[0m %s\n' "$1"; }
ok()   { printf '    \033[1;32m\xE2\x9C\x93\033[0m %s\n' "$1"; }
warn() { printf '    \033[1;33m!\033[0m %s\n' "$1"; }
fail() { printf '    \033[1;31m\xC3\x97\033[0m %s\n' "$1"; }

if [[ "$(uname)" != "Darwin" ]]; then
  echo "This script is for macOS only." >&2
  exit 1
fi

# --- macOS version --------------------------------------------------------

info "Checking macOS version"
os_version="$(sw_vers -productVersion)"
os_major="${os_version%%.*}"
if (( os_major >= 15 )); then
  ok "macOS $os_version"
else
  warn "macOS $os_version detected — MakeItOurs needs macOS 15 or newer."
  warn "Update from Apple menu > System Settings > General > Software Update"
  warn "or see https://support.apple.com/en-us/HT201475"
fi

# --- git --------------------------------------------------------------

info "Checking for git"
if command -v git >/dev/null 2>&1; then
  ok "git $(git --version | awk '{print $3}')"
else
  warn "git not found — triggering the Xcode Command Line Tools installer"
  xcode-select --install || true
  fail "Finish the installer popup, then re-run this script."
  exit 1
fi

# --- Homebrew --------------------------------------------------------------

info "Checking for Homebrew"
if command -v brew >/dev/null 2>&1; then
  ok "Homebrew $(brew --version | head -1 | awk '{print $2}')"
else
  info "Installing Homebrew (this will prompt for your password) — see https://brew.sh"
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  if [[ -x /opt/homebrew/bin/brew ]]; then
    eval "$(/opt/homebrew/bin/brew shellenv)"
  elif [[ -x /usr/local/bin/brew ]]; then
    eval "$(/usr/local/bin/brew shellenv)"
  else
    fail "Homebrew installed but not found on PATH — open a new Terminal tab and re-run this script."
    exit 1
  fi
fi

# --- Python 3.12 or 3.13 ---------------------------------------------------

info "Checking for Python 3.12 or 3.13"
python_ok=false
for py in python3.13 python3.12 python3; do
  if command -v "$py" >/dev/null 2>&1; then
    ver="$("$py" --version 2>&1 | awk '{print $2}')"
    case "$ver" in
      3.12.*|3.13.*)
        ok "$py $ver"
        python_ok=true
        break
        ;;
    esac
  fi
done
if ! $python_ok; then
  info "Installing Python 3.13 via Homebrew — see https://www.python.org/downloads/macos/"
  brew install python@3.13
fi

# --- OpenCode ----------------------------------------------------------

info "Checking for OpenCode"
if command -v opencode >/dev/null 2>&1; then
  ok "OpenCode $(opencode --version)"
else
  info "Installing OpenCode via Homebrew — see https://opencode.ai/docs/"
  brew install anomalyco/tap/opencode
fi

info "Done. MakeItOurs' Mac runtime dependencies are installed."
