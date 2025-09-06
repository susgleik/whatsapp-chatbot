import hashlib
import hmac
import logging
from fastapi import Request, HTTPException, Header
from typing import Optional

from app.config import settings

logger = logging.getLogger(__name__)

async def verify_webhook_signature(
    request: Request,
    x_hub_signature_256: Optional[str] = Header(None)
) -> str:
    """
    Verificar la firma del webhook de Meta/WhatsApp
    """
    if not settings.WEBHOOK_SECRET:
        logger.warning("WEBHOOK_SECRET not configured, skipping signature verification")
        return "no-verification"
    
    if not x_hub_signature_256:
        logger.error("Missing X-Hub-Signature-256 header")
        raise HTTPException(status_code=401, detail="Missing signature header")
    
    try:
        # Obtener el cuerpo de la solicitud
        body = await request.body()
        
        # Calcular la firma esperada
        expected_signature = hmac.new(
            settings.WEBHOOK_SECRET.encode('utf-8'),
            body,
            hashlib.sha256
        ).hexdigest()
        
        # El header viene en formato "sha256=<signature>"
        if not x_hub_signature_256.startswith('sha256='):
            logger.error("Invalid signature format")
            raise HTTPException(status_code=401, detail="Invalid signature format")
        
        received_signature = x_hub_signature_256[7:]  # Remover "sha256="
        
        # Comparar firmas de manera segura
        if not hmac.compare_digest(expected_signature, received_signature):
            logger.error("Signature verification failed")
            raise HTTPException(status_code=401, detail="Invalid signature")
        
        logger.info("Webhook signature verified successfully")
        return received_signature
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error verifying webhook signature: {str(e)}")
        raise HTTPException(status_code=500, detail="Signature verification error")

def generate_webhook_signature(payload: bytes, secret: str) -> str:
    """
    Generar firma para webhook (útil para testing)
    """
    signature = hmac.new(
        secret.encode('utf-8'),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    return f"sha256={signature}"

def validate_phone_number(phone_number: str) -> bool:
    """
    Validar formato de número de teléfono
    """
    # Implementar validación básica
    # El número debe tener al menos 10 dígitos y puede empezar con +
    import re
    pattern = r'^\+?[1-9]\d{9,14}$'
    return bool(re.match(pattern, phone_number))

def sanitize_message(message: str) -> str:
    """
    Sanitizar mensaje para evitar inyecciones o contenido malicioso
    """
    # Implementar sanitización básica
    # Remover caracteres de control y limitar longitud
    sanitized = ''.join(char for char in message if ord(char) >= 32 or char in '\n\r\t')
    return sanitized[:4096]  # Limitar a 4KB

class RateLimiter:
    """
    Rate limiter simple basado en memoria
    Para producción, considera usar Redis
    """
    def __init__(self, max_requests: int = 10, window_minutes: int = 1):
        self.max_requests = max_requests
        self.window_minutes = window_minutes
        self.requests = {}  # {user_id: [timestamps]}
    
    def is_allowed(self, user_id: str) -> bool:
        import time
        current_time = time.time()
        window_start = current_time - (self.window_minutes * 60)
        
        # Limpiar requests antiguos
        if user_id in self.requests:
            self.requests[user_id] = [
                timestamp for timestamp in self.requests[user_id] 
                if timestamp > window_start
            ]
        else:
            self.requests[user_id] = []
        
        # Verificar límite
        if len(self.requests[user_id]) >= self.max_requests:
            return False
        
        # Agregar timestamp actual
        self.requests[user_id].append(current_time)
        return True

# Instancia global del rate limiter
rate_limiter = RateLimiter(max_requests=20, window_minutes=1)