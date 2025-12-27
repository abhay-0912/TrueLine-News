#!/bin/bash
# Database initialization script for TrueLine News

# This script initializes the MongoDB database with collections and sample data

# Configuration
MONGODB_HOST=${MONGODB_HOST:-localhost}
MONGODB_PORT=${MONGODB_PORT:-27017}
MONGODB_DB=${MONGODB_DB:-trueline_news}
MONGODB_USER=${MONGODB_USER:-}
MONGODB_PASSWORD=${MONGODB_PASSWORD:-}

# Build MongoDB connection string
if [ -n "$MONGODB_USER" ] && [ -n "$MONGODB_PASSWORD" ]; then
    MONGO_URI="mongodb://${MONGODB_USER}:${MONGODB_PASSWORD}@${MONGODB_HOST}:${MONGODB_PORT}/${MONGODB_DB}"
else
    MONGO_URI="mongodb://${MONGODB_HOST}:${MONGODB_PORT}/${MONGODB_DB}"
fi

echo "Initializing TrueLine News database..."
echo "Connecting to: $MONGO_URI"

# Execute schema creation
mongo "$MONGO_URI" < schema.mongodb

echo "Database initialization completed!"
