from fastapi import APIRouter, HTTPException
from fast_ytdlp.schemas import SearchRequest, SearchResponse
from fast_ytdlp.ytdlp_utils import search_youtube
import os

# Create search router
router = APIRouter(prefix="/search", tags=["search"])

SEARCH_RESULTS_FILE = "search_results.txt"

@router.post("/", response_model=SearchResponse)
async def perform_search(request: SearchRequest):
    """
    Search YouTube and save top 10 URLs to search_results.txt.
    """
    try:
        urls = search_youtube(request.query, request.max_results)
        
        if not urls:
            raise HTTPException(status_code=404, detail="No videos found for the search term")
            
        # Save to file
        with open(SEARCH_RESULTS_FILE, "w") as f:
            for url in urls:
                f.write(f"{url}\n")
                
        return SearchResponse(urls=urls, status=f"Successfully saved {len(urls)} URLs to {SEARCH_RESULTS_FILE}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
