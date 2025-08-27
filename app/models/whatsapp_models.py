from pydantic import BaseModel, Field 
from typing import List, Optional, Dict, Any
from datetime import datetime

class WhatsAppProfile(BaseModel):
    name: str 
    
class WhatsAppContact(BaseModel):
    profile: WhatsAppProfile
    wa_id: str
    
class WhatsAppText(BaseModel):
    body: str

class WhatsAppImage(BaseModel):
    caption: Optional[str] = None
    mime_type: str
    sha256: str
    id: str

class WhatsAppDocument(BaseModel):
    caption: Optional[str] = None
    filename: Optional[str] = None
    mime_type: str
    sha256: str
    id: str

class WhatsAppAudio(BaseModel):
    mime_type: str 
    sha256: str
    id: str
    voice: bool = False
    
class WhatsAppVideo(BaseModel):
    caption: Optional[str] = None
    mime_type: str
    sha256: str
    id: str
    
class WhatsAppLocation(BaseModel):
    latitude: float
    longitude: float
    name: Optional[str] = None
    address: Optional[str] = None
    
class WhatsAppMessage(BaseModel):
    id: str
    from_: str = Field(..., alias="from")
    timestamp: str
    type: str
    text: Optional[WhatsAppText] = None
    image: Optional[WhatsAppImage] = None
    document: Optional[WhatsAppDocument] = None
    audio: Optional[WhatsAppAudio] = None
    video: Optional[WhatsAppVideo] = None
    location: Optional[WhatsAppLocation] = None
    contacts: Optional[List[WhatsAppContact]] = None
    
class WhatsAppStatus(BaseModel):
    id: str
    status: str
    timestamp: str
    recipient_id: str

class WhatsAppError(BaseModel):
    code: int
    title: str
    message: str
    error_data: Optional[Dict[str, Any]] = None
    
class WhatsAppMetadata(BaseModel):
    display_phone_number: str
    phone_number_id: str
    
class WhatsAppValue(BaseModel):
    messaging_product: str
    metadata: WhatsAppMetadata
    contacts: Optional[List[WhatsAppContact]] = None
    messages: Optional[List[WhatsAppMessage]] = None
    statuses: Optional[List[WhatsAppStatus]] = None
    errors: Optional[List[WhatsAppError]] = None

class WhatsAppChange(BaseModel):
    value: WhatsAppValue
    field: str

class WhatsAppEntry(BaseModel):
    id: str
    changes: List[WhatsAppChange]

class WebhookEvent(BaseModel):
    object: str
    entry: List[WhatsAppEntry]

# Modelos para respuestas de la API
class MessageResponse(BaseModel):
    messaging_product: str
    to: str
    type: str
    text: Optional[Dict[str, str]] = None
    template: Optional[Dict[str, Any]] = None

class APIResponse(BaseModel):
    messaging_product: str
    contacts: List[Dict[str, str]]
    messages: List[Dict[str, str]]

# Modelo para configuración de webhook
class WebhookVerification(BaseModel):
    mode: str = Field(alias="hub.mode")
    token: str = Field(alias="hub.verify_token")
    challenge: str = Field(alias="hub.challenge")

# Modelo para conversación/historial
class ConversationMessage(BaseModel):
    role: str  # "user", "assistant", "system"
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)

class UserConversation(BaseModel):
    user_id: str
    phone_number: str
    messages: List[ConversationMessage] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

# Modelo para estadísticas
class MessageStats(BaseModel):
    total_messages_received: int = 0
    total_messages_sent: int = 0
    total_users: int = 0
    active_conversations: int = 0
    last_reset: datetime = Field(default_factory=datetime.now)