# faray-skill-agent

Automation toolkit — Twitter/X + Airdrop tracking + OAuth helper.

## Commands

### faray-twitter-tweet (Twitter/X)

| Command | Description |
|---------|-------------|
| `faray-twitter-tweet read <id>` | Read single tweet |
| `faray-twitter-tweet replies <id> [N]` | Read N replies |
| `faray-twitter-tweet thread <id>` | Get full thread |
| `faray-twitter-tweet profile <user> [N]` | Scrape N tweets from profile |
| `faray-twitter-tweet delete <id>` | Delete a tweet |
| `faray-twitter-tweet bookmarks [N]` | Read bookmarked tweets |
| `faray-twitter-tweet timeline [N]` | Read home timeline |
| `faray-twitter-tweet search <query> [N]` | Search tweets |

### faray-airdrop (Campaign Tracker)

| Command | Description |
|---------|-------------|
| `faray-airdrop add <name> [options]` | Add new campaign |
| `faray-airdrop list [status]` | List campaigns (filter: pending/submitted/verified/expired/failed) |
| `faray-airdrop show <id>` | Show campaign details |
| `faray-airdrop update <id> --field value` | Update a field |
| `faray-airdrop delete <id>` | Delete a campaign |
| `faray-airdrop stats` | Summary statistics |
| `faray-airdrop check-deadlines` | Campaigns expiring within 7 days |
| `faray-airdrop export` | Export all as JSON |

**Options:** `--chain`, `--wallet`, `--deadline`, `--requirements`, `--status`, `--url`, `--notes`

### faray-auth (OAuth Helper)

| Command | Description |
|---------|-------------|
| `faray-auth status` | Check if cookies are valid |
| `faray-auth oauth <url>` | Open campaign URL, handle X OAuth flow |
| `faray-auth sync-cookies` | Refresh cookies from live session |

All output JSON.

## Setup

```bash
pip install playwright
playwright install chromium
```

Export Twitter cookies from browser via Cookie-Editor → save to `~/.agent/credentials/x-cookies.json`.

Minimum cookies: `auth_token` + `ct0`.

## Install

```bash
cp scripts/faray-twitter-tweet /usr/local/bin/
cp scripts/faray-airdrop /usr/local/bin/
cp scripts/faray-auth /usr/local/bin/
chmod +x /usr/local/bin/faray-*
```

## License

MIT
