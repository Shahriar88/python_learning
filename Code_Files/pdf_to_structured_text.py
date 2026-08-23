import sys
from pathlib import Path

from docling.document_converter import DocumentConverter
from docling_core.types.doc import ImageRefMode


FIGURE_PLACEHOLDER = "<!-- FIGURE INTENTIONALLY EXCLUDED -->"


def convert_pdf(pdf_path: Path, converter: DocumentConverter) -> str:
    """
    Convert one PDF into structured Markdown.

    Text, headings, tables, equations, lists, and captions are retained
    when Docling can identify them. Images are replaced by a placeholder.
    """

    result = converter.convert(str(pdf_path))

    markdown = result.document.export_to_markdown(
        image_mode=ImageRefMode.PLACEHOLDER,
        image_placeholder=FIGURE_PLACEHOLDER,
    )

    parts = [
        "\n\n",
        "=" * 80,
        f"\nSOURCE PDF FILE: {pdf_path.name}\n",
        f"SOURCE PDF PATH: {pdf_path}\n",
        "=" * 80,
        "\n\n",
        markdown,
        "\n\n",
        "=" * 80,
        f"\nEND OF PDF: {pdf_path.name}\n",
        "=" * 80,
        "\n\n",
    ]

    return "".join(parts)


def write_output(
    destination_file: Path,
    content: str,
    operation: str,
) -> None:
    """Write content using replace or append mode."""

    destination_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    file_mode = "w" if operation == "replace" else "a"

    with destination_file.open(
        file_mode,
        encoding="utf-8",
        errors="replace",
    ) as file:
        file.write(content)


# ============================================================
# Read command-line arguments
# ============================================================

if len(sys.argv) not in {3, 4, 5}:
    raise SystemExit(
        "Usage:\n"
        "\n"
        "Single PDF file:\n"
        "  py pdf_to_structured_text.py "
        "Source_PDF Destination_File [single] [replace|append]\n"
        "\n"
        "Source folder with separate outputs:\n"
        "  py pdf_to_structured_text.py "
        "Source_Folder Destination_Folder "
        "[separate] [replace|append]\n"
        "\n"
        "Source folder with one combined output:\n"
        "  py pdf_to_structured_text.py "
        "Source_Folder Destination_File "
        "combine [replace|append]"
    )

source = Path(sys.argv[1]).resolve()
destination = Path(sys.argv[2]).resolve()

if not source.exists():
    raise SystemExit(
        f"Source file or source folder not found: {source}"
    )

# Select the default output mode.
if len(sys.argv) >= 4:
    output_mode = sys.argv[3].lower()
else:
    output_mode = "single" if source.is_file() else "separate"

# Select the default write mode.
operation = (
    sys.argv[4].lower()
    if len(sys.argv) == 5
    else "replace"
)

if output_mode not in {"single", "separate", "combine"}:
    raise SystemExit(
        "Output mode must be 'single', 'separate', or 'combine'."
    )

if operation not in {"replace", "append"}:
    raise SystemExit(
        "Write mode must be either 'replace' or 'append'."
    )


# ============================================================
# Validate source and destination types
# ============================================================

if source.is_file():

    if source.suffix.lower() != ".pdf":
        raise SystemExit(
            f"The source file is not a PDF: {source}"
        )

    if output_mode != "single":
        raise SystemExit(
            "Use output mode 'single' when the source is one PDF file."
        )

    if destination.exists() and destination.is_dir():
        raise SystemExit(
            "For a single source PDF, the destination must be a file."
        )

elif source.is_dir():

    if output_mode == "single":
        raise SystemExit(
            "Use 'separate' or 'combine' when the source is a folder."
        )

    if output_mode == "separate":
        if destination.exists() and destination.is_file():
            raise SystemExit(
                "In separate mode, the destination must be a folder."
            )

    if output_mode == "combine":
        if destination.exists() and destination.is_dir():
            raise SystemExit(
                "In combine mode, the destination must be a file."
            )

else:
    raise SystemExit(
        f"Unsupported source path: {source}"
    )


# ============================================================
# Initialize Docling
# ============================================================

print("Loading Docling...")
converter = DocumentConverter()


# ============================================================
# Single PDF file mode
# ============================================================

if output_mode == "single":

    print(f"Processing source PDF file: {source}")

    try:
        structured_text = convert_pdf(
            source,
            converter,
        )

        write_output(
            destination,
            structured_text,
            operation,
        )

        print("Processing complete.")
        print(f"Source PDF file: {source}")
        print(f"Destination file: {destination}")
        print(f"Write mode: {operation}")
        print(f"Characters written: {len(structured_text)}")

    except Exception as error:
        raise SystemExit(
            f"Failed to process {source}\n"
            f"Reason: {type(error).__name__}: {error}"
        )


