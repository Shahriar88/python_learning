#====================================== Replace Destination
import sys
from pathlib import Path
from pypdf import PdfReader

source = Path(sys.argv[1]).resolve()
destination = Path(sys.argv[2]).resolve()
reader = PdfReader(str(source))
parts = []
for index, page in enumerate(reader.pages, start=1):
    parts.append(f"\n\n===== PAGE {index} OF {len(reader.pages)} =====\n\n")
    parts.append(page.extract_text() or "")
destination.write_text("".join(parts), encoding="utf-8", errors="replace")
print(f"pages={len(reader.pages)} chars={sum(len(p) for p in parts)} output={destination}")





# Install dependency once:
# py -m pip install pypdf

# General command:
# py This_File.py PDF_File Destination_File

# Example:
# py .\extract_pdf_text.py ".\part1\RevPap\materials-13-03562-v2.pdf" ".\current_paper.txt"



#======================================
#======================================
#======================================
#====================================== Append Destination

import sys
from pathlib import Path

from pypdf import PdfReader


source = Path(sys.argv[1]).resolve()
destination = Path(sys.argv[2]).resolve()

reader = PdfReader(str(source))

parts = [
    "\n\n\n",
    "=" * 80,
    f"\nSOURCE PDF: {source.name}\n",
    f"FULL PATH: {source}\n",
    f"TOTAL PAGES: {len(reader.pages)}\n",
    "=" * 80,
    "\n",
]

for index, page in enumerate(reader.pages, start=1):
    parts.append(
        f"\n\n===== PAGE {index} OF {len(reader.pages)} =====\n\n"
    )
    parts.append(page.extract_text() or "")

parts.append("\n\n" + "=" * 80 + "\n")
parts.append(f"END OF PDF: {source.name}\n")
parts.append("=" * 80 + "\n\n")

extracted_text = "".join(parts)

with destination.open(
    "a",
    encoding="utf-8",
    errors="replace",
) as file:
    file.write(extracted_text)

print(
    f"appended_pdf={source.name} "
    f"pages={len(reader.pages)} "
    f"chars={len(extracted_text)} "
    f"output={destination}"
)


# Install dependency once:
# py -m pip install pypdf

# General command:
# py This_File.py PDF_File Destination_File

# Example:
# py .\append_pdf_text.py ".\part1\paper1.pdf" ".\combined_papers.txt"






#======================================
#======================================
#======================================
#====================================== Append Replace Destination

import sys
from pathlib import Path

from pypdf import PdfReader


if len(sys.argv) not in {3, 4}:
    raise SystemExit(
        "Usage: py pdf_to_text.py PDF_File Destination_File [replace|append]"
    )

source = Path(sys.argv[1]).resolve()
destination = Path(sys.argv[2]).resolve()

# Default operation is "replace" when the argument is omitted.
operation = sys.argv[3].lower() if len(sys.argv) == 4 else "replace"

if operation not in {"replace", "append"}:
    raise SystemExit(
        "The operation must be either 'replace' or 'append'."
    )

if not source.exists():
    raise SystemExit(f"PDF not found: {source}")

if not source.is_file():
    raise SystemExit(f"The source path is not a file: {source}")

if source.suffix.lower() != ".pdf":
    raise SystemExit(f"The source file is not a PDF: {source}")

destination.parent.mkdir(parents=True, exist_ok=True)

reader = PdfReader(str(source))

parts = [
    "\n\n",
    "=" * 80,
    f"\nSOURCE PDF: {source.name}\n",
    f"FULL PATH: {source}\n",
    f"TOTAL PAGES: {len(reader.pages)}\n",
    "=" * 80,
    "\n",
]

for index, page in enumerate(reader.pages, start=1):
    parts.append(
        f"\n\n===== PAGE {index} OF {len(reader.pages)} =====\n\n"
    )
    parts.append(page.extract_text() or "")

parts.extend([
    "\n\n",
    "=" * 80,
    f"\nEND OF PDF: {source.name}\n",
    "=" * 80,
    "\n\n",
])

