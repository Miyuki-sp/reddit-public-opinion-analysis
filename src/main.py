"""Read-only aggregate analysis of recent public Reddit posts."""

from __future__ import annotations

import json
import os
import re
from collections import Counter
from datetime import datetime, timezone

import praw
from dotenv import load_dotenv


WORD_PATTERN = re.compile(r"[A-Za-z][A-Za-z0-9'-]{2,}")
SUBREDDIT_PATTERN = re.compile(r"^[A-Za-z0-9_]{2,21}$")
STOP_WORDS = {
    "about",
    "after",
    "again",
    "against",
    "also",
    "and",
    "are",
    "because",
    "been",
    "before",
    "being",
    "but",
    "can",
    "could",
    "from",
    "have",
    "into",
    "its",
    "just",
    "more",
    "not",
    "over",
    "that",
    "the",
    "their",
    "then",
    "there",
    "these",
    "they",
    "this",
    "was",
    "were",
    "what",
    "when",
    "where",
    "which",
    "who",
    "will",
    "with",
    "would",
    "you",
    "your",
}


def require_env(name: str) -> str:
    """Return a required environment variable or raise a clear error."""
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def selected_subreddits() -> list[str]:
    """Read and validate the explicitly configured subreddit names."""
    raw_names = os.getenv("SUBREDDITS", "technology,worldnews")
    names = [name.strip() for name in raw_names.split(",") if name.strip()]

    if not names:
        raise RuntimeError("SUBREDDITS must contain at least one subreddit name.")

    invalid = [name for name in names if not SUBREDDIT_PATTERN.fullmatch(name)]
    if invalid:
        raise RuntimeError(f"Invalid subreddit name(s): {', '.join(invalid)}")

    return names


def post_limit() -> int:
    """Return a conservative per-subreddit request limit."""
    raw_limit = os.getenv("POST_LIMIT", "25")
    try:
        value = int(raw_limit)
    except ValueError as exc:
        raise RuntimeError("POST_LIMIT must be an integer.") from exc

    if not 1 <= value <= 100:
        raise RuntimeError("POST_LIMIT must be between 1 and 100.")

    return value


def title_keywords(title: str) -> list[str]:
    """Extract normalized title words for aggregate frequency counts."""
    return [
        word.lower()
        for word in WORD_PATTERN.findall(title)
        if word.lower() not in STOP_WORDS
    ]


def build_client() -> praw.Reddit:
    """Create an OAuth client that is explicitly restricted to read-only use."""
    reddit = praw.Reddit(
        client_id=require_env("REDDIT_CLIENT_ID"),
        client_secret=require_env("REDDIT_CLIENT_SECRET"),
        user_agent=require_env("REDDIT_USER_AGENT"),
    )
    reddit.read_only = True
    return reddit


def analyze_subreddit(
    reddit: praw.Reddit, subreddit_name: str, limit: int
) -> dict[str, object]:
    """Calculate aggregate metrics without retaining usernames or raw post bodies."""
    keywords: Counter[str] = Counter()
    post_count = 0
    total_score = 0
    total_comments = 0

    for post in reddit.subreddit(subreddit_name).new(limit=limit):
        post_count += 1
        total_score += int(post.score)
        total_comments += int(post.num_comments)
        keywords.update(title_keywords(post.title))

    return {
        "posts_analyzed": post_count,
        "average_score": round(total_score / post_count, 2) if post_count else 0,
        "average_comment_count": (
            round(total_comments / post_count, 2) if post_count else 0
        ),
        "top_title_keywords": [
            {"keyword": keyword, "count": count}
            for keyword, count in keywords.most_common(10)
        ],
    }


def main() -> None:
    """Run the configured aggregate analysis and print JSON."""
    load_dotenv()
    reddit = build_client()
    limit = post_limit()

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "mode": "read_only",
        "post_limit_per_subreddit": limit,
        "subreddits": {
            name: analyze_subreddit(reddit, name, limit)
            for name in selected_subreddits()
        },
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
