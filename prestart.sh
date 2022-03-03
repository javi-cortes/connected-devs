#!/usr/bin/env bash

sleep 5

cd /app

# Create tables DB
python app/db/database.py

# Run migrations
alembic upgrade head