extracted_text = "".join(parts)

file_mode = "w" if operation == "replace" else "a"

with destination.open(
    file_mode,
    encoding="utf-8",
    errors="replace",
) as file:
    file.write(extracted_text)

print(
    f"operation={operation} "
    f"pdf={source.name} "
    f"pages={len(reader.pages)} "
    f"chars={len(extracted_text)} "
    f"output={destination}"
)


# ============================================================
# Installation
# ============================================================

# Install pypdf once:
# py -m pip install pypdf


# ============================================================
# Usage
# ============================================================

# General command:
# py .\pdf_to_text.py PDF_File Destination_File [replace|append]


# Replace destination using the default operation:
# py .\pdf_to_text.py ".\part1\paper1.pdf" ".\papers.txt"


# Replace destination explicitly:
# py .\pdf_to_text.py ".\part1\paper1.pdf" ".\papers.txt" replace


# Append to destination:
# py .\pdf_to_text.py ".\part1\paper2.pdf" ".\papers.txt" append




#======================================
#======================================
#======================================
#====================================== Append Replace Destination, Read pdfs in folder and subfolders

import sys
from pathlib import Path

from pypdf import PdfReader


def extract_pdf_text(pdf_path: Path) -> tuple[str, int]:
    """Extract text from every page of one PDF."""

    reader = PdfReader(str(pdf_path))

    parts = [
        "\n\n",
        "=" * 80,
        f"\nSOURCE PDF: {pdf_path.name}\n",
        f"FULL PATH: {pdf_path}\n",
        f"TOTAL PAGES: {len(reader.pages)}\n",
        "=" * 80,
        "\n",
    ]

    for index, page in enumerate(reader.pages, start=1):
        parts.append(
            f"\n\n===== PAGE {index} OF {len(reader.pages)} =====\n\n"
        )
        parts.append(page.extract_text() or "")

    parts.extend([
        "\n\n",
        "=" * 80,
        f"\nEND OF PDF: {pdf_path.name}\n",
        "=" * 80,
        "\n\n",
    ])

    return "".join(parts), len(reader.pages)


# ============================================================
# Read command-line arguments
# ============================================================

if len(sys.argv) not in {3, 4, 5}:
    raise SystemExit(
        "Usage:\n"
        "  py pdf_folder_to_text.py Source_Folder Output [separate|combine] "
        "[replace|append]"
    )

source_folder = Path(sys.argv[1]).resolve()
destination = Path(sys.argv[2]).resolve()

# Default output mode: separate text files
output_mode = (
    sys.argv[3].lower()
    if len(sys.argv) >= 4
    else "separate"
)

# Default writing operation: replace
operation = (
    sys.argv[4].lower()
    if len(sys.argv) == 5
    else "replace"
)

if output_mode not in {"separate", "combine"}:
    raise SystemExit(
        "Output mode must be either 'separate' or 'combine'."
    )

if operation not in {"replace", "append"}:
    raise SystemExit(
        "Operation must be either 'replace' or 'append'."
    )

if not source_folder.exists():
    raise SystemExit(
        f"Source folder not found: {source_folder}"
    )

if not source_folder.is_dir():
    raise SystemExit(
        f"The source path is not a folder: {source_folder}"
    )


# ============================================================
# Find PDFs recursively
# ============================================================

pdf_files = sorted(
    (
        path
        for path in source_folder.rglob("*")
        if path.is_file() and path.suffix.lower() == ".pdf"
    ),
    key=lambda path: str(path).lower(),
)

if not pdf_files:
    raise SystemExit(
        f"No PDF files were found in: {source_folder}"
    )

print(f"PDF files found: {len(pdf_files)}")


# ============================================================
# Process PDFs
# ============================================================

successful = 0
failed = 0
total_pages = 0


