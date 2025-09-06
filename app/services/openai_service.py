import openai
import logging
from typing import List, Dict, Optional

from app.config import settings

logger = logging.getLogger(__name__)

class OpenAIService:
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY
        self.model = "gpt-3.5-turbo"  # o "gpt-4" si tienes acceso
        self.max_tokens = 1000
        self.conversation_history: Dict[str, List[Dict]] = {}
    
    async def generate_response(self, user_message: str, user_id: str = "default") -> str:
        """Generar respuesta usando OpenAI GPT"""
        try:
            # Obtener o inicializar historial de conversación
            if user_id not in self.conversation_history:
                self.conversation_history[user_id] = [
                    {
                        "role": "system",
                        "content": "Eres un asistente útil y amigable que responde a través de WhatsApp. "
                                 "Mantén tus respuestas concisas y relevantes. "
                                 "Puedes ayudar con preguntas generales, dar consejos y mantener conversaciones casuales."
                    }
                ]
            
            # Agregar mensaje del usuario
            self.conversation_history[user_id].append({
                "role": "user",
                "content": user_message
            })
            
            # Limitar historial para evitar exceder límites de tokens
            if len(self.conversation_history[user_id]) > 10:
                # Mantener mensaje del sistema y últimos 8 mensajes
                system_msg = self.conversation_history[user_id][0]
                recent_msgs = self.conversation_history[user_id][-8:]
                self.conversation_history[user_id] = [system_msg] + recent_msgs
            
            # Generar respuesta
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=self.conversation_history[user_id],
                max_tokens=self.max_tokens,
                temperature=0.7,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            
            ai_response = response.choices[0].message.content.strip()
            
            # Agregar respuesta al historial
            self.conversation_history[user_id].append({
                "role": "assistant",
                "content": ai_response
            })
            
            logger.info(f"Generated response for user {user_id}: {ai_response}")
            return ai_response
            
        except Exception as e:
            logger.error(f"Error generating OpenAI response: {str(e)}")
            return "Lo siento, no pude procesar tu mensaje en este momento. Por favor intenta más tarde."
    
    def clear_conversation_history(self, user_id: str):
        """Limpiar historial de conversación para un usuario"""
        if user_id in self.conversation_history:
            del self.conversation_history[user_id]
            logger.info(f"Cleared conversation history for user {user_id}")
    
    def get_conversation_history(self, user_id: str) -> List[Dict]:
        """Obtener historial de conversación"""
        return self.conversation_history.get(user_id, [])
    
    async def generate_summary(self, conversation: List[Dict]) -> str:
        """Generar resumen de conversación"""
        try:
            messages_text = "\n".join([
                f"{msg['role']}: {msg['content']}" 
                for msg in conversation 
                if msg['role'] in ['user', 'assistant']
            ])
            
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "Resume la siguiente conversación de manera concisa:"
                    },
                    {
                        "role": "user",
                        "content": messages_text
                    }
                ],
                max_tokens=200,
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error generating summary: {str(e)}")
            return "Error generando resumen"