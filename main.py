from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests 

app = FastAPI()

#1 Mounts static folder so the browser can load prof pic
app.mount("/static", StaticFiles(directory="static"), name="static")

# 2 Point FastAPI to the templates folder
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def serve_portfolio(request: Request):
    #3 Fetch live metrics from Github via API
    try:
        github_api_url = "https://api.github.com/users/AGreen1990"
        
        # Define user so Github does not block
        headers = {
            "User-Agent": "AGreen1990-Portfolio-App"
        }
        
        response = requests.get(github_api_url, headers=headers, timeout=5)

        #LOGGING: Print exactly what GitHub sends back
        print(f"API Response Code: {response.status_code}")
        print(f"API Data: {response.text}")


        user_data = response.json()
        repo_count = user_data.get("public_repos", "Not Found in Data")
        
    except Exception as e:
        # Fallback just in case Github's API goes down
        print(f"Pipeline Error: {e}")
        repo_count = "Unavailable"

    #4 Serve the html page and inject python variable
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"live_repos": repo_count}
    )