if output_mode == "separate":

    # In separate mode, destination is an output folder.
    destination.mkdir(parents=True, exist_ok=True)

    for number, pdf_path in enumerate(pdf_files, start=1):
        relative_pdf_path = pdf_path.relative_to(source_folder)

        # Preserve the source subfolder structure.
        output_path = (
            destination / relative_pdf_path
        ).with_suffix(".txt")

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        try:
            extracted_text, page_count = extract_pdf_text(
                pdf_path
            )

            file_mode = (
                "w" if operation == "replace" else "a"
            )

            with output_path.open(
                file_mode,
                encoding="utf-8",
                errors="replace",
            ) as file:
                file.write(extracted_text)

            successful += 1
            total_pages += page_count

            print(
                f"[{number}/{len(pdf_files)}] "
                f"Completed: {pdf_path.name} "
                f"-> {output_path}"
            )

        except Exception as error:
            failed += 1

            print(
                f"[{number}/{len(pdf_files)}] "
                f"Failed: {pdf_path}\n"
                f"Reason: {type(error).__name__}: {error}"
            )


elif output_mode == "combine":

    # In combine mode, destination is one text file.
    destination.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    file_mode = "w" if operation == "replace" else "a"

    with destination.open(
        file_mode,
        encoding="utf-8",
        errors="replace",
    ) as combined_file:

        for number, pdf_path in enumerate(
            pdf_files,
            start=1,
        ):
            try:
                extracted_text, page_count = extract_pdf_text(
                    pdf_path
                )

                combined_file.write(extracted_text)

                successful += 1
                total_pages += page_count

                print(
                    f"[{number}/{len(pdf_files)}] "
                    f"Appended: {pdf_path.name}"
                )

            except Exception as error:
                failed += 1

                print(
                    f"[{number}/{len(pdf_files)}] "
                    f"Failed: {pdf_path}\n"
                    f"Reason: {type(error).__name__}: {error}"
                )


# ============================================================
# Completion summary
# ============================================================

print("\nProcessing complete.")
print(f"PDFs found: {len(pdf_files)}")
print(f"Successfully processed: {successful}")
print(f"Failed: {failed}")
print(f"Total pages extracted: {total_pages}")
print(f"Output mode: {output_mode}")
print(f"Operation: {operation}")
print(f"Destination: {destination}")


# ============================================================
# Installation
# ============================================================

# Install pypdf once:
# py -m pip install pypdf


# ============================================================
# Examples
# ============================================================

# Read all PDFs in the source folder and subfolders, then create one separate text file per PDF in the destination folder; replace existing text files.
# py .\pdf_folder_to_text.py ".\part1" ".\extracted_text"

# Same as above, but explicitly specify the separate output mode and replace write mode.
# py .\pdf_folder_to_text.py ".\part1" ".\extracted_text" separate replace

# Read all PDFs in the source folder and append each PDF's text to its corresponding text file in the destination folder.
# py .\pdf_folder_to_text.py ".\part1" ".\extracted_text" separate append

# Read all PDFs in the source folder and subfolders, then combine their text into one destination file; replace the existing file.
# py .\pdf_folder_to_text.py ".\part1" ".\all_papers.txt" combine

# Read all PDFs in the source folder and append all extracted text to the end of one existing destination file.
# py .\pdf_folder_to_text.py ".\part1" ".\all_papers.txt" combine append


















"""Extract PDF text into separate, combined, or batched text files."""

import sys
from pathlib import Path

from pypdf import PdfReader


def extract_pdf_text(pdf_path: Path) -> tuple[str, int]:
    """Extract text from every page of one PDF."""

    reader = PdfReader(str(pdf_path))

    parts = [
        "\n\n",
        "=" * 80,
        f"\nSOURCE PDF: {pdf_path.name}\n",
        f"FULL PATH: {pdf_path}\n",
        f"TOTAL PAGES: {len(reader.pages)}\n",
        "=" * 80,
        "\n",
    ]

    for index, page in enumerate(reader.pages, start=1):
        parts.append(
            f"\n\n===== PAGE {index} OF {len(reader.pages)} =====\n\n"
        )
        parts.append(page.extract_text() or "")

    parts.extend([
        "\n\n",
        "=" * 80,
        f"\nEND OF PDF: {pdf_path.name}\n",
        "=" * 80,
        "\n\n",
    ])

    return "".join(parts), len(reader.pages)


