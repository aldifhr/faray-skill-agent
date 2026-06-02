# faray-skill-agent

Twitter/X automation toolkit — cookie-based Playwright automation.

## Commands

| Command | Description |
|---------|-------------|
| `faras-twitter-tweet read <id>` | Read single tweet |
| `faras-twitter-tweet replies <id> [N]` | Read N replies |
| `faras-twitter-tweet thread <id>` | Get full thread |
| `faras-twitter-tweet profile <user> [N]` | Scrape N tweets from profile |
| `faras-twitter-tweet delete <id>` | Delete a tweet |
| `faras-twitter-tweet bookmarks [N]` | Read bookmarked tweets |
| `faras-twitter-tweet timeline [N]` | Read home timeline |
| `faras-twitter-tweet search <query> [N]` | Search tweets |

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
cp scripts/faras-twitter-tweet /usr/local/bin/
chmod +x /usr/local/bin/faras-twitter-tweet
```

## License

MIT
