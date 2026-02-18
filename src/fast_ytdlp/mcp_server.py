from fastmcp import FastMCP
from fast_ytdlp.ytdlp_utils import search_youtube, download_video
import os

# this is the file where you will write the code for the fastmcp server

mcp = FastMCP("FastYTDLP")

SEARCH_RESULTS_FILE = "search_results.txt"
DOWNLOAD_DIR = "downloads"

@mcp.tool()
def search_youtube_tool(query: str, max_results: int = 10):
    """
    Search YouTube for a query and save the top 10 URLs to search_results.txt.
    """
    urls = search_youtube(query, max_results)
    
    if not urls:
        return "No results found."
        
    with open(SEARCH_RESULTS_FILE, "w") as f:
        for url in urls:
            f.write(f"{url}\n")
            
    return f"Successfully saved {len(urls)} URLs to {SEARCH_RESULTS_FILE}:\n" + "\n".join(urls)

@mcp.tool()
def download_videos_tool():
    """
    Download videos from the URLs contained in search_results.txt.
    """
    if not os.path.exists(SEARCH_RESULTS_FILE):
        return f"{SEARCH_RESULTS_FILE} not found. Please search first."
        
    with open(SEARCH_RESULTS_FILE, "r") as f:
        urls = [line.strip() for line in f if line.strip()]
        
    if not urls:
        return "No URLs found in search_results.txt"
        
    results = []
    for url in urls:
        try:
            filename = download_video(url, DOWNLOAD_DIR)
            results.append(f"SUCCESS: {url} -> {filename}")
        except Exception as e:
            results.append(f"FAILED: {url} -> {str(e)}")
            
    return "\n".join(results)

if __name__ == "__main__":
    mcp.run()
