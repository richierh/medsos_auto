import sys
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent

# tambahkan folder yang berisi package automation_dj
sys.path.insert(0, str(BASE_DIR / "automation_dj"))


os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "automation_dj.settings"
)

from django.core.management import execute_from_command_line


def main_app():
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main_app()