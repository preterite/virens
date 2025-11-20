# Observatory Data Directory

This directory contains your personal academic metrics data.

## Structure

- `data/` - SQLite database with publication and citation data
- `logs/` - Observatory fetcher logs

## Privacy

This data is part of your private user instance and is never committed to the public VIRENS framework repository.

## Usage

The Observatory module (if enabled) will automatically create and maintain the database in `data/observatory.db`.

Run `observatory-configure` to set up your API keys and publication information.
