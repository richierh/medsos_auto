from fileinput import filename
from pathlib import Path
from datetime import datetime
from scripts.asset_service import get_background_video 
from scripts.music_service import get_music
from scripts.ffmpeg_renderer import render_video_ffmpeg
from scripts.ffmpeg_renderer import get_template

# five parameters to the function of render_video
def render_video(
    caption=None,
    row_number=None,
    title ='oalah',
    template = 'Educational',
    texts=['dd','dfd','dfdf','dfdf','dfdf'],
    asset_keyword='ocean',
    music_mood='sports'):

    if texts is None:
        texts = []

    # Ambil template
    print(template)
    print('tes disini')
    template_data = get_template(template)

    scene_duration = template_data["scene"]["duration"]

    # Hitung text yang tidak kosong
    active_texts = [
        t for t in texts
        if t and str(t).strip()
    ]

    # Durasi final video
    total_duration = len(active_texts) * scene_duration

    # Sesuai SOW minimal 30 detik
    if total_duration < 30:
        total_duration = 30

    # Sesuai SOW maksimal 60 detik
    if total_duration > 60:
        total_duration = 60

    print(f"Target Duration = {total_duration}s")

    # Cari background video



    video_asset_search = get_background_video(
        asset_keyword,
         target_duration=total_duration

    )
    video_asset = video_asset_search["path"]
    video_duration = video_asset_search["duration"]

    music_asset = get_music(
    mood=music_mood,
    duration=total_duration
            )

    print('berhasil kok gimana sih')


    filename = datetime.now().strftime("%Y%m%d_%H%M%S")
    BASE_DIR = Path(__file__).resolve().parent.parent
    print(BASE_DIR)
    output_path = f"{BASE_DIR}/outputs/videos/{filename}_{row_number}.mp4"
    print(output_path)
    print('test')


    render_video_ffmpeg(
    caption=caption,
    template_path=template,
    src_video=video_asset,
    src_music=music_asset,
    out_video=output_path,
    title=title,
    texts=texts
    )    
    print('berhasil kok gimana sih')

    # nanti panggil ffmpeg di sini
    print('hello')

    return {
        'row_number':row_number,
        "status": "success",
        "video_path": output_path,
        "preview_url": f"http://38.68.69.211:8080/video/{filename}_{row_number}.mp4",
        "duration": total_duration
    }