#!/usr/bin/env python3
"""Mathematica Art — End-to-end 4K render pipeline.

Usage:
    python scripts/run_pipeline.py --input data/primes.json [--frames 300] [--fps 60]
"""
import argparse
import os
import shutil
import subprocess
import sys

FRAMES_DIR = "renders/frames"
OUTPUT_DIR = "renders/output"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "mathematica_art.mp4")


def check_dependencies():
    """Verify blender and ffmpeg are available on PATH."""
    for tool in ["blender", "ffmpeg", "ffprobe"]:
        if not shutil.which(tool):
            print(f"Error: '{tool}' not found on PATH. Install it first.", file=sys.stderr)
            sys.exit(1)


def render_frames(input_file, frame_count):
    """Run Blender headless to produce image sequence."""
    os.makedirs(FRAMES_DIR, exist_ok=True)
    cmd = [
        "blender", "--background", "--python", "renderer/render.py",
        "--", "--input", input_file,
        "--frames", str(frame_count),
        "--output-dir", FRAMES_DIR,
    ]
    print(f"▶ Rendering {frame_count} frames with Blender...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Blender failed:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)
    # Verify frames exist
    frames = sorted(f for f in os.listdir(FRAMES_DIR) if f.endswith(".png"))
    if len(frames) < frame_count:
        print(f"Warning: expected {frame_count} frames, found {len(frames)}", file=sys.stderr)
    print(f"  ✓ {len(frames)} frames rendered to {FRAMES_DIR}/")


def encode_video(fps):
    """Stitch frames into 4K H.264 MP4 with FFmpeg."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(fps),
        "-i", os.path.join(FRAMES_DIR, "frame_%04d.png"),
        "-c:v", "libx264",
        "-preset", "slow",
        "-crf", "17",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        OUTPUT_FILE,
    ]
    print(f"▶ Encoding {fps}fps H.264 MP4...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"FFmpeg failed:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)
    print(f"  ✓ Video written to {OUTPUT_FILE}")


def validate_output(expected_width=3840, expected_height=2160):
    """Verify MP4 metadata with ffprobe."""
    if not os.path.exists(OUTPUT_FILE):
        print(f"Error: output file {OUTPUT_FILE} does not exist", file=sys.stderr)
        sys.exit(1)
    cmd = [
        "ffprobe", "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height",
        "-of", "csv=p=0",
        OUTPUT_FILE,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    dims = result.stdout.strip()
    if f"{expected_width},{expected_height}" not in dims:
        print(f"Warning: unexpected resolution: {dims}", file=sys.stderr)
    else:
        print(f"  ✓ Resolution verified: {dims}")
    size_mb = os.path.getsize(OUTPUT_FILE) / (1024 * 1024)
    print(f"  ✓ File size: {size_mb:.1f} MB")


def main():
    parser = argparse.ArgumentParser(description="Mathematica Art 4K render pipeline")
    parser.add_argument("--input", required=True, help="Path to JSON data file")
    parser.add_argument("--frames", type=int, default=300, help="Number of frames to render (default: 300)")
    parser.add_argument("--fps", type=int, default=60, help="Output video framerate (default: 60)")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: input file {args.input} does not exist", file=sys.stderr)
        sys.exit(1)

    check_dependencies()
    render_frames(args.input, args.frames)
    encode_video(args.fps)
    validate_output()

    print(f"\n✓ Pipeline complete: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
