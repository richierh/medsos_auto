import json
import os
import subprocess

import sys

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

# sys.path.insert(0, BASE_DIR)
sys.path.insert(
    0,
    os.path.join(BASE_DIR, "automation_dj")
)

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "automation_dj.settings"
)

import django
django.setup()

from setting_template.models import VideoTemplate

def get_template(template_name):
    template = VideoTemplate.objects.get(
        name=template_name
    )

    return template.template_data


def load_template(template_path):
    with open(template_path, "r", encoding="utf-8") as f:
        return json.load(f)


def escape_text(text):
    return (
        str(text)
        .replace("\\", "\\\\")
        .replace(":", "\\:")
        .replace("'", "\\'")
    )


def build_filter(template, title, texts):

    title_size = template["title"]["font_size"]
    title_y = template["title"]["position"]["y"]

    text_size = template["text_blocks"]["font_size"]

    font_color = template["font"]["color"].replace("#", "")

    music_volume = template["music"]["volume"]

    scene_duration = template["scene"]["duration"]

    filters = []

    # =========================
    # TITLE
    # =========================

    title = escape_text(title)

    filters.append(
        f"""
        drawtext=
        fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:
        text='{title}':
        fontsize={title_size}:
        fontcolor={font_color}:
        x=(w-text_w)/2:
        y={title_y}
        """
    )

    # =========================
    # TEXT SCENES
    # =========================

    for idx, text in enumerate(texts):

        if not text:
            continue

        start_time = idx * scene_duration
        end_time = start_time + scene_duration

        text = escape_text(text)

        filters.append(
            f"""
            drawtext=
            fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:
            text='{text}':
            fontsize={text_size}:
            fontcolor={font_color}:
            x=(w-text_w)/2:
            y=700:
            enable='between(t,{start_time},{end_time})'
            """
        )

    draw_filters = ",".join(
        filter.strip()
        for filter in filters
    )

    filter_complex = f"""
    [0:v]
    scale=1080:1920:force_original_aspect_ratio=increase,
    crop=1080:1920,

    drawbox=
    x=0:
    y=0:
    w=iw:
    h=ih:
    color=white@0.10:
    t=fill,

    {draw_filters}

    [v];

    [1:a]
    volume={music_volume}
    [a]
    """

    return filter_complex


def render_video(
    template_path,
    src_video,
    src_music,
    out_video,
    title,
    texts
):

    # template = load_template(template_path)
    template = get_template(template_path)

    filter_complex = build_filter(
        template,
        title,
        texts
    )

    total_duration = (
        len([x for x in texts if x])
        * template["scene"]["duration"]
    )

    cmd = [
        "ffmpeg",
        "-y",

        "-stream_loop", "-1",
        "-i", src_video,

        "-stream_loop", "-1",
        "-i", src_music,

        "-filter_complex",
        filter_complex,

        "-map", "[v]",
        "-map", "[a]",

        "-t", str(total_duration),

        "-c:v", "libx264",
        "-preset", "medium",

        "-c:a", "aac",
        "-b:a", "192k",

        "-pix_fmt", "yuv420p",

        out_video
    ]

    print("=" * 50)
    print("RUNNING FFMPEG")
    print("=" * 50)

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(result.stderr)
        raise Exception("Render Failed")

    print("Render Success")
    print(out_video)


if __name__ == "__main__":

    BASE_DIR = os.getcwd()

    template_path = os.path.join(
        BASE_DIR,
        "templates",
        "educational.json"
    )
    template_path = 'Educational'

    src_video = os.path.join(
        BASE_DIR,
        "assets",
        "videos",
        "5873948-uhd_4096_2160_30fps.mp4"
    )

    src_music = os.path.join(
        BASE_DIR,
        "assets",
        "musics",
        "nickype-royal-guard-144997.mp3"
    )

    out_video = os.path.join(
        BASE_DIR,
        "outputs","videos",
        "result.mp4"
    )

    title = "5 TIPS BELAJAR PYTHON"

    texts = [
        "Mulai dari dasar Python",
        "Latihan coding setiap hari",
        "Buat project kecil",
        "Pelajari dokumentasi resmi",
        "Konsisten selama 30 hari"
    ]

    render_video(
        template_path=template_path,
        src_video=src_video,
        src_music=src_music,
        out_video=out_video,
        title=title,
        texts=texts
    )