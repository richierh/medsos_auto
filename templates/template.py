import json

with open("templates/zodiac_dark.json") as f:
    template = json.load(f)

font_size = template["title"]["font_size"]
font_color = template["font"]["color"]

template_name = row["template"]

with open(f"templates/{template_name}.json") as f:
    template = json.load(f)