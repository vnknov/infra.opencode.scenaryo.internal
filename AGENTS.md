# AGENTS.md

## Repository State
- This is Docker Compose infrastructure for a remote devbox plus an OpenCode server behind Caddy, not an application repo.
- There are no verified lint, test, format, typecheck, package-manager, CI, or Terraform commands in this repo.
- `README.md` is only a title placeholder; trust `docker-compose.yml`, `Dockerfile`, `Caddyfile`, and `opencode.json` over prose.

## Runtime Layout
- `devbox` and `opencode` both build from `Dockerfile`; the image installs OpenCode, Node.js 20, Java 21, Maven, Python, SSH, and dev tools.
- `devbox` exposes SSH on host port `2222`; `opencode` exposes port `4096` only on the Compose network.
- `caddy` publishes host port `443` and reverse-proxies `opencode.scenaryo.internal` to `opencode:4096` with `tls internal`.
- `./workspace` is bind-mounted to `/home/dev/workspace`; `devbox-home` is shared by `devbox` and `opencode` so auth state persists across both.
- `opencode.json` is mounted into the container as `/home/dev/.config/opencode/opencode.json`.
- LM Studio is configured as provider `lmstudio` at `https://inference.scenaryo.internal/v1`; the container trusts it through `NODE_EXTRA_CA_CERTS=/certs/root-ca.crt`.

## Required Local Inputs
- Compose references ignored local paths: `.env`, `certs/root-ca.crt`, `keys/laptop.pub`, `keys/github/id_ed25519`, and `keys/github/id_ed25519.pub`.
- `.env` provides `OPEN_API_KEY`, `OPENCODE_SERVER_PASSWORD`, `OBSIDIAN_API_KEY`, `CHANNELS_MCP_TOKEN`, and `LM_STUDIO_TOKEN` for the configured services/MCP servers.
- Do not commit `certs/`, `keys/`, or `.env`; they are intentionally ignored.

## Commands
- Start or rebuild the stack with `docker compose up -d --build`.
- Check the rendered Compose config with `docker compose config` after editing `docker-compose.yml` or environment handling.
- Follow service logs with `docker compose logs -f opencode`, `docker compose logs -f devbox`, or `docker compose logs -f caddy`.

## Working Guidance
- If adding the first real test/lint/build workflow, update this file with exact commands and prerequisites.
- Be careful changing usernames, home paths, or volume names; Compose command blocks and mounts assume user `dev` and `/home/dev`.
