"""FastAPI backend entry point"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.v1 import playlists

app = FastAPI(title="Ladybug TV API", version="1.0.0")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(playlists.router)
@app.get("/")
async def root():
    return {"message": "Ladybug TV API"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
