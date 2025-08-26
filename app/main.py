from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
#from dotenv import load_dotenv
#import os

#from app.config import settings
#from app.routers import webhook

# Crear la aplicación FastAPI
app = FastAPI(
    title="WhatsApp Bot API",
    description="Bot de WhatsApp integrado con OpenAI",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica los dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
#app.include_router(webhook.router, prefix="/webhook", tags=["webhook"])

@app.get("/")
async def root():
    return {"message": "WhatsApp Bot API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "environment": settings.ENVIRONMENT}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)