from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from typing import Optional

from pathlib import Path

# TODO: Database
# TODO: Pijul機能追加

PATH_BASE: Path = Path(__file__).resolve().parent
PATH_STATIC: Path = PATH_BASE / "static"
PATH_REPO: Path = PATH_BASE / "repository"


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
        StaticFiles(directory=str(PATH_STATIC), html=False),
        name="static",
    )

    return _app


app = create_app()

# テンプレート関連の設定(jinja2)
templates = Jinja2Templates(directory="templates")
jinja_env = templates.env  # Jinja2.Environment : filterやglobalの設定用


@app.get("/")
async def get_index(request: Request):
    user_dict: dict[str, str] = {"id": "KidaHajime",
                                 "username": "紀田　創"}
    return templates.TemplateResponse("index.html",
                                      {"request": request,
                                       "user_dict": user_dict})


@app.get("/{user_id}")
async def get_dashboard(request: Request, user_id: str):
    # pathlib: オブジェクト指向のファイルパスシステム
    # __file__でこのファイルのパスを取得
    user_repos_path: Path = Path(PATH_REPO) / user_id
    if user_repos_path.is_dir():
        # repositoryディレクトリ内のディレクトリをリポジトリとして取得
        # TODO: Dict DB request(reponame & descriptions)
        repositories: list[str] = [repo.name for repo in user_repos_path.iterdir() if repo.is_dir()]
    else:
        # TODO: Error
        repositories = []
    return templates.TemplateResponse("dashboard.html",
                                      {"request": request,
                                       "user_id": user_id,
                                       "username": "紀田　創",
                                       "repository": repositories})


# /{user_id}/{repository}(?subdir=xxx/xxx)
@app.get("/{user_id}/{repository}")
async def get_repository(request: Request,
                         user_id: str,
                         repository: str,
                         subdir: Optional[str] = None):
    # TODO: query reject
    if subdir:
        target_path: Path = PATH_REPO / user_id / repository / subdir
        if len(subdir.split("/")) >= 2:
            parent: str = f"/{user_id}/{repository}?subdir={Path(subdir).parent}"
        else:
            parent: str = f"/{user_id}/{repository}"
    else:
        target_path: Path = PATH_REPO / user_id / repository
        parent: str = f"/{user_id}"

    readme_path = target_path / 'README.md'
    if readme_path.exists():
        readme_file: str = readme_path.read_text()
    else:
        readme_file: str = ""

    if target_path.is_dir():
        # リポジトリ内のディレクトリを取得
        target_dirs: list[str] = sorted([repo.name for repo in target_path.iterdir() if repo.is_dir()])
        target_files: list[str] = sorted([repo.name for repo in target_path.iterdir() if repo.is_file()])
    else:
        # TODO: Error
        target_dirs = []
        target_files = []

    return templates.TemplateResponse("repository.html",
                                      {"request": request,
                                       "user_id": user_id,
                                       "repository": repository,
                                       "target_dirs": target_dirs,
                                       "target_files": target_files,
                                       "readme_file": readme_file,
                                       "subdir": subdir,
                                       "parent": parent})


@app.get("/{user_id}/{repository}")
async def view_file(request: Request,
                    user_id: str,
                    repository: str,
                    subdir: Optional[str] = None,
                    file: Optional[str] = None):
    return 1

# TODO: ファイルビューア, リポジトリページのパス化, README, md, 戻るボタン＝前ディレクトリ
"""
    リポジトリ機能:
        config機能: 話数管理、タイトル管理、
"""
