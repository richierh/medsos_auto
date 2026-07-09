import requests
from pathlib import Path
import hashlib
from dotenv import load_dotenv
import os

load_dotenv()

CACHE_DIR = Path("cache/music")
CACHE_DIR.mkdir(parents=True, exist_ok=True)

JAMENDO_CLIENT_ID = os.getenv("JAMENDO_CLIENT_ID")
print(JAMENDO_CLIENT_ID)


def get_cache_path(keyword: str):
    filename = hashlib.md5(keyword.encode()).hexdigest() + ".mp3"
    return CACHE_DIR / filename


def fetch_from_jamendo(keyword: str, min_duration: int = 0):

    load_dotenv()


    JAMENDO_CLIENT_ID = os.getenv("JAMENDO_CLIENT_ID")
    print(JAMENDO_CLIENT_ID)


    url = "https://api.jamendo.com/v3.0/tracks/"

    params = {
        "client_id": JAMENDO_CLIENT_ID,
        "format": "json",
        "limit": 20,
        "tags": keyword,
        "audioformat": "mp32"
    }

    res = requests.get(
        url,
        params=params,
        timeout=10
    )
    print(res.status_code)
    print(JAMENDO_CLIENT_ID)
    print('test')
    print(res.text)


    data = res.json()

    tracks = data.get("results", [])

    if not tracks:
        return None

    if min_duration > 0:
        suitable = [
            t for t in tracks
            if int(t.get("duration", 0)) >= min_duration
        ]

        if suitable:
            return suitable[0]["audio"]

    return tracks[0]["audio"]


def download_music(url: str, path: Path):

    r = requests.get(
        url,
        stream=True,
        timeout=30
    )

    with open(path, "wb") as f:
        for chunk in r.iter_content(
            chunk_size=1024 * 1024
        ):
            f.write(chunk)


def get_music(
    mood: str,
    duration: int = 0
):

    cache_key = f"{mood}_{duration}"

    cache_path = get_cache_path(
        cache_key
    )

    # CACHE
    if cache_path.exists():
        print("CACHE HIT")
        return str(cache_path)

    # JAMENDO
    print("SEARCH JAMENDO")

    music_url = fetch_from_jamendo(
        mood,
        duration
    )
    BASE_DIR = Path(__file__).resolve().parent.parent

    ASSET_DIR = BASE_DIR / "assets" / "musics"


    # LOCAL FALLBACK
    if not music_url:

        print("FALLBACK LOCAL")
        local = ASSET_DIR / "default.mp3"
        print(local)

        # local = (
        #     Path("assets/music")
        #     / "default.mp3"
        # )

        if local.exists():
            return str(local)

        raise Exception(
            "No music found anywhere"
        )

    # DOWNLOAD
    print("DOWNLOADING MUSIC")

    download_music(
        music_url,
        cache_path
    )

    return str(cache_path)

if __name__ == "__main__":

    path = get_music("", 60)

    print("RESULT:", path)
    print('hhh')