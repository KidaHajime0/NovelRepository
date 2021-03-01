from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from starlette.templating import Jinja2Templates


from pathlib import Path

# TODO: Database
# TODO: Pijul機能追加

PATH_BASE = Path(__file__).resolve().parent
PATH_STATIC = str(PATH_BASE / "static")
PATH_REPO = str(PATH_BASE / "repository")

def create_app():
    _app = FastAPI(
        title="Pijul簡易リポジトリ",
        description="Pijul用リポジトリ テスト版",
        version="0.0.1",
    )
    # static
    # Url "/static"以下にstaticファイルをマウント
    _app.mount(
        "/static",
        StaticFiles(directory=PATH_STATIC, html=False),
        name="static",
    )
    # TODO: Database Internal Repository
    # repository
    # Url "/repository"以下にrepositoryファイルをマウント
    _app.mount(
        "/repository",
        StaticFiles(directory=PATH_REPO, html=False),
        name="repository",
    )
    return _app


app = create_app()

# テンプレート関連の設定(jinja2)
templates = Jinja2Templates(directory="templates")
jinja_env = templates.env  # Jinja2.Environment : filterやglobalの設定用


@app.get("/")
async def root():
    return RedirectResponse("/_kida_hajime_")


@app.get("/{user_id}")
async def root(request: Request, user_id: str):
    # pathlib: オブジェクト指向のファイルパスシステム
    # __file__でこのファイルのパスを取得
    repo_path = Path(PATH_REPO) / user_id
    if repo_path.is_dir():
        repositories: list[str] = [repo.name for repo in repo_path.iterdir() if repo.is_dir()]
    else:
        repositories: list[str] = ["test"]
    return templates.TemplateResponse("dashboard.html",
                                      {"request": request,
                                       "id": user_id,
                                       "username": "紀田　創",
                                       "repository": repositories})
