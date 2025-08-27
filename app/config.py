from pydantic_settings import BaseSettings
from typing import Optional
import os 

class Settings(BaseSettings):
    # app settings
    ENVIRONMENT: str = "development"
    DEBUG: bool = True 
    
    # whatsapp settings
    WHATSAPP_API_URL: str = "https://graph.facebook.com/v16.0"
    WHATASSAPP_ACCESS_TOKEN: Optional[str] = None
    WHATSAPP_PHONE_NUMBER_ID: Optional[str] = None
    WHATSAPP_VERIFY_TOKEN: Optional[str] = None
    
    # OpenAI Config
    OPENAI_API_KEY: Optional[str] = None
    
    # Security 
    WEBHOOK_SECRET: Optional[str] = None
    
    class Config:
        env_file =  ".env"
        case_sensitive = True
        
# load global settings object
settings = Settings()

# check if running in a container and override settings from environment variables
def validate_settings():
    required_vars = [
        "WHATSAPP_ACCESS_TOKEN",
        "WHATSAPP_PHONE_NUMBER_ID", 
        "WHATSAPP_VERIFY_TOKEN",
        "OPENAI_API_KEY"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not getattr(settings, var):
            missing_vars.append(var)
            
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

if settings.ENVIRONMENT == "production":
    validate_config()