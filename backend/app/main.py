from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.database import Base,engine
from backend.app.routers import auth

Base.metadata.create_all(bind=engine)
app=FastAPI()

origins = [
    "http://localhost:3000", #front
    "http://10.0.2.2.8081", #emulador
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)