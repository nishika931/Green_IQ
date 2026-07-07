from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.database import Base, engine

from models.user import User
from models.plant import Plant
from models.chat import Chat

# Routes
from routes.auth_routes import router as auth_router
from routes.plant_routes import router as plant_router
from routes.chat_routes import router as chat_router
from routes.plant_info_routes import router as plant_info_router
from routes.history_routes import router as history_router
from routes.plant_ai_routes import router as plant_ai_router


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Green IQ API",
    version="1.0.0",
    description="Multi-Agent AI Plant Care Assistant"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "message": "🌿 Green IQ API Running",
        "status": "success"
    }



app.include_router(auth_router, tags=["Auth"])
app.include_router(plant_router, tags=["Plants"])
app.include_router(chat_router, tags=["Chat & AI"])
app.include_router(plant_info_router, tags=["Plant Info"])
app.include_router(history_router,tags=["history"])
app.include_router(plant_ai_router)