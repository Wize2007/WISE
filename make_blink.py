from PIL import Image

source = r"character\neutral\animation\blink_new.png"
output = r"character\neutral\animation\blink.png"

# Target dimensions of normal WISE
TARGET_WIDTH = 313
TARGET_HEIGHT = 893

# Open the new generated blink
image = Image.open(source).convert("RGBA")

print("Original blink:", image.size)

# ==================================================
# CROP TO THE SAME ASPECT RATIO AS NORMAL WISE
# ==================================================

target_ratio = TARGET_WIDTH / TARGET_HEIGHT

width, height = image.size
current_ratio = width / height

if current_ratio > target_ratio:

    # Image is too wide.
    # Crop equally from left and right.

    new_width = round(height * target_ratio)

    left = (width - new_width) // 2
    right = left + new_width

    image = image.crop(
        (left, 0, right, height)
    )

else:

    # Image is too tall.
    # Crop equally from top and bottom.

    new_height = round(width / target_ratio)

    top = (height - new_height) // 2
    bottom = top + new_height

    image = image.crop(
        (0, top, width, bottom)
    )

print("After proportional crop:", image.size)

# ==================================================
# RESIZE WITHOUT DISTORTING
# ==================================================

image = image.resize(
    (TARGET_WIDTH, TARGET_HEIGHT),
    Image.Resampling.LANCZOS
)

# Save the final blink
image.save(
    output,
    "PNG"
)

print()
print("BLINK CREATED SUCCESSFULLY!")
print("Final size:", image.size)