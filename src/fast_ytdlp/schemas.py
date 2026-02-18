from pydantic import BaseModel, Field
from typing import List, Optional

# this is the file where you will write the fastapi schemas or classes

class SearchRequest(BaseModel):
    query: str = Field(..., description="The search term for YouTube")
    max_results: int = Field(default=10, description="Number of results to return (up to 10)")

class SearchResponse(BaseModel):
    urls: List[str] = Field(..., description="List of top 10 URLs")
    status: str = Field(..., description="Status of the search and save operation")

class DownloadStatus(BaseModel):
    url: str
    status: str
    filename: Optional[str] = None
    error: Optional[str] = None

class DownloadResponse(BaseModel):
    results: List[DownloadStatus] = Field(..., description="Status of each download")
