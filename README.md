# SocialDex — Blockchain-Certified Social Platform

🇮🇹 [Leggi in italiano](README.it.md)

A full-stack Django web application where users can publish posts that are automatically certified on the Ethereum blockchain. Each post's content is hashed with SHA-256, and the hash is written on-chain as the data payload of an Ethereum transaction — creating a permanent, tamper-evident record of when the content existed.

## Features
- User registration and authentication
- IP monitoring: warns the user when a login occurs from a different IP address than their last session
- Automatic blockchain certification on post creation
- SHA-256 content hashing, with the resulting transaction ID stored alongside the post
- JSON REST API for all posts and for posts from the last hour
- Full-text search across post titles and content
- Admin panel with per-user post counts
- Public user profile with post statistics
- Basic content validation (disallowed-word filter)
- Automatic user profile creation via Django signals

## Tech Stack
- Python 3
- Django 3.1
- web3.py — Ethereum blockchain integration
- SHA-256 — content hashing
- Ethereum Sepolia Testnet — on-chain certification
- SQLite
- Bootstrap 3, HTML/CSS

## Project structure
```
socialDex/     → Django project configuration
API/           → post logic, REST API, blockchain integration
  models.py    → Post model (hash + on-chain transaction ID)
  views.py     → home, new post, search, last-hour posts, JSON API
  utils.py     → sends the certification transaction to the blockchain
  wallet.py    → utility to generate a new Ethereum wallet
accounts/      → authentication and user profile management
  models.py    → Profile model (IP tracking)
  views.py     → register, login, logout
```

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Copy `.env.example` to `.env` and fill in your own values:
   ```bash
   cp .env.example .env
   ```
   - Generate a Django secret key:
     ```bash
     python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
     ```
   - Get a free Ethereum Sepolia RPC endpoint from [Infura](https://www.infura.io/).
   - Generate a wallet for testing (never reuse a wallet holding real funds):
     ```bash
     python API/wallet.py
     ```
   - Fund the test wallet with free Sepolia ETH from a [public faucet](https://sepoliafaucet.com/) — this is required to pay gas fees for on-chain transactions.
3. Run migrations and start the server:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser   # optional, for the admin panel
   python manage.py runserver
   ```

## Security notes

- The Django secret key and blockchain credentials (RPC URL, wallet address, private key) are **never** hardcoded — they're loaded from a local `.env` file, excluded from version control via `.gitignore`.
- `db.sqlite3` is also excluded from version control: it holds real user accounts (password hashes) and content, and a database file should never be committed to a public repository regardless of what it contains.
- If you generate a wallet for this project, treat its private key as sensitive even on a testnet — don't reuse it for anything holding real value.

## Notes on this version

This project was originally built against Ethereum's **Ropsten** testnet, which was permanently deprecated in late 2022. This version has been updated to use **Sepolia**, the current recommended Ethereum testnet, and the `web3.py` calls have been updated to the modern (v6+) API.

While preparing this repository for publication, a few functional issues found in the original implementation were also fixed:
- The on-chain certification step was defined on the `Post` model but was never actually called when a new post was created — posts were saved but never certified. Fixed by calling it explicitly after saving.
- The `hash` field was defined with `max_length=32`, too short for a SHA-256 hex digest (64 characters). Corrected to 64.
- The disallowed-word validation methods were named in camelCase (`cleanTitle`/`cleanContent`), so Django's forms framework — which looks for `clean_<fieldname>` — never actually invoked them. Renamed to `clean_title`/`clean_content` so the filter is now active.

## Purpose

Personal project built to explore the integration between Django web applications and the Ethereum blockchain, applying concepts of immutability and digital content certification.
