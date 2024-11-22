# CPS121 Project 3
# Written: 11/15/24 Matthew Brittain matt.brittain@gordon.edu
# 
# This program creates a collage of images using various transformations performed on images randomly grabbed from a folder.
# It first rescales the image so that it fits 1/9th of the canvas, then applies the transformations to each of the images.
# Once it finishes making the collage image it generates an html of the collage image and displays it in the browser.
##
# Change each occurrence of "_" in the list below to be "Y" or "N" to indicate
# whether or not the given transformation is implemented in your program.
#
#   Can be done using just getPixels()
#   N Altering colors of the image
#   Y Grayscale
#   N Making darker or lighter
#   Y Sepia-toned
#   Y Posterized
#   Need nested loops
#   Y Mirrorizing
#   Y Edge detection
#   N Chromakey (change background)
#   Y Blurring
#   Need nested loops and alter size or shape
#   Y Rotation
#   N Cropping
#   N Shifting
#   Other transformations
#   Y Automatic rescaling for every image used
#   Y Image flip
#   Y Negative Image
# ============================================================================

import GCPictureTools as pgt
import pygame as pg
import os, sys
import traceback
import random
from GCPictureTools import Picture

# ============================================================================
# ================ Start making changes after this comment ===================
# ============================================================================

# ---- SUPPORTING FUNCTIONS SHOULD GO HERE ----

def resize_image(image, new_width, new_height):
    """Resize the image to the given dimensions."""
    resized_image = Picture(new_width, new_height)
    for x in range(new_width):
        for y in range(new_height):
            src_x = int(x * image.getWidth() / new_width)
            src_y = int(y * image.getHeight() / new_height)
            resized_image.setColor(x, y, image.getColor(src_x, src_y))
    return resized_image

def grayscale_image(image):
    """Convert the image to grayscale."""
    grayscale_image = Picture(image.getWidth(), image.getHeight())
    for x in range(image.getWidth()):
        for y in range(image.getHeight()):
            color = image.getColor(x, y)
            gray_value = int(0.3 * color.r + 0.59 * color.g + 0.11 * color.b)
            gray_color = pg.Color(gray_value, gray_value, gray_value)
            grayscale_image.setColor(x, y, gray_color)
    return grayscale_image

def mirror_image(image):
    """Mirror the image."""
    mirrored_image = Picture(image.getWidth(), image.getHeight())
    for x in range(image.getWidth()):
        for y in range(image.getHeight()):
            mirrored_image.setColor(image.getWidth() - 1 - x, y, image.getColor(x, y))
    return mirrored_image

def flip_image(image):
    """Flip the image upside down."""
    flipped_image = Picture(image.getWidth(), image.getHeight())
    for x in range(image.getWidth()):
        for y in range(image.getHeight()):
            flipped_image.setColor(x, image.getHeight() - 1 - y, image.getColor(x, y))
    return flipped_image

def negative_image(image):
    """Apply negative effect to the image."""
    negative_image = Picture(image.getWidth(), image.getHeight())
    for x in range(image.getWidth()):
        for y in range(image.getHeight()):
            color = image.getColor(x, y)
            negative_color = pg.Color(255 - color.r, 255 - color.g, 255 - color.b)
            negative_image.setColor(x, y, negative_color)
    return negative_image

def sepia_image(image):
    """Apply sepia effect to the image."""
    sepia_image = Picture(image.getWidth(), image.getHeight())
    for x in range(image.getWidth()):
        for y in range(image.getHeight()):
            color = image.getColor(x, y)
            tr = int(0.393 * color.r + 0.769 * color.g + 0.189 * color.b)
            tg = int(0.349 * color.r + 0.686 * color.g + 0.168 * color.b)
            tb = int(0.272 * color.r + 0.534 * color.g + 0.131 * color.b)
            sepia_color = pg.Color(min(tr, 255), min(tg, 255), min(tb, 255))
            sepia_image.setColor(x, y, sepia_color)
    return sepia_image

