---
name: codex-gpt-image
description: Generate or edit images with GPT Image through Codex/ChatGPT subscription authentication instead of OPENAI_API_KEY. Use for text-to-image, reference-image editing, or visual assets when the user wants local Codex auth, especially when no native image tool is available. Do not use for official OpenAI API-key billing or OpenAI-compatible gateways.
---

# Codex GPT Image

Use this skill to generate or edit images through Codex OAuth instead of the OpenAI API-key path. The bundled CLI reads the local Codex auth file and calls the Codex Images backend endpoints.

## When To Use

- The user asks to use GPT Image through Codex auth/subscription.
- The current agent supports `SKILL.md` but does not have a native image tool.
- The user explicitly does not want to use `OPENAI_API_KEY`.
- The user wants the same local image workflow across Codex, Claude Code, OpenClaw, Hermes Agent, or similar agents.

Do not use this skill when the user wants the official OpenAI Images API, an OpenAI-compatible gateway, or API-key billing. This skill is deliberately Codex-OAuth-only.

## Core Workflow

All CLI commands below assume the working directory is this skill folder. Otherwise, resolve the absolute path to `scripts/codex_gpt_image.py` from this `SKILL.md`.

1. Check local Codex auth:

   ```bash
   python3 scripts/codex_gpt_image.py auth-status
   ```

2. If Codex auth is missing, run the device-code login flow:

   ```bash
   python3 scripts/codex_gpt_image.py login --open-browser
   ```

   The CLI prints a browser URL and a short user code. The user must complete this step; never ask them to paste tokens.

3. Generate an image with the user's actual prompt. Choose only the CLI flags required by the request, and do not reuse prompt wording from this skill.

4. Edit or use reference images by passing one or more `--image` inputs. For edits, build the prompt from the user's requested changes and the invariants that must stay unchanged.

5. Report the saved path(s), actual output size when inspected, and whether Codex OAuth was used. Do not claim the requested model was used unless the backend identifies it.

## Generate or edit

Supply exactly one of `--prompt` or `--prompt-file`. Describe composition, desired changes and details to preserve in the prompt. Pass local references in order with repeated `--image`. The host resolves images from the conversation to files. Include `--transparent-background` when transparency is requested. Omitted image and background fields stay absent from the request.

Save to a PNG with `--out`; the default is `output/codex-gpt-image/output.png`. For multiple assets, make separate calls with distinct paths. The backend selects the model. Report its identity only when returned.
