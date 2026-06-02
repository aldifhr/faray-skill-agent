# faray-skill-agent

Twitter/X automation toolkit — cookie-based Playwright automation for agents.

## Features

| Command | Description |
|---------|-------------|
| `faras-twitter-tweet read <id>` | Read single tweet (text, author, engagement, quoted tweet) |
| `faras-twitter-tweet replies <id> [N]` | Read N replies to a tweet |
| `faras-twitter-tweet thread <id>` | Get full conversation thread |
| `faras-twitter-tweet profile <user> [N]` | Scrape N recent tweets from a profile |
| `faras-twitter-tweet delete <id>` | Delete a tweet |
| `faras-twitter-tweet bookmarks [N]` | Read N bookmarked tweets |
| `faras-twitter-tweet timeline [N]` | Read home timeline |
| `faras-twitter-tweet search <query> [N]` | Search tweets |

## Requirements

- Python 3.10+
- Playwright (`pip install playwright && playwright install chromium`)
- Twitter/X browser cookies exported as JSON

## Setup

### 1. Export Cookies

1. Install [Cookie-Editor](https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicbahaaabklfkp) extension
2. Login to [x.com](https://x.com) in your browser
3. Cookie-Editor → Export → JSON
4. Save to `~/.agent/credentials/x-cookies.json`

### 2. Cookie Format

Supports two formats:

**Format A — Cookie-Editor array:**
```json
[
  {"domain": ".x.com", "name": "auth_token", "value": "..."},
  {"domain": ".x.com", "name": "ct0", "value": "..."}
]
```

**Format B — Dict:**
```json
{
  "cookies": {
    "auth_token": "...",
    "ct0": "..."
  }
}
```

Minimum required: `auth_token` + `ct0`.

### 3. Install

```bash
# Copy script to PATH
cp scripts/faras-twitter-tweet /usr/local/bin/
chmod +x /usr/local/bin/faras-twitter-tweet

# Install dependencies
pip install playwright
playwright install chromium
```

## Usage Examples

```bash
# Read a tweet
faras-twitter-tweet read 2061681372218233324
faras-twitter-tweet read https://x.com/faraybless/status/2061681372218233324

# Read 5 replies
faras-twitter-tweet replies 2059363078450315727 5

# Get full thread
faras-twitter-tweet thread 2059363078450315727

# Scrape profile (10 recent tweets)
faras-twitter-tweet profile kaomojinft 10

# Search tweets
faras-twitter-tweet search "WL NFT free" 5

# Read bookmarks
faras-twitter-tweet bookmarks 10

# Delete a tweet
faras-twitter-tweet delete <tweet_id>
```

## Output

All commands output JSON to stdout:

```json
{
  "tweet_id": "2061681372218233324",
  "author_name": "Faraay",
  "author_handle": "@faraybless",
  "text": "LFG",
  "time": "2026-06-02T05:28:37.000Z",
  "replies": "0 Replies. Reply",
  "retweets": "0 reposts. Repost",
  "likes": "0 Likes. Like",
  "quoted_tweet": {
    "author": "@flxeth",
    "text": "Claim your Free Mint spot..."
  }
}
```

## Architecture

- **`scripts/faras-twitter-tweet`** — Multi-command CLI (read, replies, thread, profile, delete, bookmarks, timeline, search)
- **`src/faras_twitter.py`** — Base Playwright automation library (post, like, retweet, follow, etc.)

## How It Works

1. Loads browser cookies from `~/.agent/credentials/x-cookies.json`
2. Launches headless Chromium via Playwright
3. Navigates to X.com pages directly (no API calls)
4. Parses DOM elements by `data-testid` attributes
5. Returns structured JSON

## Known Limitations

- Quote retweets: **broken** via Playwright (X anti-bot overlay intercepts post button)
- Replies: **broken** via Playwright (same anti-bot overlay issue)
- Profile scraping shows retweets mixed with own tweets
- Virtual scrolling: only visible tweets are in DOM during scroll

## License

MIT
