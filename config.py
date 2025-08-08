"""
Configuration for AutoGen Society of Mind with Dynamic Tools
Centralizes all configuration settings for the system
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Verify the API key is loaded
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables. Please check your .env file.")

# Configuration for model client creation
OPENAI_CONFIG = {
    "model": os.getenv("OPENAI_MODEL", "gpt-4"),
    "api_key": OPENAI_API_KEY,
    "temperature": 0.7,
    "max_tokens": 1500
}

# UserProxyAgent Configuration
USER_PROXY_CONFIG = {
    "human_input_mode": "ALWAYS",
    "max_consecutive_auto_reply": 3,
    "code_execution_config": False
}

# Tool Configuration
TOOL_CONFIG = {
    "timeout": 30,
    "max_retries": 3,
    "enable_caching": True
}

# API Endpoints
API_ENDPOINTS = {
    "duckduckgo": os.getenv("DUCKDUCKGO_API_URL", "https://api.duckduckgo.com/"),
    "openweather": "https://api.openweathermap.org/data/2.5/"
}

# Debug: Print first few characters of API key to verify it's loaded
print(f"✅ API Key loaded: {OPENAI_API_KEY[:10]}..." if OPENAI_API_KEY else "❌ API Key not loaded")
