# Phase 5: Discussion Log

**Date:** 2026-03-26
**Phase:** 5 (4K Export Automation)

## Area 1: Image Sequence Format
**Question:** How should raw frames be saved?
**Options Presented:**
A. PNG (16-bit) — Lossless, standard, easy to inspect manually
B. OpenEXR — Highest bit-depth, raw linear data
C. TIFF — Uncompressed high quality
**User Selection:** A AND C (PNG 16-bit and TIFF)

## Area 2: Automation Strategy
**Question:** How should we orchestrate Blender render followed by FFmpeg?
**Options Presented:**
A. Python Wrapper Script (e.g. `run_pipeline.py`)
B. Bash/Shell Script
C. Blender Output Handler
**User Selection:** A (Python Wrapper Script)

## Area 3: Output Video Specs
**Question:** What framerate and codec for the 4K MP4?
**Options Presented:**
A. 24fps H.264
B. 60fps H.264
C. 30fps H.265 (HEVC)
**User Selection:** B (60fps H.264)

## Area 4: Directory Structure
**Question:** Where should render artifacts be stored?
**Options Presented:**
A. Separate `renders/` root directory with subfolders for `frames/` and `output/`.
B. Inside the `renderer/` module alongside the script.
C. Dedicated timestamped folders for every run.
**User Selection:** A (Separate `renders/` root directory)
