import requests
from pathlib import Path
import hashlib
from dotenv import load_dotenv
import os

load_dotenv()

CACHE_DIR = Path("cache/videos")
CACHE_DIR.mkdir(parents=True, exist_ok=True)

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY")


def get_cache_path(keyword: str):
    filename = hashlib.md5(keyword.encode()).hexdigest() + ".mp4"
    return CACHE_DIR / filename


def fetch_from_pexels(keyword: str, target_duration: int = 60):
    url = "https://api.pexels.com/videos/search"

    headers = {
        "Authorization": PEXELS_API_KEY
    }

    params = {
        "query": keyword,
        "per_page": 15
    }

    res = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=10
    )

    res.raise_for_status()

    data = res.json()
    videos = data.get("videos", [])

    if not videos:
        return None

    valid_videos = [
        v for v in videos
        if v.get("duration", 0) >= 10
    ]

    if not valid_videos:
        valid_videos = videos

    selected = min(
        valid_videos,
        key=lambda v: abs(
            v.get("duration", 0) - target_duration
        )
    )

    files = selected.get("video_files", [])

    if not files:
        return None

    best = max(
        files,
        key=lambda f: f.get("width", 0)
    )

    return {
        "url": best["link"],
        "duration": selected.get("duration", 0)
    }


def fetch_from_pixabay(keyword: str, target_duration: int = 60):
    url = "https://pixabay.com/api/videos/"

    params = {
        "key": PIXABAY_API_KEY,
        "q": keyword,
        "per_page": 15
    }

    res = requests.get(
        url,
        params=params,
        timeout=10
    )

    res.raise_for_status()

    data = res.json()

    hits = data.get("hits", [])

    if not hits:
        return None

    selected = min(
        hits,
        key=lambda h: abs(
            h.get("duration", 0) - target_duration
        )
    )

    return {
        "url": selected["videos"]["medium"]["url"],
        "duration": selected.get("duration", 0)
    }


def download_video(url: str, path: Path):
    r = requests.get(
        url,
        stream=True,
        timeout=30
    )

    r.raise_for_status()

    with open(path, "wb") as f:
        for chunk in r.iter_content(
            chunk_size=1024 * 1024
        ):
            f.write(chunk)


def get_background_video(
    keyword: str,
    target_duration: int = 60
):
    cache_path = get_cache_path(keyword)

    if cache_path.exists():
        print("CACHE HIT")

        return {
            "path": str(cache_path),
            "duration": None
        }

    print("TRY PEXELS")

    result = fetch_from_pexels(
        keyword,
        target_duration
    )

    if not result:
        print("TRY PIXABAY")

        result = fetch_from_pixabay(
            keyword,
            target_duration
        )
        BASE_DIR = Path(__file__).resolve().parent.parent

        VIDEO_DIR = BASE_DIR / "assets" / "videos"
        IMAGE_DIR = BASE_DIR / "assets" / "images"

    if not result:
        print("FALLBACK LOCAL")
        local = VIDEO_DIR / "default.mp4"
        print(local)

        # local = Path(
        #     "assets/videos/default.mp4"
        # )

        if local.exists():
            return {
                "path": str(local),
                "duration": None
            }

        raise Exception(
            "No video found anywhere"
        )

    if not result:
        print("FALLBACK LOCAL")
        local = IMAGE_DIR / "default.jpg"
        print(local)

        # local = Path(
        #     "assets/videos/default.mp4"
        # )

        if local.exists():
            return {
                "path": str(local),
                "duration": None
            }

        raise Exception(
            "No images found anywhere"
        )


    print("DOWNLOADING")

    download_video(
        result["url"],
        cache_path
    )

    return {
        "path": str(cache_path),
        "duration": result["duration"]
    }