# ============================================================
# Find PDFs recursively when source is a folder
# ============================================================

else:

    pdf_files = sorted(
        (
            path
            for path in source.rglob("*")
            if path.is_file()
            and path.suffix.lower() == ".pdf"
        ),
        key=lambda path: str(path).lower(),
    )

    if not pdf_files:
        raise SystemExit(
            f"No PDF files were found in source folder: {source}"
        )

    print(f"PDF files found: {len(pdf_files)}")

    successful = 0
    failed = 0


    # ========================================================
    # Separate output files
    # ========================================================

    if output_mode == "separate":

        destination.mkdir(
            parents=True,
            exist_ok=True,
        )

        for number, pdf_path in enumerate(
            pdf_files,
            start=1,
        ):
            relative_pdf_path = pdf_path.relative_to(source)

            destination_file = (
                destination / relative_pdf_path
            ).with_suffix(".md")

            print(
                f"\n[{number}/{len(pdf_files)}] "
                f"Processing source PDF file: {pdf_path}"
            )

            try:
                structured_text = convert_pdf(
                    pdf_path,
                    converter,
                )

                write_output(
                    destination_file,
                    structured_text,
                    operation,
                )

                successful += 1

                print(
                    f"Saved destination file: "
                    f"{destination_file}"
                )

            except Exception as error:
                failed += 1

                print(
                    f"Failed source PDF file: {pdf_path}\n"
                    f"Reason: {type(error).__name__}: {error}"
                )


    # ========================================================
    # One combined output file
    # ========================================================

    elif output_mode == "combine":

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        file_mode = (
            "w" if operation == "replace" else "a"
        )

        with destination.open(
            file_mode,
            encoding="utf-8",
            errors="replace",
        ) as combined_file:

            for number, pdf_path in enumerate(
                pdf_files,
                start=1,
            ):
                print(
                    f"\n[{number}/{len(pdf_files)}] "
                    f"Processing source PDF file: {pdf_path}"
                )

                try:
                    structured_text = convert_pdf(
                        pdf_path,
                        converter,
                    )

                    combined_file.write(structured_text)
                    combined_file.flush()

                    successful += 1

                    print(
                        f"Added to destination file: "
                        f"{destination}"
                    )

                except Exception as error:
                    failed += 1

                    print(
                        f"Failed source PDF file: {pdf_path}\n"
                        f"Reason: {type(error).__name__}: {error}"
                    )


    # ========================================================
    # Completion summary
    # ========================================================

    print("\nProcessing complete.")
    print(f"Source folder: {source}")
    print(f"PDF files found: {len(pdf_files)}")
    print(f"Successfully processed: {successful}")
    print(f"Failed: {failed}")
    print(f"Output mode: {output_mode}")
    print(f"Write mode: {operation}")
    print(f"Destination: {destination}")


# ============================================================
# Installation
# ============================================================

# Install Docling once:
# py -m pip install docling


# ============================================================
# Example commands
# ============================================================

# Read one source PDF file and replace one destination Markdown file:
# py .\pdf_to_structured_text.py ".\part1\paper1.pdf" ".\paper1.md"

# Read one source PDF file and explicitly replace one destination file:
# py .\pdf_to_structured_text.py ".\part1\paper1.pdf" ".\paper1.md" single replace

# Read one source PDF file and append it to one destination file:
# py .\pdf_to_structured_text.py ".\part1\paper1.pdf" ".\paper1.md" single append

# Read every PDF in the source folder and subfolders, then create one separate Markdown file per PDF in the destination folder:
# py .\pdf_to_structured_text.py ".\part1" ".\structured_papers"

# Same as above, with separate and replace modes explicitly specified:
# py .\pdf_to_structured_text.py ".\part1" ".\structured_papers" separate replace

# Read every PDF in the source folder and append each PDF to its corresponding separate destination Markdown file:
# py .\pdf_to_structured_text.py ".\part1" ".\structured_papers" separate append

# Read every PDF in the source folder and combine them into one destination Markdown file, replacing its previous contents:
# py .\pdf_to_structured_text.py ".\part1" ".\all_papers.md" combine replace

# Read every PDF in the source folder and append all extracted content to one existing destination Markdown file:
# py .\pdf_to_structured_text.py ".\part1" ".\all_papers.md" combine append