def get_batch_destination(
    destination_file: Path,
    batch_number: int,
    total_batches: int,
) -> Path:
    """Return a numbered destination filename for one PDF batch."""

    number_width = max(3, len(str(total_batches)))
    part_number = str(batch_number).zfill(number_width)

    return destination_file.with_name(
        f"{destination_file.stem}_part_{part_number}"
        f"{destination_file.suffix}"
    )


# ============================================================
# Read command-line arguments
# ============================================================

if len(sys.argv) not in {3, 4, 5, 6}:
    raise SystemExit(
        "Usage:\n"
        "  py pdf_folder_to_text.py Source_Folder Output "
        "[separate|combine] [replace|append] [PDFs_Per_File]\n"
        "\n"
        "Example: create one combined text file for every 5 PDFs:\n"
        "  py pdf_folder_to_text.py Source_Folder Output_File "
        "combine replace 5"
    )

source_folder = Path(sys.argv[1]).resolve()
destination = Path(sys.argv[2]).resolve()

# Default output mode: separate text files
output_mode = (
    sys.argv[3].lower()
    if len(sys.argv) >= 4
    else "separate"
)

# Default writing operation: replace
operation = (
    sys.argv[4].lower()
    if len(sys.argv) >= 5
    else "replace"
)

# Optional number of PDFs in each combined output file.
# If omitted, combine mode writes all PDFs to one file.
pdfs_per_file = None

if len(sys.argv) == 6:
    if output_mode != "combine":
        raise SystemExit(
            "PDFs_Per_File can be used only with output mode 'combine'."
        )

    try:
        pdfs_per_file = int(sys.argv[5])
    except ValueError:
        raise SystemExit(
            "PDFs_Per_File must be a positive integer, such as 5."
        )

    if pdfs_per_file <= 0:
        raise SystemExit(
            "PDFs_Per_File must be greater than zero."
        )

if output_mode not in {"separate", "combine"}:
    raise SystemExit(
        "Output mode must be either 'separate' or 'combine'."
    )

if operation not in {"replace", "append"}:
    raise SystemExit(
        "Operation must be either 'replace' or 'append'."
    )

if not source_folder.exists():
    raise SystemExit(
        f"Source folder not found: {source_folder}"
    )

if not source_folder.is_dir():
    raise SystemExit(
        f"The source path is not a folder: {source_folder}"
    )


# ============================================================
# Find PDFs recursively
# ============================================================

pdf_files = sorted(
    (
        path
        for path in source_folder.rglob("*")
        if path.is_file() and path.suffix.lower() == ".pdf"
    ),
    key=lambda path: str(path).lower(),
)

if not pdf_files:
    raise SystemExit(
        f"No PDF files were found in: {source_folder}"
    )

print(f"PDF files found: {len(pdf_files)}")


# ============================================================
# Process PDFs
# ============================================================

successful = 0
failed = 0
total_pages = 0
combined_files_created = 0


if output_mode == "separate":

    # In separate mode, destination is an output folder.
    destination.mkdir(parents=True, exist_ok=True)

    for number, pdf_path in enumerate(pdf_files, start=1):
        relative_pdf_path = pdf_path.relative_to(source_folder)

        # Preserve the source subfolder structure.
        output_path = (
            destination / relative_pdf_path
        ).with_suffix(".txt")

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        try:
            extracted_text, page_count = extract_pdf_text(
                pdf_path
            )

            file_mode = (
                "w" if operation == "replace" else "a"
            )

            with output_path.open(
                file_mode,
                encoding="utf-8",
                errors="replace",
            ) as file:
                file.write(extracted_text)

            successful += 1
            total_pages += page_count

            print(
                f"[{number}/{len(pdf_files)}] "
                f"Completed: {pdf_path.name} "
                f"-> {output_path}"
            )

        except Exception as error:
            failed += 1

            print(
                f"[{number}/{len(pdf_files)}] "
                f"Failed: {pdf_path}\n"
                f"Reason: {type(error).__name__}: {error}"
            )


