from fastapi import FastAPI
from fast_ytdlp.routers import search, download
import os

# this file is where you will write the main code for the fastapi app

app = FastAPI(title="FastYTDLP API", description="FastAPI with yt-dlp integration")

# Include routers
app.include_router(search.router)
app.include_router(download.router)

@app.get("/")
async def root():
    return {"message": "Welcome to FastYTDLP API. Use /search and /download endpoints."}

@app.get("/health")
async def health():
    return {"status": "ok"}
