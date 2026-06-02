# faray-skill-agent

Multi-tool automation toolkit for agents. Twitter, crypto, web scraping, GitHub, system monitoring — all CLI-based, JSON output.

## Tools

### 🐦 `faras-twitter-tweet` — Twitter/X Automation

Cookie-based Playwright automation for Twitter/X.

| Command | Description |
|---------|-------------|
| `read <id>` | Read single tweet (text, author, engagement, quoted tweet) |
| `replies <id> [N]` | Read N replies to a tweet |
| `thread <id>` | Get full conversation thread |
| `profile <user> [N]` | Scrape N recent tweets from a profile |
| `delete <id>` | Delete a tweet |
| `bookmarks [N]` | Read N bookmarked tweets |
| `timeline [N]` | Read home timeline |
| `search <query> [N]` | Search tweets |

### 🌐 `faras-scrape` — Universal Web Scraper

Playwright-based web scraper with multiple extraction modes.

| Command | Description |
|---------|-------------|
| `text <url>` | Extract text from page |
| `links <url>` | Extract all links |
| `table <url>` | Extract table data as JSON |
| `meta <url>` | Extract Open Graph + meta tags |
| `forms <url>` | Extract form fields |
| `screenshot <url>` | Take screenshot |
| `url <url> --attr href` | Extract specific attributes |

### 💰 `faras-crypto` — Crypto/Web3 Toolkit

Wallet balance, token info, gas prices — no API keys needed.

| Command | Description |
|---------|-------------|
| `balance <address> [--chain X]` | Wallet balance (ETH/SOL/BNB/MATIC/ARB) |
| `gas [--chain X]` | Current gas prices |
| `price <coin_id>` | CoinGecko price lookup |
| `ens <name>` | Resolve ENS name |
| `portfolio <address>` | Full portfolio with USD value |

### 🐙 `faras-gh` — GitHub Operations

Thin wrapper around `gh` CLI — passes args through directly.

| Command | Description |
|---------|-------------|
| `repo list -L 5` | List repos |
| `repo create <name>` | Create repo |
| `pr list <repo> -s open` | List PRs |
| `pr create <repo> -t "..." -b "..."` | Create PR |
| `issue list <repo>` | List issues |
| `issue create <repo> -t "..." -b "..."` | Create issue |
| `search repos <query>` | Search repos |
| `file <repo> <path>` | Read file from repo |

### 📊 `faras-monitor` — VPS/System Monitor

System health: disk, memory, CPU, Docker, network, processes.

| Command | Description |
|---------|-------------|
| `overview` | Full system snapshot |
| `disk [--warn 80]` | Disk usage with warnings |
| `memory` | Memory + swap + top processes |
| `cpu [--top 10]` | CPU usage + top processes |
| `docker` | Docker containers + images |
| `ports` | Listening ports |
| `network` | Public IP + connections |
| `services` | Systemd services |

### 🔍 `faras-research` — Web Research (Exa API)

Deep web research via Exa API. **Requires `EXA_API_KEY`.**

| Command | Description |
|---------|-------------|
| `search <query>` | Web search |
| `extract <url>` | Extract full page content |
| `extract-multi <url1> <url2>` | Batch extract |
| `find-similar <url>` | Find similar pages |
| `research <query> --depth full` | Deep research (search + extract) |

## Setup

### Prerequisites

```bash
# Python 3.10+
pip install playwright
playwright install chromium

# GitHub CLI (for faras-gh)
# https://cli.github.com/

# Twitter cookies (for faras-twitter-tweet)
# Export from browser → ~/.agent/credentials/x-cookies.json
```

### Install All Scripts

```bash
# Copy to PATH
cp scripts/* /usr/local/bin/
chmod +x /usr/local/bin/faras-*

# Or install from repo
git clone https://github.com/aldifhr/faray-skill-agent.git
cd faray-skill-agent
cp scripts/* /usr/local/bin/
```

### Cookie Setup (Twitter)

1. Install [Cookie-Editor](https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicbahaaabklfkp)
2. Login to x.com → Cookie-Editor → Export → JSON
3. Save to `~/.agent/credentials/x-cookies.json`

Minimum cookies: `auth_token` + `ct0`.

### API Keys (Optional)

```bash
# Exa API (for faras-research)
export EXA_API_KEY=your_key_here
```

## Examples

```bash
# Twitter: read a tweet
faras-twitter-tweet read https://x.com/user/status/123456

# Scraper: extract page meta
faras-scrape meta https://example.com

# Crypto: check wallet balance
faras-crypto balance 0x854db5c41419a42967de4ec6a47c011b28b227eb

# Crypto: Solana balance
faras-crypto balance 5ZuFVHf6fod9w5geD9jihGNrgLPyyczBPaigr9hi4W59 --chain solana

# Crypto: BTC price
faras-crypto price bitcoin

# GitHub: list repos
faras-gh repo list -L 5

# GitHub: search repos
faras-gh search repos "playwright automation" -L 5

# Monitor: system overview
faras-monitor overview

# Monitor: disk warnings
faras-monitor disk --warn 80

# Monitor: Docker status
faras-monitor docker
```

## Output Format

All tools output JSON to stdout. Pipe to `jq` for filtering:

```bash
faras-monitor overview | jq '.memory'
faras-crypto balance 0x... | jq '.usd_value'
faras-gh repo list -L 5 | jq '.[].name'
```

## Architecture

```
scripts/
├── faras-twitter-tweet   # Twitter/X automation (Playwright)
├── faras-scrape          # Web scraping (Playwright)
├── faras-crypto          # Crypto toolkit (RPC + APIs)
├── faras-gh              # GitHub ops (gh CLI wrapper)
├── faras-monitor         # System monitor (shell commands)
└── faras-research        # Web research (Exa API)
src/
└── faras_twitter.py      # Base Twitter Playwright library
```

## How It Works

- **Twitter/Scraper**: Playwright headless Chromium → automates real browser UI → parses DOM by `data-testid`
- **Crypto**: Public RPCs (Ankr, Solana) + CoinGecko API — no API keys needed
- **GitHub**: Thin wrapper around `gh` CLI
- **Monitor**: Shell commands (`df`, `free`, `ps`, `ss`, `docker`)
- **Research**: Exa API (requires API key)

## Requirements

| Tool | Requirements |
|------|-------------|
| faras-twitter-tweet | Playwright + Twitter cookies |
| faras-scrape | Playwright |
| faras-crypto | Python stdlib only |
| faras-gh | gh CLI |
| faras-monitor | Python stdlib only |
| faras-research | EXA_API_KEY |

## License

MIT
