from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

def create_image_cards(news_items, captions, output_dir):
    for idx, (item, caption) in enumerate(zip(news_items, captions), 1):
        img = Image.new('RGB', (800, 600), color='white')
        d = ImageDraw.Draw(img)

        title = item["title"]
        font = ImageFont.load_default()

        lines = textwrap.wrap(title, width=40)
        y_text = 100
        for line in lines:
            d.text((50, y_text), line, fill="black", font=font)
            y_text += 30

        image_path = os.path.join(output_dir, f"post_{idx}.jpg")
        text_path = os.path.join(output_dir, f"post_{idx}.txt")

        img.save(image_path)
        with open(text_path, "w", encoding="utf-8") as f:
            f.write(caption)
