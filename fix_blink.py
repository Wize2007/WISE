from PIL import Image

normal_path = r"character\neutral\neutral.png"
blink_path = r"character\neutral\animation\blink.png"

# Read the normal WISE image
normal = Image.open(normal_path).convert("RGBA")

# Read the blink image
blink = Image.open(blink_path).convert("RGBA")

# Target canvas = normal WISE dimensions
target_width, target_height = normal.size

# Keep the blink image's proportions
blink.thumbnail(
    (target_width, target_height),
    Image.Resampling.LANCZOS
)

# Create a transparent canvas
canvas = Image.new(
    "RGBA",
    (target_width, target_height),
    (0, 0, 0, 0)
)

# Center the blink image
x = (target_width - blink.width) // 2
y = (target_height - blink.height) // 2

canvas.paste(
    blink,
    (x, y),
    blink
)

# Save the corrected blink image
canvas.save(
    blink_path,
    "PNG"
)

print("BLINK FIXED!")
print("NORMAL SIZE:", normal.size)
print("NEW BLINK SIZE:", canvas.size)

from PIL import Image

normal_path = r"character\neutral\neutral.png"
blink_path = r"character\neutral\animation\blink.png"

# Load images
normal = Image.open(normal_path).convert("RGBA")
blink = Image.open(blink_path).convert("RGBA")

# Get the actual visible area of the blink image
bbox = blink.getbbox()

if bbox is None:
    print("ERROR: Blink image is completely transparent.")
    exit()

print("Original blink bbox:", bbox)

# Crop away empty transparent space
blink_cropped = blink.crop(bbox)

print("Cropped blink size:", blink_cropped.size)

# Resize the cropped blink artwork to the same
# height as the normal WISE image.
target_width = normal.width
target_height = normal.height

blink_cropped = blink_cropped.resize(
    (target_width, target_height),
    Image.Resampling.LANCZOS
)

# Create a new canvas exactly matching normal WISE
fixed_blink = Image.new(
    "RGBA",
    normal.size,
    (0, 0, 0, 0)
)

# Put the corrected blink artwork onto the canvas
fixed_blink.paste(
    blink_cropped,
    (0, 0),
    blink_cropped
)

# Save the corrected blink
fixed_blink.save(
    blink_path,
    "PNG"
)

print("BLINK FIXED!")
print("Normal size:", normal.size)
print("New blink size:", fixed_blink.size)
print("New blink bbox:", fixed_blink.getbbox())