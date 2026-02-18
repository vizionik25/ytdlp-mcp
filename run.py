import subprocess
import time
import httpx
import sys
import os

def run_fastapi():
    print("🚀 Starting FastAPI server...")
    # Run uvicorn as a background process
    # We use 'src' in PYTHONPATH so it can find fast_ytdlp
    env = os.environ.copy()
    env["PYTHONPATH"] = os.path.join(os.getcwd(), "src")
    
    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "fast_ytdlp.main:app", "--host", "127.0.0.1", "--port", "8000"],
        env=env
    )
    return proc

def wait_for_health():
    print("⏳ Waiting for FastAPI health check...")
    url = "http://127.0.0.1:8000/health"
    max_retries = 30
    for i in range(max_retries):
        try:
            with httpx.Client() as client:
                response = client.get(url)
                if response.status_code == 200 and response.json().get("status") == "ok":
                    print("✅ FastAPI is healthy!")
                    return True
        except Exception:
            pass
        time.sleep(1)
    print("❌ FastAPI failed to start in time.")
    return False

def run_mcp():
    print("⚡ Starting MCP server (HTTP transport)...")
    # Import and run the MCP server
    # We need src in path for imports to work
    sys.path.append(os.path.join(os.getcwd(), "src"))
    from fast_ytdlp.mcp_server import mcp
    
    # FastMCP run(transport="http") starts an HTTP server
    mcp.run(transport="http", host="0.0.0.0", port=8888)

if __name__ == "__main__":
    fastapi_proc = None
    try:
        fastapi_proc = run_fastapi()
        if wait_for_health():
            run_mcp()
        else:
            fastapi_proc.terminate()
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
    finally:
        if fastapi_proc:
            fastapi_proc.terminate()
