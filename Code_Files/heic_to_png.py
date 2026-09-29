# pip install pillow pillow-heif
# python heic_to_png.py "C:\Users\Casper\Pictures\Receipts"
# C:\Users\Casper\Pictures\Receipts\PNG


import argparse
from pathlib import Path

from PIL import Image
from pillow_heif import register_heif_opener


def convert_heic_to_png(input_folder: Path, output_folder: Path, recursive: bool = False):
    """
    Convert all HEIC files in input_folder to PNG files in output_folder.

    Parameters
    ----------
    input_folder : Path
        Folder containing HEIC files.
    output_folder : Path
        Folder where PNG files will be saved.
    recursive : bool
        If True, search subfolders recursively.
    """

    register_heif_opener()

    if not input_folder.exists():
        raise FileNotFoundError(f"Input folder does not exist: {input_folder}")

    if not input_folder.is_dir():
        raise NotADirectoryError(f"Input path is not a folder: {input_folder}")

    output_folder.mkdir(parents=True, exist_ok=True)

    if recursive:
        files = [
            file
            for file in input_folder.rglob("*")
            if file.is_file() and file.suffix.lower() == ".heic"
        ]
    else:
        files = [
            file
            for file in input_folder.iterdir()
            if file.is_file() and file.suffix.lower() == ".heic"
        ]

    if not files:
        print(f"No HEIC files found in: {input_folder}")
        return

    print(f"Found {len(files)} HEIC file(s).")
    print(f"Output folder: {output_folder}")
    print()

    converted = 0
    failed = 0

    for index, heic_file in enumerate(files, start=1):
        try:
            if recursive:
                relative_path = heic_file.relative_to(input_folder)
                png_file = output_folder / relative_path.with_suffix(".png")
                png_file.parent.mkdir(parents=True, exist_ok=True)
            else:
                png_file = output_folder / f"{heic_file.stem}.png"

            with Image.open(heic_file) as image:
                # Convert to RGB/RGBA if necessary
                if image.mode not in ("RGB", "RGBA"):
                    image = image.convert("RGB")

                image.save(png_file, format="PNG")

            converted += 1
            print(
                f"[{index}/{len(files)}] "
                f"{heic_file.name} -> {png_file.name}"
            )

        except Exception as e:
            failed += 1
            print(f"[ERROR] {heic_file}: {e}")

    print()
    print("=" * 50)
    print("Conversion complete")
    print(f"Successfully converted : {converted}")
    print(f"Failed                 : {failed}")
    print(f"Total HEIC files       : {len(files)}")
    print(f"Output folder          : {output_folder}")
    print("=" * 50)


def main():
    parser = argparse.ArgumentParser(
        description="Convert all HEIC images in a folder to PNG."
    )

    parser.add_argument(
        "input_folder",
        type=Path,
        help="Folder containing HEIC images."
    )

    parser.add_argument(
        "output_folder",
        type=Path,
        nargs="?",
        default=None,
        help=(
            "Folder where converted PNG images will be saved. "
            "Default: <input_folder>/PNG"
        )
    )

    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="Search for HEIC files in all subfolders."
    )

    args = parser.parse_args()

    input_folder = args.input_folder

    if args.output_folder is None:
        output_folder = input_folder / "PNG"
    else:
        output_folder = args.output_folder

    convert_heic_to_png(
        input_folder=input_folder,
        output_folder=output_folder,
        recursive=args.recursive
    )


if __name__ == "__main__":
    main()