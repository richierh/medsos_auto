from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR))

from scripts.render_video import render_video


def index(request):
    return render(request, "login.html")


@csrf_exempt
def render_view(request):
    print('masuk ke render view')

    if request.method == "GET":
        print('auah gelap')
        # import pdb 
        # pdb.set_trace()
        tes_render()
        return JsonResponse({
            "status": "running"
        })

    if request.method != "POST":
        return JsonResponse(
            {"error": "POST required"},
            status=405
        )

    data = json.loads(request.body)
    print(data)


    result = render_video(
        caption=data.get("caption"),
        row_number = data.get("row_number"),
        title=data.get("title"),
        template=data.get("template"),
        texts=[
            data.get("text_1", ""),
            data.get("text_2", ""),
            data.get("text_3", ""),
            data.get("text_4", ""),
            data.get("text_5", "")
        ],
        asset_keyword=data.get("asset_keyword", ""),
        music_mood=data.get("music_mood", "")
    )

    return JsonResponse(result)








def tes_render():

    result = render_video(
        caption='lkjjl',
        title='asdfsadf',
        template='Educational',
        texts=[
            'Text 1',
            'Text 2',
            'Text 3',
            'Text 4',
            'Text 5'
        ],
        asset_keyword='ocean',
        music_mood='relaxing'
    )

    return JsonResponse(result)