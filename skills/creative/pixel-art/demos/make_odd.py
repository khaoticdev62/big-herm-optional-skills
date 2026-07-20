from PIL import Image, ImageDraw
img = Image.new("RGBA", (17, 17), (0, 0, 0, 0))
d = ImageDraw.Draw(img)
d.rectangle([2, 2, 14, 14], fill=(200, 60, 60, 255))
d.rectangle([2, 2, 14, 14], outline=(20, 20, 20, 255))
img.save(r"C:/Users/thecr/AppData/Local/hermes/profiles/big-herm/skills/pixel-art/demos/real_odd.png")
print("wrote 17x17 with content")
