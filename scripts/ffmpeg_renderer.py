import json
import os
import subprocess

import sys
import textwrap

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

from PIL import ImageFont

font = ImageFont.truetype(
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    58
)

def wrap_by_pixels(text, font, max_width):
    words = text.split()

    lines = []
    line = ""

    for word in words:
        test = word if line == "" else line + " " + word

        if font.getlength(test) <= max_width:
            line = test
        else:
            lines.append(line)
            line = word

    if line:
        lines.append(line)

    return "\n".join(lines)


def wrap_text(text, width=25):
    return "\n".join(textwrap.wrap(text, width=width))

def escape_text(text):
    return (
        str(text)
        .replace("\\", "\\\\")
        .replace(":", "\\:")
        .replace("'", "\\'")
    )


def build_filter(template, title, texts,caption):
    title_cfg = template["title"]

    title_size = title_cfg["font_size"]
    title_y = title_cfg["position"]["y"]

    title_box = title_cfg["box"]

    title_box_color = title_box["color"].replace("#", "")
    title_box_opacity = title_box["opacity"]
    title_box_padding = title_box["padding"]




    text_size = template["text_blocks"]["font_size"]
    text_y = template['text_blocks']['position']['y']


    font_color = template["font"]["color"].replace("#", "")

    music_volume = template["music"]["volume"]

    scene_duration = template["scene"]["duration"]


    # color highlith
    highlight = template["highlight"]

    highlight_color = highlight["color"].replace("#","")
    highlight_opacity = highlight["opacity"]
    highlight_padding = highlight["padding"]


    # color caption 
    caption_cfg = template["caption"]

    caption_size = caption_cfg["font_size"]
    caption_y = caption_cfg["position"]["y"]
    caption_color = caption_cfg["color"].replace("#","")
    caption_bg = caption_cfg["background_color"].replace("#","")
    caption_opacity = caption_cfg["background_opacity"]

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
    y={title_y}:
    box=1:
    boxcolor={title_box_color}@{title_box_opacity}:
    boxborderw={title_box_padding}
    """
)

    # caption = wrap_text(caption, 35)
    caption = wrap_by_pixels(
            caption,
            font,
            template["text_blocks"]["max_width"]
        )
    caption = escape_text(caption)
    filters.append(
            f"""
                drawtext=
                fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:
                text='{caption}':
                fontsize={caption_size}:
                fontcolor={caption_color}:
                box=1:
                boxcolor={caption_bg}@{caption_opacity}:
                boxborderw={highlight_padding}:
                x=(w-text_w)/2:
                y={caption_y}        
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

        # text = wrap_text(text, 25)
        text = wrap_by_pixels(
            text,
            font,
            template["text_blocks"]["max_width"]
        )
        text = escape_text(text)

        filters.append(
            f"""
            drawtext=
            fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:
            text='{text}':
            fontsize={text_size}:
            fontcolor={font_color}:
            box=1:
            boxcolor={highlight_color}@{highlight_opacity}:
            boxborderw={highlight_padding}:
            x=(w-text_w)/2:
            y={text_y}:
            enable='between(t,{start_time},{end_time})'
            """)

    draw_filters = ",".join(
        filter.strip()
        for filter in filters)

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


def render_video_ffmpeg(
    template_path,
    src_video,
    src_music,
    out_video,
    title,
    texts,
    caption
):

    # template = load_template(template_path)
    template = get_template(template_path)
    print(template)

    filter_complex = build_filter(
        template,
        title,
        texts,
        caption
    )

    total_duration = (
        len([x for x in texts if x])
        * template["scene"]["duration"]
    )

    cmd = [
        "/usr/bin/ffmpeg",
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
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=900 
       )

    if result.returncode != 0:
        print(result.stderr)
        raise Exception("Render Failed")

    print("Render Success")
    print(out_video)

    return out_video


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
        "Aries, hari ini energi kamu sedang naik.",
        "Tapi jangan terlalu cepat mengambil keputusan.",
        "BuFokus ke satu hal yang paling penting dulu.",
        "Kalau kamu sabar, hasilnya bisa lebih baik.",
        "Aries hari ini perlu lebih tenang dalam mengambil keputusan. Jangan buru-buru, fokus dulu ke prioritas utama."
    ]

    caption="Aries hari ini perlu lebih tenang dalam mengambil keputusan. Jangan buru-buru, fokus dulu ke prioritas utama."

    render_video_ffmpeg(
        template_path=template_path,
        src_video=src_video,
        src_music=src_music,
        out_video=out_video,
        title=title,
        texts=texts,
        caption=caption
    )

