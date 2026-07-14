# CamCog: CamCAN Cognitive Score Extractor

![Python](https://img.shields.io/badge/python-3.6+-blue.svg) ![License](https://img.shields.io/badge/license-MIT-green.svg)

A lightweight Python tool to extract and merge behavioral and cognitive metrics from BIDS-compliant CamCAN `*_summary.txt` files into a single CSV. Output is keyed by Subject ID (CCID) for easy integration with neuroimaging data. 

*Zero external dependencies required (no `pandas` or `numpy`). Handles missing data (`NaN`) and namespace collisions automatically.*

---

## 📁 Data Structure

The script expects the default CamCAN release structure:
```text
<BASE_DIR>/<TaskName>/release001/summary/<TaskName>_summary.txt

```

---

## 🚀 Quick Start

The easiest way to use CamCog is via the included bash wrapper script.

**1. Edit `CamCog.sh**`

Open the file in a text editor. Update `--base` to your dataset folder, and add the tests/columns you want:

```bash
#!/bin/bash
python CamCog.py \
    --base "/path/to/camcan/cc700-scored" \
    --test "BentonFaces" --cols TotalScore \
    --test "Hotel" --cols Time \
    --test "MRI" --cols PctCorrect,mRT,stdRT \
    --output "my_study_data.csv"

```

*(Rule: Every `--test` must be immediately followed by exactly one `--cols` argument, but you can easily extract multiple cols with comma-separated values.)*

**2. Make Executable (Mac/Linux)**

Open your terminal and run:

```bash
chmod +x CamCog.sh

```

**3. Run the Extraction**

```bash
./CamCog.sh

```

---

## ⚙️ CLI Arguments

If running `CamCog.py` manually, here are the available arguments:

| Parameter | Required | Description |
| --- | --- | --- |
| `--base` | **Yes** | Root directory of the dataset (e.g., `./cc700-scored`). |
| `--test` | **Yes** | Task folder name (e.g., `Hotel`). Repeatable for batching. |
| `--cols` | **Yes** | Comma-separated target metrics (e.g., `Time,mRT`). Maps 1:1 to `--test`. |
| `--output` | No | Destination path for the merged CSV. Defaults to `merged.csv`. |
| `--sub` | No | Path to a `.txt` whitelist of Subject IDs to keep (one per line). |

---

## 📝 Citation

If you use this tool in your research, please cite:

**APA Format:**

> Mahmoudi, A. (2026). CamCog: CamCAN Cognitive Score Extractor (Version 1.0.0) [Computer software]. https://github.com/pythyn/camcan-cognitive-extractor

**BibTeX:**

```bibtex
@software{CamCog2026,
  author = {Mahmoudi, AmirHossein},
  title = {CamCog: CamCAN Cognitive Score Extractor},
  year = {2026},
  version = {1.0.0},
  url = {https://github.com/pythyn/camcan-cognitive-extractor}
}

```