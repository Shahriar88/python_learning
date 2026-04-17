# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 22:57:43 2026

@author: kec994
"""
# =====================================================
# Find folders and PNG files inside executed_notebooks
# =====================================================

from pathlib import Path

# Parent directory containing experiment folders
parent = Path("executed_notebooks")

# Only use folders whose names start with this text
folder_start_with = "E"

# Get matching folders
folders = [
    p for p in parent.iterdir()
    if p.is_dir() and p.name.startswith(folder_start_with)
]

# Show matching folders
print("Matched folders:")
print(folders)


# =====================================================
# Collect all PNG files from those folders
# =====================================================

png_files = []

for folder in folders:
    # Add all png files from each folder
    png_files.extend(folder.glob("*.png"))

# Show all png files found
print("\nPNG files:")
print(png_files)



# =====================================================
# Plot selected images as subplots
# Main Title   = image file name
# Subtitle     = folder name
# =====================================================

from pathlib import Path
import math
import matplotlib.pyplot as plt
from PIL import Image

# Parent folder
parent = Path("executed_notebooks")

# Folder prefix filter
folder_start_with = "E"

# Image prefix filter
# Example:
# gt_vs_pred_raw_idx3
# gt_vs_pred_crf_idx3
image_start_with = "gt_vs_pred_raw_idx3"


# -----------------------------------------------------
# Get matching folders
# -----------------------------------------------------
folders = sorted(
    [p for p in parent.iterdir()
     if p.is_dir() and p.name.startswith(folder_start_with)]
)


# -----------------------------------------------------
# Collect matching images
# Store:
# (folder_name, image_path)
# -----------------------------------------------------
matches = []

for folder in folders:
    imgs = sorted(folder.glob(f"{image_start_with}*.png"))

    for img in imgs:
        matches.append((folder.name, img))


print(f"\nTotal matched images: {len(matches)}")


# -----------------------------------------------------
# Plot images
# -----------------------------------------------------
if len(matches) == 0:
    print("No matching images found.")

else:
    # Number of images
    n = len(matches)

    # Number of subplot columns
    ncols = 3

    # Auto-compute rows
    nrows = math.ceil(n / ncols)

    # Create subplot grid
    fig, axes = plt.subplots(
        nrows,
        ncols,
        figsize=(5 * ncols, 5.5 * nrows)
    )

    # Make axes iterable
    if nrows == 1 and ncols == 1:
        axes = [axes]
    else:
        axes = axes.flatten()

    # -------------------------------------------------
    # Plot each image
    # -------------------------------------------------
    for ax, (folder_name, img_path) in zip(axes, matches):

        # Open image
        img = Image.open(img_path)

        # Show image
        ax.imshow(img)

        # Main title = image file name
        ax.set_title(
            img_path.name,
            fontsize=10,
            pad=18,
            fontweight="bold"
        )

        # Subtitle = folder name
        ax.text(
            0.5, 1.01,
            folder_name,
            transform=ax.transAxes,
            ha="center",
            va="bottom",
            fontsize=9
        )

        # Hide axis ticks
        ax.axis("off")

    # -------------------------------------------------
    # Hide unused subplot cells
    # -------------------------------------------------
    for ax in axes[len(matches):]:
        ax.axis("off")

    # Improve spacing
    plt.tight_layout()

    # Show figure
    plt.show()