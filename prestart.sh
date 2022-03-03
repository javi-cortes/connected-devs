#! /usr/bin/env bash

cd /app

# Create tables DB
python app/db/database.py

# Run migrations
alembic upgrade head
