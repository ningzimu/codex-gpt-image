# OpenAI Images API And Codex Request Reference

This reference summarizes the official OpenAI Images API fields used by this skill and the Codex OAuth request shape used to reach the Codex Images backend.
Treat the linked OpenAI documentation as the source of truth when behavior changes:

- Create image: https://developers.openai.com/api/reference/resources/images/methods/generate
- Create image edit: https://developers.openai.com/api/reference/resources/images/methods/edit
- Image generation guide: https://developers.openai.com/api/docs/guides/image-generation
- GPT Image 2.6 Flare: https://developers.openai.com/api/docs/models/gpt-image-2.6-flare
- GPT Image 2.6 Sunburst: https://developers.openai.com/api/docs/models/gpt-image-2.6-sunburst

## Codex Request Shape

This skill uses Codex OAuth with Codex backend equivalents of the public Images API.

Codex backend endpoints:

```text
POST https://chatgpt.com/backend-api/codex/images/generations
POST https://chatgpt.com/backend-api/codex/images/edits
```

Public OpenAI API equivalents:

```text
POST https://api.openai.com/v1/images/generations
POST https://api.openai.com/v1/images/edits
```

Request headers:

| Header | Source / rule |
| --- | --- |
| `Authorization` | `Bearer <access token from ~/.codex/auth.json>` |
| `Accept` | `application/json` |
| `Content-Type` | `application/json` |
| `originator` | Skill originator string |
| `User-Agent` | Skill user-agent string |
| `ChatGPT-Account-ID` | Included only when an account id is available from Codex auth |

Both endpoints require a prompt. Edit requests also include an ordered `images` array of base64 data URL references. Both endpoints omit `background` unless the caller supplies `--transparent-background`, which sends `transparent`. The backend selects the model. Output files must contain PNG data.

## Device-Code Login

When `~/.codex/auth.json` is missing, the script can run the OpenAI Codex device-code login flow:

1. Resolve the OAuth client id from `--client-id`, then `CODEX_APP_SERVER_LOGIN_CLIENT_ID`, then the public Codex default.
2. `POST https://auth.openai.com/api/accounts/deviceauth/usercode`
3. Show `https://auth.openai.com/codex/device` and the returned user code.
4. Poll `POST https://auth.openai.com/api/accounts/deviceauth/token`.
5. Exchange the returned authorization code at `POST https://auth.openai.com/oauth/token`.
6. Save `access_token` and `refresh_token` into `~/.codex/auth.json`.

The default client id is the public Codex OAuth client id used by official Codex login tooling. It is not a secret.
