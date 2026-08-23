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