from fastapi import FastAPI, Query  # type: ignore
import httpx  # type: ignore

app = FastAPI()

GITHUB_API = "https://api.github.com/search/repositories"
HEADERS = {"Accept": "application/vnd.github+json"}

@app.get("/search")
async def search_mcp(prompt: str = Query(..., description="Search query for MCP server-based apps")):
    # The query looks for repositories that mention "mcp server" + the user's prompt
    query_keywords = f'{prompt} "mcp server"'

    params = {
        "q": query_keywords,
        "sort": "stars",
        "order": "desc"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(GITHUB_API, headers=HEADERS, params=params)
        data = response.json()

    results = [
        {
            "name": item["full_name"],
            "url": item["html_url"],
            "description": item["description"]
        }
        for item in data.get("items", [])[:10]
        if item["description"] and "mcp" in item["description"].lower()
    ]
    return {"results": results}

# 👇 Add this to allow running with `python main.py`
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
