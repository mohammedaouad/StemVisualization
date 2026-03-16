# StemVis — Femoral Stem Surgical Planning Tool

A Python-based 3D surgical planning tool for total hip arthroplasty (THA), developed as part of a Master's project in Medical Engineering at **FH Aachen University of Applied Sciences**.

The tool processes femur bone meshes and computes key anatomical landmarks used in femoral stem implant planning, with an interactive dual-viewport visualization interface.

---

## Methodology

### Femoral Head Center (HJC)
The femoral head is geometrically a sphere. To find the Hip Joint Center, a sphere is fitted to the dome region of the femoral head using least-squares optimization. The center of that fitted sphere is, by definition, the HJC — the point around which the femoral head rotates within the acetabulum.

The fitting is done only on the dome (upper portion of the head) to avoid the cut neck boundary that appears in STL exports from 3D Slicer.

### Shaft Axis
The shaft axis is defined using two cross-sectional slices taken at different heights along the proximal femoral shaft. The center of each slice is computed using the median of the cross-section points (more robust than the mean for irregular shapes). The line connecting these two centers defines the anatomical shaft axis.

### Stem Tip Placement
The Stem Tip is the point along the shaft axis where the CCD angle (Caput-Collum-Diaphysis angle) is satisfied. The CCD angle is the angle between the neck axis (Stem Tip → HJC) and the stem axis (Stem Tip → Stem Toe). The tool scans along the shaft axis to find the exact point where this angle matches the target value set by the user (between 115° and 135°).

### Neck Resection
The resection plane is placed along the neck axis at a user-defined fraction of the neck length (between 20% and 80%), measured from the Stem Tip toward the HJC. This matches the standard surgical workflow for femoral neck osteotomy.

---

## Features

- Automatic PCA-based alignment of the femur long axis
- Femoral Head Center detection via sphere fitting
- Shaft axis computation using median cross-sectional slice centers
- Stem Tip placement driven by CCD angle (115–135°)
- Interactive neck resection with adjustable resection level (20–80% of neck)
- Dual-viewport visualization: full femur (pre-op) vs resected femur (post-resection)
- Professional Qt-based GUI with live sliders and direct value input

---

## Project Structure

```
StemVis/
├── main.py             # Entry point — Qt window and event handling
├── ui.py               # UI colors and stylesheet
├── visualisation.py    # 3D rendering — PyVista + PyVistaqt
├── HJC.py              # Femoral head center detection
├── StemAxis.py         # Shaft axis computation
├── StemTip.py          # Stem tip placement via CCD angle
├── ResectedFemur.py    # Neck resection plane and mesh clipping
├── Data/               # STL mesh files (not tracked)
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Data

The femur mesh used for development and testing was obtained from open-source CT data and segmented manually using **3D Slicer** (exported in RAS orientation as STL).

The STL file is not included in this repository. To use the tool with your own data:
1. Obtain a CT scan from an open source such as [The Cancer Imaging Archive](https://www.cancerimagingarchive.net/) or [Zenodo](https://zenodo.org)
2. Segment the femur in [3D Slicer](https://www.slicer.org/)
3. Export as STL and place the file at `Data/Femur_Bone.stl`

---

## Installation

```bash
git clone https://github.com/YOUR_USERNAME/StemVis.git
cd StemVis

python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
```

---

## Usage

```bash
python main.py
```

The application opens two interactive 3D viewports:

- **Left — Pre-Op:** full femur with stem and neck axis overlay
- **Right — Post-Resection:** resected femur showing the osteotomy result

Use the sidebar sliders or type a value directly to adjust:
- **CCD Angle** (115°–135°) — controls stem tip position along the shaft
- **Resection Level** (20%–80% of neck length) — controls where the neck is cut

---

## Dependencies

```
numpy
scipy
pyvista
pyvistaqt
PyQt6
```

Install with:
```bash
pip install -r requirements.txt
```

---

## Academic Context

Developed as part of a Master's thesis in **Medical Engineering** at **FH Aachen University of Applied Sciences**, focusing on computer-assisted planning for total hip arthroplasty.

The anatomical definitions and planning workflow reference the `automaticFemoralCS` toolbox (RWTH Aachen, MATLAB) by Modenese et al.

---

© FH Aachen — Medical Engineering · 2025–2026