elif output_mode == "combine":

    destination.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    # If no batch size is supplied, one batch contains every PDF.
    batch_size = pdfs_per_file or len(pdf_files)
    pdf_batches = [
        pdf_files[start:start + batch_size]
        for start in range(0, len(pdf_files), batch_size)
    ]
    total_batches = len(pdf_batches)

    for batch_number, pdf_batch in enumerate(
        pdf_batches,
        start=1,
    ):
        # Preserve the original destination filename when no batch size
        # is supplied. Otherwise, create numbered output files.
        if pdfs_per_file is None:
            output_path = destination
        else:
            output_path = get_batch_destination(
                destination,
                batch_number,
                total_batches,
            )

        file_mode = "w" if operation == "replace" else "a"
        first_pdf_number = (batch_number - 1) * batch_size + 1
        last_pdf_number = first_pdf_number + len(pdf_batch) - 1

        print(
            f"\nWriting batch {batch_number}/{total_batches}: "
            f"PDFs {first_pdf_number}-{last_pdf_number}\n"
            f"Output file: {output_path}"
        )

        with output_path.open(
            file_mode,
            encoding="utf-8",
            errors="replace",
        ) as combined_file:

            for pdf_offset, pdf_path in enumerate(pdf_batch):
                number = first_pdf_number + pdf_offset

                try:
                    extracted_text, page_count = extract_pdf_text(
                        pdf_path
                    )

                    combined_file.write(extracted_text)
                    combined_file.flush()

                    successful += 1
                    total_pages += page_count

                    print(
                        f"[{number}/{len(pdf_files)}] "
                        f"Added: {pdf_path.name} -> {output_path.name}"
                    )

                except Exception as error:
                    failed += 1

                    print(
                        f"[{number}/{len(pdf_files)}] "
                        f"Failed: {pdf_path}\n"
                        f"Reason: {type(error).__name__}: {error}"
                    )

        combined_files_created += 1


# ============================================================
# Completion summary
# ============================================================

print("\nProcessing complete.")
print(f"PDFs found: {len(pdf_files)}")
print(f"Successfully processed: {successful}")
print(f"Failed: {failed}")
print(f"Total pages extracted: {total_pages}")
print(f"Output mode: {output_mode}")
print(f"Operation: {operation}")

if output_mode == "combine":
    if pdfs_per_file is None:
        print("PDFs per combined file: all")
    else:
        print(f"PDFs per combined file: {pdfs_per_file}")
        print(f"Combined files created: {combined_files_created}")

print(f"Destination: {destination}")


# ============================================================
# Installation
# ============================================================

# Install pypdf once:
# py -m pip install pypdf


# ============================================================
# Examples
# ============================================================

# Read all PDFs in the source folder and subfolders, then create one
# separate text file per PDF; replace existing text files.
# py .\pdf_folder_to_text.py ".\part1" ".\extracted_text"

# Same as above, explicitly specifying separate and replace modes.
# py .\pdf_folder_to_text.py ".\part1" ".\extracted_text" separate replace

# Append each PDF's text to its corresponding separate text file.
# py .\pdf_folder_to_text.py ".\part1" ".\extracted_text" separate append

# Combine every PDF into one destination file; replace the existing file.
# py .\pdf_folder_to_text.py ".\part1" ".\all_papers.txt" combine replace

# Append every PDF to one existing destination file.
# py .\pdf_folder_to_text.py ".\part1" ".\all_papers.txt" combine append

# Create one numbered combined text file for every 5 PDFs.
# Creates all_papers_part_001.txt, all_papers_part_002.txt, and so on.
# py .\pdf_folder_to_text.py ".\part1" ".\all_papers.txt" combine replace 5

# Append each group of 5 PDFs to its corresponding numbered file.
# Warning: rerunning this command appends duplicate extracted content.
# py .\pdf_folder_to_text.py ".\part1" ".\all_papers.txt" combine append 5
