# faray-skill-agent

Twitter/X automation toolkit — cookie-based Playwright automation.

## Commands

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
chmod +x /usr/local/bin/faray-twitter-tweet
```

## License

MIT
