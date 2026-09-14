# Reddit Public Opinion Analysis

A small, non-commercial research prototype for read-only analysis of publicly available Reddit posts from a limited set of selected subreddits.

## Purpose

This project is intended to help study broad discussion trends and public sentiment at an aggregate level. It uses Reddit's official OAuth API and is designed to:

- read a limited number of recent public posts from explicitly selected subreddits;
- calculate aggregate activity metrics and common title keywords;
- support future aggregate trend and sentiment research;
- avoid collecting data that is not needed for the analysis.

## What the app does not do

The app does **not**:

- create posts or comments;
- vote, moderate, follow users, or send messages;
- access private content;
- profile or monitor individual Redditors;
- scrape Reddit web pages;
- use Reddit data to train an AI or machine-learning model;
- sell or redistribute Reddit data.

The client is read-only and respects Reddit API authentication requirements and rate limits.

## Data handling

The current proof of concept processes a small sample in memory and prints only aggregate results. It does not intentionally collect usernames and does not persist raw Reddit content to a database.

## Project status

This repository contains an initial proof of concept for a Reddit Data API application review. The scope is intentionally small and transparent.

## Setup

Requirements:

- Python 3.10 or newer
- A Reddit OAuth application with a client ID and client secret

Install the dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows PowerShell, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

Copy `.env.example` to `.env`, then fill in the OAuth credentials issued for your Reddit application.

Run the read-only analysis:

```bash
python src/main.py
```

## Configuration

| Variable | Description | Default |
| --- | --- | --- |
| `REDDIT_CLIENT_ID` | Reddit OAuth client ID | Required |
| `REDDIT_CLIENT_SECRET` | Reddit OAuth client secret | Required |
| `REDDIT_USER_AGENT` | Descriptive API user agent | Required |
| `SUBREDDITS` | Comma-separated subreddit names | `technology,worldnews` |
| `POST_LIMIT` | Recent posts read per subreddit; maximum 100 | `25` |

## Responsible use

Anyone running this project is expected to follow Reddit's Developer Terms, Data API Terms, Content Policy, privacy requirements, and API rate limits. Access can be reduced or disabled if Reddit's requirements change.
