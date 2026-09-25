from PIL import Image

normal_path = r"character\neutral\neutral.png"
blink_path = r"character\neutral\animation\blink.png"

# Load images
normal = Image.open(normal_path).convert("RGBA")
blink = Image.open(blink_path).convert("RGBA")

# Find the visible blink artwork
bbox = blink.getbbox()

if bbox is None:
    print("ERROR: Blink image is empty.")
    exit()

# Crop only the visible artwork
blink_cropped = blink.crop(bbox)

print("Blink artwork before scaling:", blink_cropped.size)

# --------------------------------------------------
# IMPORTANT:
# Preserve the original aspect ratio.
# We only scale based on HEIGHT.
# --------------------------------------------------

target_height = normal.height

original_width = blink_cropped.width
original_height = blink_cropped.height

scale = target_height / original_height

new_width = round(
    original_width * scale
)

new_height = target_height

print(
    "New proportional size:",
    new_width,
    "x",
    new_height
)

blink_cropped = blink_cropped.resize(
    (new_width, new_height),
    Image.Resampling.LANCZOS
)

# --------------------------------------------------
# Create the exact same canvas as normal WISE
# --------------------------------------------------

canvas = Image.new(
    "RGBA",
    normal.size,
    (0, 0, 0, 0)
)

# Center horizontally
x = (
    normal.width - blink_cropped.width
) // 2

# Start at the top
y = 0

canvas.paste(
    blink_cropped,
    (x, y),
    blink_cropped
)

# Save
canvas.save(
    blink_path,
    "PNG"
)

print()
print("BLINK FIXED PROPORTIONALLY!")
print("Normal:", normal.size)
print("Blink:", canvas.size)
print("Blink bbox:", canvas.getbbox())