def posterize_image(image):
    """Apply posterize effect to the image."""
    posterize_image = Picture(image.getWidth(), image.getHeight())
    for x in range(image.getWidth()):
        for y in range(image.getHeight()):
            color = image.getColor(x, y)
            r = (color.r // 64) * 64
            g = (color.g // 64) * 64
            b = (color.b // 64) * 64
            posterize_color = pg.Color(r, g, b)
            posterize_image.setColor(x, y, posterize_color)
    return posterize_image

def edge_detection_image(image):
    """Apply edge detection to the image."""
    edge_image = Picture(image.getWidth(), image.getHeight())
    for x in range(1, image.getWidth() - 1):
        for y in range(1, image.getHeight() - 1):
            color = image.getColor(x, y)
            right_color = image.getColor(x + 1, y)
            bottom_color = image.getColor(x, y + 1)
            edge_r = min(abs(color.r - right_color.r) + abs(color.r - bottom_color.r), 255)
            edge_g = min(abs(color.g - right_color.g) + abs(color.g - bottom_color.g), 255)
            edge_b = min(abs(color.b - right_color.b) + abs(color.b - bottom_color.b), 255)
            edge_color = pg.Color(edge_r, edge_g, edge_b)
            edge_image.setColor(x, y, edge_color)
    return edge_image

def blur_image(image):
    """Apply blur effect to the image."""
    blur_image = Picture(image.getWidth(), image.getHeight())
    for x in range(1, image.getWidth() - 1):
        for y in range(1, image.getHeight() - 1):
            colors = [
                image.getColor(x - 1, y - 1), image.getColor(x, y - 1), image.getColor(x + 1, y - 1),
                image.getColor(x - 1, y), image.getColor(x, y), image.getColor(x + 1, y),
                image.getColor(x - 1, y + 1), image.getColor(x, y + 1), image.getColor(x + 1, y + 1)
            ]
            r = sum(color.r for color in colors) // 9
            g = sum(color.g for color in colors) // 9
            b = sum(color.b for color in colors) // 9
            blur_color = pg.Color(r, g, b)
            blur_image.setColor(x, y, blur_color)
    return blur_image

def create_collage():
    # Create a blank canvas
    canvas = Picture(950, 700, "white")

    # Get a list of all image files in the "Photos" folder
    photos_folder = 'Photos'
    image_files = [f for f in os.listdir(photos_folder) if os.path.isfile(os.path.join(photos_folder, f))]

    # Scale dimensions for the images to fit 1/9th of the canvas
    new_width = canvas.getWidth() // 3
    new_height = canvas.getHeight() // 3

    # Define transformations
    transformations = [
        lambda img: img,  # Original
        grayscale_image,  # Grayscale
        mirror_image,  # Mirroring
        flip_image,  # Flipping upside down
        negative_image,  # Negative
        sepia_image,  # Sepia
        posterize_image,  # Posterize
        edge_detection_image,  # Edge detection
        blur_image,  # Blur
    ]

    # Apply transformations and place images on the canvas
    for i, transform in enumerate(transformations):
        # Randomly select an image file
        selected_image_file = random.choice(image_files)
        original_image = Picture(os.path.join(photos_folder, selected_image_file))

        # Resize the original image
        original_image = resize_image(original_image, new_width, new_height)

        # Apply the transformation
        transformed_image = transform(original_image)

        # Calculate position on the canvas
        x = (i % 3) * new_width
        y = (i // 3) * new_height

        # Copy the transformed image onto the canvas
        transformed_image.copyInto(canvas, x, y)

    # Save the canvas as a JPEG file
    canvas.save('collage.jpg')

    return 'collage.jpg'

def create_webpage(image_file, webpage_file):
    """Create web page that contains the collage."""
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Collage Result</title>
        <style>
            body {{
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                font-family: Arial, sans-serif;
                background-color: #fff;
                background-image: 
                    linear-gradient(45deg, #000 25%, transparent 25%, transparent 75%, #000 75%, #000),
                    linear-gradient(45deg, #000 25%, transparent 25%, transparent 75%, #000 75%, #000);
                background-size: 40px 40px;
                background-position: 0 0, 20px 20px;
            }}
            h1 {{
                margin-bottom: 40px;
                background: linear-gradient(to right, red, orange, yellow, green, blue, indigo, violet);
                -webkit-background-clip: text;
                color: transparent;
            }}
            img {{
                max-width: 50%;
                height: auto;
            }}
        </style>
    </head>
    <body>
        <h1>Behold, my creation</h1>
        <img src="{image_file}" alt="Collage">
    </body>
    </html>
    """
    with open(webpage_file, 'w') as file:
        file.write(html_content)

if __name__ == "__main__":
    collage_file = create_collage()
    create_webpage(collage_file, 'collage.html')