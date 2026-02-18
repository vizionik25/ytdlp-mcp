from fastapi import APIRouter, HTTPException
from fast_ytdlp.schemas import DownloadResponse, DownloadStatus
from fast_ytdlp.ytdlp_utils import download_video
import os

# Create download router
router = APIRouter(prefix="/download", tags=["download"])

SEARCH_RESULTS_FILE = "search_results.txt"
DOWNLOAD_DIR = "downloads"

@router.post("/", response_model=DownloadResponse)
async def perform_download():
    """
    Download videos for each URL contained within search_results.txt.
    """
    if not os.path.exists(SEARCH_RESULTS_FILE):
        raise HTTPException(status_code=400, detail=f"{SEARCH_RESULTS_FILE} not found. Please run search first.")
        
    with open(SEARCH_RESULTS_FILE, "r") as f:
        urls = [line.strip() for line in f if line.strip()]
        
    if not urls:
        raise HTTPException(status_code=400, detail="No URLs found in search_results.txt")
        
    results = []
    for url in urls:
        try:
            filename = download_video(url, DOWNLOAD_DIR)
            results.append(DownloadStatus(url=url, status="Success", filename=filename))
        except Exception as e:
            results.append(DownloadStatus(url=url, status="Failed", error=str(e)))
            
    return DownloadResponse(results=results)
