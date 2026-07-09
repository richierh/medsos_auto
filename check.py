from scripts.logging_app import *
from dotenv import load_dotenv
import os

def main():
    print("Hello from automation-app!")


def test():

    logging.info("Application started dd")
    logging.warning("Low disk space")
    logging.error("Database connection failed")



    logger = logging.getLogger(__name__)

    try:
        result = 10 / 0
    except Exception:
        logger.exception("Unexpected error")

    logger.info(...)
    logger.warning(...)
    logger.error(...)
    logger.exception(...)


def test_env():

    load_dotenv()

    pexels_key = os.getenv("PEXELS_API_KEY")
    pixabay_key = os.getenv("PIXABAY_API_KEY")
    nuelink_key = os.getenv("NUELINK_API_KEY")
    google_key = os.getenv("GOOGLE_CREDENTIALS_FILE")
    videos_path_out = os.getenv("OUTPUT_VIDEO_DIR")
    videos_path_assets = os.getenv('ASSET_VIDEO_DIR')
    images_path_assets= os.getenv('ASSET_IMAGE_DIR')
    musics_path_assets= os.getenv('ASSET_MUSIC_DIR')




    BASE_DIR =os.getcwd()
    videos_dir = os.path.join(BASE_DIR,videos_path_out)
    videos_assdir = os.path.join(BASE_DIR,videos_path_assets)




    print(pexels_key)
    print(pixabay_key)
    print(nuelink_key)
    print(google_key)
    # print('hj')
    print(BASE_DIR)
    print(videos_dir)
    print(videos_assdir)


if __name__ == "__main__":
    # test()
    test_env()
    # main()
