# Codex GPT Image Skill

[![中文](https://img.shields.io/badge/docs-中文-blue)](README.md) [![Skill](https://img.shields.io/badge/skill-codex--gpt--image-cd3b35)](skills/codex-gpt-image)

A `SKILL.md` image-generation skill for **OpenClaw, Claude Code, Codex, Hermes Agent**, and other skill-capable agents. It generates images with Codex OAuth / ChatGPT login, without requiring `OPENAI_API_KEY`.

The skill reads the local `~/.codex/auth.json` and calls the Codex Images backend at `https://chatgpt.com/backend-api/codex/images/generations` or `https://chatgpt.com/backend-api/codex/images/edits` so agents can reuse an existing Codex / ChatGPT subscription session.

## Install

Install into the current agent's global skills directory with the `skills` CLI:

```bash
npx -y skills@latest add ningzimu/codex-gpt-image \
  --global
```

This repository currently contains one skill: `codex-gpt-image`. Restart the current agent after installation.


## Prerequisites

The preferred path is an existing Codex login on the same machine:

```bash
codex login
test -f ~/.codex/auth.json
```

Override the auth file when needed:

```bash
export CODEX_AUTH_FILE=/path/to/auth.json
```

The device-code login fallback uses the same public OAuth client id as official Codex login tooling by default. Override it when needed:

```bash
export CODEX_APP_SERVER_LOGIN_CLIENT_ID=your-client-id
```

If the machine does not have Codex auth yet, use the bundled device-code login flow. It follows the official Codex device-code login flow: the CLI prints a browser URL and a short code, the user confirms in the browser, and the CLI writes access/refresh tokens to `~/.codex/auth.json`.

```bash
python3 skills/codex-gpt-image/scripts/codex_gpt_image.py login --open-browser
```

On remote servers or inside Claude Code, omit `--open-browser` and open the printed URL manually:

```bash
python3 skills/codex-gpt-image/scripts/codex_gpt_image.py login
```

## Usage

Supply a prompt directly or via `--prompt-file`. Reference images (repeatable) and transparency are optional. Use a separate invocation and PNG path for each asset.

```sh
python3 skills/codex-gpt-image/scripts/codex_gpt_image.py generate --prompt "A blue mug"
python3 skills/codex-gpt-image/scripts/codex_gpt_image.py generate --prompt "Make the mug green" --image mug.png --transparent-background --out edited.png
```

Default output is `output/codex-gpt-image/output.png`. Codex selects the model and may omit its ID in the response.

## License

MIT
