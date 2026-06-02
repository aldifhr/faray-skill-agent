#!/usr/bin/python3
"""
Faras Twitter CLI — cookie-based Twitter/X client (Playwright backend)
Usage: faray-twitter <command> [args]

Commands:
  whoami                        Show authenticated user info
  tweet <text>                  Post a tweet
  reply <tweet_id> <text>       Reply to a tweet
  search <query> [count]        Search tweets (default: 10)
  like <tweet_id>               Like a tweet
  unlike <tweet_id>             Unlike a tweet
  retweet <tweet_id>            Retweet
  follow <username>             Follow a user
  unfollow <username>           Unfollow a user
  timeline [count]              Home timeline (default: 10)
  user <username>               User info

Credential: ~/.agent/credentials/x-cookies.json
"""

import asyncio
import json
import sys
import time
from pathlib import Path

COOKIES_PATH = Path.home() / ".agent" / "credentials" / "x-cookies.json"


def load_cookies():
    if not COOKIES_PATH.exists() or COOKIES_PATH.stat().st_size == 0:
        print(json.dumps({"error": "Cookies file empty or missing."}))
        sys.exit(1)
    with open(COOKIES_PATH) as f:
        data = json.load(f)

    # Support both formats: dict with "cookies" key, or array of objects
    if isinstance(data, dict) and "cookies" in data:
        raw = data["cookies"]
    elif isinstance(data, list):
        raw = {c["name"]: c["value"] for c in data}
    else:
        raw = data

    # Convert to Playwright cookie format
    cookies = []
    for name, value in raw.items():
        cookies.append({
            "name": name,
            "value": value,
            "domain": ".x.com",
            "path": "/",
            "secure": True,
            "httpOnly": name in ("auth_token", "auth_multi", "kdt"),
        })
    return cookies


def run_playwright(func_name, *args):
    """Run a Playwright action synchronously."""
    from playwright.sync_api import sync_playwright

    cookies = load_cookies()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        context.add_cookies(cookies)

        try:
            result = globals()[f"_pw_{func_name}"](context, *args)
        except Exception as e:
            result = {"error": str(e)}
        finally:
            browser.close()

    print(json.dumps(result, ensure_ascii=False, indent=2))


def _pw_whoami(context):
    page = context.new_page()
    page.goto("https://x.com/home", timeout=30000)
    page.wait_for_timeout(4000)

    # Get profile link from nav
    profile_link = page.query_selector('[data-testid="AppTabBar_Profile_Link"]')
    if not profile_link:
        return {"error": "Not logged in"}

    href = profile_link.get_attribute("href") or ""
    username = href.strip("/")

    # Navigate to profile for more info
    page.goto(f"https://x.com/{username}", timeout=30000)
    page.wait_for_timeout(3000)

    # Get display name
    name_el = page.query_selector('[data-testid="UserName"] span')
    display_name = name_el.inner_text() if name_el else username

    # Get stats
    stats = page.query_selector_all('[data-testid="UserJoinDate"] ~ a span, [data-testid="UserJoinDate"] ~ div span')
    followers = following = "N/A"

    # Try to get follower/following from the page
    body_text = page.inner_text('body')
    for part in body_text.split('\n'):
        if 'Followers' in part:
            followers = part.split('Followers')[0].strip().split()[-1] if part.strip() else "N/A"
        if 'Following' in part:
            following = part.split('Following')[0].strip().split()[-1] if part.strip() else "N/A"

    return {
        "username": username,
        "name": display_name,
        "followers": followers,
        "following": following,
    }


def _pw_tweet(context, text):
    page = context.new_page()
    page.goto("https://x.com/compose/post", timeout=30000)
    page.wait_for_timeout(3000)

    textbox = page.query_selector('[data-testid="tweetTextarea_0"]')
    if not textbox:
        return {"error": "Text area not found"}

    textbox.click()
    textbox.fill(text)
    time.sleep(1)

    post_btn = page.query_selector('[data-testid="tweetButton"]')
    if not post_btn:
        return {"error": "Post button not found"}

    post_btn.click()
    page.wait_for_timeout(5000)

    return {"status": "posted", "text": text}


def _pw_reply(context, tweet_id, text):
    page = context.new_page()
    page.goto(f"https://x.com/i/web/status/{tweet_id}", timeout=30000)
    page.wait_for_timeout(3000)

    # Click reply button
    reply_btn = page.query_selector('[data-testid="reply"]')
    if reply_btn:
        reply_btn.click()
        page.wait_for_timeout(2000)

    textbox = page.query_selector('[data-testid="tweetTextarea_0"]')
    if textbox:
        textbox.click()
        textbox.fill(text)
        time.sleep(1)

        post_btn = page.query_selector('[data-testid="tweetButton"]')
        if post_btn:
            post_btn.click()
            page.wait_for_timeout(5000)
            return {"status": "replied", "reply_to": tweet_id, "text": text}

    return {"error": "Reply failed"}


def _pw_like(context, tweet_id):
    page = context.new_page()
    page.goto(f"https://x.com/i/web/status/{tweet_id}", timeout=30000)
    page.wait_for_timeout(3000)

    like_btn = page.query_selector('[data-testid="like"]')
    if like_btn:
        like_btn.click()
        time.sleep(1)
        return {"status": "liked", "tweet_id": tweet_id}
    return {"error": "Like button not found"}


