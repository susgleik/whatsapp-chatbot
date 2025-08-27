import aiohttp
import logging
from typing import Optional

from app.config import settings

logger = logging.getLogger(__name__)

class WhatsAppService: 
    def __init__(self):
        self.api_url = settings.WHATSAPP_API_URL
        self.access_token = settings.WHATASSAPP_ACCESS_TOKEN
        self.phone_number_id = settings.WHATSAPP_PHONE_NUMBER_ID
        
    async def send_message(self, to: str, message: str, message_type: str = "text" ) -> bool:
        """Enviar mensaje de texto via WhatsApp Business API"""
        url = f"{self.api_url}/{self.phone_number_id}/messages"
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": message_type,
            "text": {
                "body": message
            }
        }
        
        try: 
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload, headers=headers) as response:
                    if response.status == 200:
                        result = await response.json()
                        logger.info(f"Message sent successfully: {result}")
                        return True
                    else:
                        error_text = await response.text()
                        logger.error(f"Failed to send message: {response.status} - {error_text}")
                        return False
        except Exception as e:
            logger.exception(f"Exception occurred while sending message: {e}")
            return False
        
        async def send_template_message(self, to: str, template_name: str, language_code: str = "es"):
            """Enviar mensaje de plantilla"""
            url = f"{self.api_url}/{self.phone_number_id}/messages"
            
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "messaging_product": "whatsapp",
                "to": to,
                "type": "template",
                "template": {
                    "name": template_name,
                    "language": {
                        "code": language_code
                    }
                }
            }
            
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(url, json=payload, headers=headers) as response:
                        if response.status == 200:
                            result = await response.json()
                            logger.info(f"Template message sent successfully: {result}")
                            return True
                        else:
                            error_text = await response.text()
                            logger.error(f"Failed to send template message: {response.status} - {error_text}")
                            return False
            
            except Exception as e:
                logger.exception(f"Exception occurred while sending template message: {e}")
                return False
            
    async def mark_message_as_read(self, message_id: str) -> bool:
        """Marcar mensaje como leído"""
        url = f"{self.api_url}/{self.phone_number_id}/messages"
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id": message_id
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload, headers=headers) as response:
                    return response.status == 200
        except Exception as e:
            logger.exception(f"Error marking message as read: {str(e)}")
            return False        