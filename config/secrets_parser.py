from __future__ import annotations

import logging
import os
from pathlib import Path

import pymongo
import yaml
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()
logger = logging.getLogger("farm_app")

# Load config from secrets.yml as fallback defaults
config_path = Path(__file__).parent / "secrets.yml"
with open(config_path) as stream:
    secrets = yaml.safe_load(stream)

# Prefer environment variables, fall back to secrets.yml
mongodb_host = os.getenv("MONGODB_HOST", secrets["mongodb"]["host"])
mongodb_port = int(os.getenv("MONGODB_PORT", secrets["mongodb"]["port"]))
mongodb_username = os.getenv("MONGODB_USERNAME", secrets["mongodb"].get("username"))
mongodb_password = os.getenv("MONGODB_PASSWORD", secrets["mongodb"].get("password"))
mongodb_database = os.getenv("MONGODB_DATABASE", secrets["mongodb"].get("database", "farm_template"))
# Auth database for the credentials. Defaults to "admin" because that is where
# the MONGO_INITDB_ROOT_USERNAME user lives (docker-compose setup).
mongodb_auth_source = os.getenv("MONGODB_AUTH_SOURCE", secrets["mongodb"].get("auth_source", "admin"))

# Connection string for MongoDB
if mongodb_username and mongodb_password:
    MONGODB_URL = (
        f"mongodb://{mongodb_username}:{mongodb_password}@{mongodb_host}:{mongodb_port}"
        f"/{mongodb_database}?authSource={mongodb_auth_source}"
    )
else:
    MONGODB_URL = f"mongodb://{mongodb_host}:{mongodb_port}"

# Async MongoDB client
client = AsyncIOMotorClient(MONGODB_URL)


def get_database():
    """Get the database instance"""
    return client[mongodb_database]


def connect_to_mongodb():
    """Connect to MongoDB (sync version for testing)"""
    try:
        sync_client = pymongo.MongoClient(
            host=mongodb_host,
            port=mongodb_port,
            username=mongodb_username,
            password=mongodb_password,
            authSource=mongodb_auth_source if mongodb_username else None,
            authMechanism="SCRAM-SHA-256" if mongodb_username else None,
        )
        sync_client.admin.command("ping")
        return sync_client
    except Exception:
        logger.exception("MongoDB connection error")
        return None


def get_mongodb_database():
    try:
        db_client = connect_to_mongodb()
        return db_client[mongodb_database]
    except Exception:
        logger.exception("Failed to get MongoDB database")
        return None


def get_mongodb_collection(collection_name: str):
    try:
        database = get_mongodb_database()
        return database[collection_name]
    except Exception:
        logger.exception("Failed to get MongoDB collection")
        return None