def _pw_unlike(context, tweet_id):
    page = context.new_page()
    page.goto(f"https://x.com/i/web/status/{tweet_id}", timeout=30000)
    page.wait_for_timeout(3000)

    unlike_btn = page.query_selector('[data-testid="unlike"]')
    if unlike_btn:
        unlike_btn.click()
        time.sleep(1)
        return {"status": "unliked", "tweet_id": tweet_id}
    return {"error": "Unlike button not found (may not be liked)"}


def _pw_retweet(context, tweet_id):
    page = context.new_page()
    page.goto(f"https://x.com/i/web/status/{tweet_id}", timeout=30000)
    page.wait_for_timeout(3000)

    rt_btn = page.query_selector('[data-testid="retweet"]')
    if rt_btn:
        rt_btn.click()
        page.wait_for_timeout(1000)
        # Confirm retweet in dropdown
        confirm = page.query_selector('[data-testid="retweetConfirm"]')
        if confirm:
            confirm.click()
            time.sleep(1)
        return {"status": "retweeted", "tweet_id": tweet_id}
    return {"error": "Retweet button not found"}


def _pw_follow(context, username):
    page = context.new_page()
    page.goto(f"https://x.com/{username.lstrip('@')}", timeout=30000)
    page.wait_for_timeout(3000)

    follow_btn = page.query_selector('[data-testid="follow"]')
    if follow_btn:
        follow_btn.click()
        time.sleep(1)
        return {"status": "followed", "username": username}
    return {"error": "Follow button not found (already following?)"}


def _pw_unfollow(context, username):
    page = context.new_page()
    page.goto(f"https://x.com/{username.lstrip('@')}", timeout=30000)
    page.wait_for_timeout(3000)

    unfollow_btn = page.query_selector('[data-testid="unfollow"]')
    if unfollow_btn:
        unfollow_btn.click()
        page.wait_for_timeout(1000)
        confirm = page.query_selector('[data-testid="confirmationSheetConfirm"]')
        if confirm:
            confirm.click()
            time.sleep(1)
        return {"status": "unfollowed", "username": username}
    return {"error": "Unfollow button not found (not following?)"}


def _pw_search(context, query, count=10):
    page = context.new_page()
    page.goto(f"https://x.com/search?q={query}&src=typed_query&f=live", timeout=30000)
    page.wait_for_timeout(5000)

    tweets = page.query_selector_all('[data-testid="tweetText"]')
    results = []
    for i, t in enumerate(tweets[:count]):
        text = t.inner_text()
        # Try to get username
        parent = t.evaluate("el => el.closest('[data-testid=\"tweet\"]')")
        user_el = page.query_selector('[data-testid="User-Name"]') if parent else None
        username = user_el.inner_text().split('\n')[0] if user_el else "unknown"

        results.append({"index": i, "user": username, "text": text[:200]})
    return results


def _pw_timeline(context, count=10):
    page = context.new_page()
    page.goto("https://x.com/home", timeout=30000)
    page.wait_for_timeout(5000)

    tweets = page.query_selector_all('[data-testid="tweetText"]')
    results = []
    for i, t in enumerate(tweets[:count]):
        results.append({"index": i, "text": t.inner_text()[:200]})
    return results


def _pw_user(context, username):
    page = context.new_page()
    page.goto(f"https://x.com/{username.lstrip('@')}", timeout=30000)
    page.wait_for_timeout(4000)

    name_el = page.query_selector('[data-testid="UserName"] span')
    display_name = name_el.inner_text() if name_el else username

    bio_el = page.query_selector('[data-testid="UserDescription"]')
    bio = bio_el.inner_text() if bio_el else ""

    body = page.inner_text('body')
    followers = following = "N/A"
    for part in body.split('\n'):
        if 'Followers' in part:
            followers = part.replace('Followers', '').strip().split()[-1] if part.strip() else "N/A"
        if 'Following' in part:
            following = part.replace('Following', '').strip().split()[-1] if part.strip() else "N/A"

    return {
        "username": username.lstrip('@'),
        "name": display_name,
        "bio": bio,
        "followers": followers,
        "following": following,
    }


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    cmd = sys.argv[1].lower()

    if cmd == "whoami":
        run_playwright("whoami")
    elif cmd == "tweet":
        if len(sys.argv) < 3:
            print(json.dumps({"error": "Usage: tweet <text>"}))
            sys.exit(1)
        run_playwright("tweet", sys.argv[2])
    elif cmd == "reply":
        if len(sys.argv) < 4:
            print(json.dumps({"error": "Usage: reply <tweet_id> <text>"}))
            sys.exit(1)
        run_playwright("reply", sys.argv[2], sys.argv[3])
    elif cmd == "like":
        run_playwright("like", sys.argv[2])
    elif cmd == "unlike":
        run_playwright("unlike", sys.argv[2])
    elif cmd == "retweet":
        run_playwright("retweet", sys.argv[2])
    elif cmd == "follow":
        run_playwright("follow", sys.argv[2])
    elif cmd == "unfollow":
        run_playwright("unfollow", sys.argv[2])
    elif cmd == "search":
        query = sys.argv[2] if len(sys.argv) > 2 else ""
        count = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        run_playwright("search", query, count)
    elif cmd == "timeline":
        count = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        run_playwright("timeline", count)
    elif cmd == "user":
        run_playwright("user", sys.argv[2])
    else:
        print(json.dumps({"error": f"Unknown command: {cmd}"}))
        sys.exit(1)


if __name__ == "__main__":
    main()
