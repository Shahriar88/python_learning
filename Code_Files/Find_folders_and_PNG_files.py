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
    
    
    
    
    
# =====================================================
# Function
# Plot selected images as subplots
# Main Title   = image file name
# Subtitle     = folder name
# =====================================================
    
    
from pathlib import Path
import math
import matplotlib.pyplot as plt
from PIL import Image


def plot_matching_images(
    parent_folder="executed_notebooks",
    folder_start_with="E",
    image_start_with="gt_vs_pred_raw_idx3",
    ncols=3,
    fig_scale_x=5,
    fig_scale_y=5.5,
    row_gap=0.15,
    save_image=False,
    save_folder="combined_plots",
    dpi=300,
):
    """
    Plot matching images from folders as subplots.

    Parameters
    ----------
    parent_folder : str
        Parent directory containing experiment folders.

    folder_start_with : str
        Only use folders whose names start with this text.

    image_start_with : str
        Only use image files whose names start with this text.

    ncols : int
        Number of subplot columns.

    fig_scale_x : float
        Width multiplier per column.

    fig_scale_y : float
        Height multiplier per row.

    row_gap : float
        Vertical spacing between rows.

    save_image : bool
        If True, save the combined subplot image.

    save_folder : str
        Folder to save combined figure.

    dpi : int
        Save resolution.
    """

    # -----------------------------------------
    # Parent path
    # -----------------------------------------
    parent = Path(parent_folder)

    # -----------------------------------------
    # Get matching folders
    # -----------------------------------------
    folders = sorted(
        [
            p for p in parent.iterdir()
            if p.is_dir() and p.name.startswith(folder_start_with)
        ]
    )

    # -----------------------------------------
    # Collect matching images
    # -----------------------------------------
    matches = []

    for folder in folders:
        imgs = sorted(folder.glob(f"{image_start_with}*.png"))

        for img in imgs:
            matches.append((folder.name, img))

    print(f"Total matched images: {len(matches)}")

    # -----------------------------------------
    # No matches
    # -----------------------------------------
    if len(matches) == 0:
        print("No matching images found.")
        return

    # -----------------------------------------
    # Grid size
    # -----------------------------------------
    n = len(matches)
    nrows = math.ceil(n / ncols)

    # -----------------------------------------
    # Create figure
    # -----------------------------------------
    fig, axes = plt.subplots(
        nrows,
        ncols,
        figsize=(fig_scale_x * ncols, fig_scale_y * nrows)
    )

    # Make iterable
    if nrows == 1 and ncols == 1:
        axes = [axes]
    elif nrows == 1 or ncols == 1:
        axes = list(axes)
    else:
        axes = axes.flatten()

    # -----------------------------------------
    # Plot images
    # -----------------------------------------
    for ax, (folder_name, img_path) in zip(axes, matches):

        img = Image.open(img_path)

        ax.imshow(img)

        # Main title = file name
        ax.set_title(
            img_path.name,
            fontsize=10,
            pad=18,
            fontweight="bold"
        )

        # Subtitle = folder name
        ax.text(
            0.5,
            1.01,
            folder_name,
            transform=ax.transAxes,
            ha="center",
            va="bottom",
            fontsize=9
        )

        ax.axis("off")

    # Hide unused cells
    for ax in axes[len(matches):]:
        ax.axis("off")

    plt.tight_layout()
    fig.subplots_adjust(hspace=row_gap)

    # -----------------------------------------
    # Save figure
    # -----------------------------------------
    if save_image:
        save_dir = Path(save_folder)
        save_dir.mkdir(parents=True, exist_ok=True)

        save_name = f"{image_start_with}_combined.png"
        save_path = save_dir / save_name

        plt.savefig(save_path, dpi=dpi, bbox_inches="tight")
        print(f"Saved: {save_path}")

    plt.show()
