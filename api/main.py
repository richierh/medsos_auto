print("FILE LOADED", flush=True)

from fastapi import FastAPI
from pydantic import BaseModel
from scripts.render_video import render_video

app = FastAPI()


class RenderRequest(BaseModel):
    row_number: int
    template: str
    title: str
    text_1: str = ""
    text_2: str = ""
    text_3: str = ""
    text_4: str = ""
    text_5: str = ""
    asset_keyword: str = ""
    music_mood: str = ""


# @app.post("/render")
# def render(req: RenderRequest):

#     print(req.title)
#     print(req.template)
#     print(req.text_1)

#     return {"status": "success"}

@app.get("/")
def root():
    print("ROOT HIT", flush=True)
    return {"status": "ok"}

@app.post("/render")
def render(req: RenderRequest):
    print('hello')
    result = render_video(
        title=req.title,
        template=req.template,
        texts=[
            req.text_1,
            req.text_2,
            req.text_3,
            req.text_4,
            req.text_5
        ],
        asset_keyword=req.asset_keyword,
        music_mood=req.music_mood
    )
    print('hello')

    return result