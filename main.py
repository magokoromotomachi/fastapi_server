from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from convert_to_geojsons import tokyo_ku_dict


app = FastAPI()
origins = [
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "tokyo_ku_dict": tokyo_ku_dict})


@app.get("/maps/maplibre.html", response_class=HTMLResponse)
def get_map(request: Request):
    return templates.TemplateResponse(
        "maplibre.html",
        {"request": request},
    )


@app.get("/maps/{map_id}", response_class=HTMLResponse)
def get_map(map_id: str, request: Request):
    title = tokyo_ku_dict[map_id.split('_')[0]]
    geojson_path = f"/static/json/{map_id.replace('.html', '')}.geojson"
    return templates.TemplateResponse(
        "map.html",
        {"request": request, "title": title, "geojson_path": geojson_path},
    )
