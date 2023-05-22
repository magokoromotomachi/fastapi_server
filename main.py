from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles


app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/maps/maplibre.html", response_class=HTMLResponse)
def get_map(request: Request):
    return templates.TemplateResponse(
        "maplibre.html",
        {"request": request},
    )


@app.get("/maps/{map_id}", response_class=HTMLResponse)
def get_map(map_id: str, request: Request):
    return templates.TemplateResponse(
        "map.html",
        {"request": request, "map_id": map_id, "geojson_path": f"/json/{map_id}.geojson"},
    )
