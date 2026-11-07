# Codex GPT Image Skill

[![English](https://img.shields.io/badge/docs-English-blue)](README_en.md) [![Skill](https://img.shields.io/badge/skill-codex--gpt--image-cd3b35)](skills/codex-gpt-image)

一个面向 **OpenClaw / Claude Code / Codex / Hermes Agent** 的 `SKILL.md` 生图 skill：通过 **Codex OAuth / ChatGPT 登录态** 生成或编辑 PNG 图片，不需要 `OPENAI_API_KEY`。

它读取本机 `~/.codex/auth.json`，请求 Codex Images 后端 `https://chatgpt.com/backend-api/codex/images/generations` 或 `https://chatgpt.com/backend-api/codex/images/edits`，让 agent 复用已有 Codex / ChatGPT 订阅权限生成图片。

## 目录结构

```text
codex-gpt-image/
├── README.md
├── README_en.md
├── LICENSE
├── CHANGELOG.md
├── AGENTS.md
└── skills/
    └── codex-gpt-image/
        ├── SKILL.md
        ├── references/
        │   └── openai-images-api-parameters.md
        └── scripts/
            └── codex_gpt_image.py
```

## 安装

推荐使用 `skills` CLI 一次安装到当前 agent 的全局 skills 目录：

```bash
npx -y skills@latest add ningzimu/codex-gpt-image \
  --global
```

这个仓库目前只包含 `codex-gpt-image` 一个 skill。安装完成后，重启当前 agent 让新 skill 生效。


本地开发时可以用软链接：

```bash
mkdir -p ~/.codex/skills
ln -s /path/to/codex-gpt-image/skills/codex-gpt-image ~/.codex/skills/codex-gpt-image
```

## 前置条件

首选路径是本机已经登录 Codex，并存在可读的 Codex OAuth 文件：

```bash
codex login
test -f ~/.codex/auth.json
```

这个 skill 不读取也不需要 `OPENAI_API_KEY`。如果你想指定另一个 Codex auth 文件：

```bash
export CODEX_AUTH_FILE=/path/to/auth.json
```

device-code 登录 fallback 默认使用官方 Codex 登录工具同一个公开 OAuth client id；如需覆盖：

```bash
export CODEX_APP_SERVER_LOGIN_CLIENT_ID=your-client-id
```

如果机器上还没有 Codex 登录态，也可以直接用本 skill 的 device-code 登录流程。它参考官方 Codex device-code 登录流程：先生成浏览器 URL 和短 code，用户在浏览器中确认后，脚本把 access/refresh token 写入 `~/.codex/auth.json`。

```bash
python3 skills/codex-gpt-image/scripts/codex_gpt_image.py login --open-browser
```

在远程服务器或 Claude Code 终端里，可以不加 `--open-browser`，手动复制 URL 到本地浏览器：

```bash
python3 skills/codex-gpt-image/scripts/codex_gpt_image.py login
```

## 使用方式

通过 `--prompt` 或 `--prompt-file` 提供提示词，二选一。其余参数均可选。

- 省略 `--image` 时，CLI 调用 `/images/generations`。传入一张或多张参考图时，CLI 调用 `/images/edits`。每张图用一个 `--image`，顺序与命令行一致。
- 加上 `--transparent-background` 会请求透明 PNG。省略时由后端决定背景，结果也可能透明。
- 用 `generate --help` 查看全部选项。用 `--dry-run` 可在发送前查看所选接口和请求字段。

```sh
python3 skills/codex-gpt-image/scripts/codex_gpt_image.py generate --prompt "A blue mug"
python3 skills/codex-gpt-image/scripts/codex_gpt_image.py generate --prompt "Make the mug green" --image mug.png --transparent-background --out edited.png
```

默认输出 `output/codex-gpt-image/output.png`。模型由 Codex 后端选择，响应可能省略模型 ID。

## 许可证

MIT
