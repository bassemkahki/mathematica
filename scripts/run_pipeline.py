#!/usr/bin/env python3
"""Mathematica Art — End-to-end 4K render pipeline.

Renders each artwork (fibonacci, primes, fractal) separately, producing:
  - renders/output/{slug}.mp4        — turntable video
  - renders/output/{slug}-poster.png — single poster frame

Usage:
    python scripts/run_pipeline.py --all                        # render all artworks
    python scripts/run_pipeline.py --slug fibonacci             # render one artwork
    python scripts/run_pipeline.py --slug primes --poster-only  # poster only (fast)
"""
import argparse
import os
import shutil
import subprocess
import sys
import glob

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RENDERS_DIR = os.path.join(BASE_DIR, "renders")
OUTPUT_DIR = os.path.join(RENDERS_DIR, "output")

ALL_SLUGS = ["fibonacci", "primes", "fractal"]


def check_dependencies():
    """Verify blender and ffmpeg are available on PATH."""
    for tool in ["blender", "ffmpeg", "ffprobe"]:
        if not shutil.which(tool):
            print(f"Error: '{tool}' not found on PATH. Install it first.", file=sys.stderr)
            sys.exit(1)


def frames_dir_for(slug):
    return os.path.join(RENDERS_DIR, "frames", slug)


def render_frames(slug, input_file, frame_count, poster_only=False):
    """Run Blender headless to produce image sequence for one artwork."""
    fdir = frames_dir_for(slug)
    os.makedirs(fdir, exist_ok=True)

    cmd = [
        "blender", "--background", "--python", os.path.join(BASE_DIR, "renderer", "render.py"),
        "--", "--input", input_file,
        "--frames", str(frame_count),
        "--output-dir", fdir,
        "--slug", slug,
    ]
    if poster_only:
        cmd.append("--poster-only")

    mode = "poster" if poster_only else f"{frame_count} frames"
    print(f"\n{'='*60}")
    print(f"  Rendering {slug} ({mode})")
    print(f"{'='*60}")

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Blender stderr:\n{result.stderr}", file=sys.stderr)
        print(f"Blender stdout:\n{result.stdout}")
        sys.exit(1)

    # Verify output
    frames = sorted(f for f in os.listdir(fdir) if f.endswith(".png"))
    print(f"  Rendered {len(frames)} frame(s) to {fdir}/")
    return frames


def extract_poster(slug):
    """Copy first rendered frame as the poster image."""
    fdir = frames_dir_for(slug)
    # Find first frame
    frames = sorted(glob.glob(os.path.join(fdir, "frame_*.png")))
    if not frames:
        print(f"Warning: no frames found for {slug} poster", file=sys.stderr)
        return

    poster_path = os.path.join(OUTPUT_DIR, f"{slug}-poster.png")
    shutil.copy2(frames[0], poster_path)
    print(f"  Poster: {poster_path}")


def encode_video(slug, fps):
    """Stitch frames into 4K H.264 MP4 with FFmpeg."""
    fdir = frames_dir_for(slug)
    output_file = os.path.join(OUTPUT_DIR, f"{slug}.mp4")

    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(fps),
        "-i", os.path.join(fdir, "frame_%04d.png"),
        "-c:v", "libx264",
        "-preset", "slow",
        "-crf", "17",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        output_file,
    ]
    print(f"  Encoding {slug} at {fps}fps...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"FFmpeg failed for {slug}:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)
    print(f"  Video: {output_file}")
    return output_file


def validate_output(slug, expected_width=3840, expected_height=2160):
    """Verify MP4 metadata with ffprobe."""
    output_file = os.path.join(OUTPUT_DIR, f"{slug}.mp4")
    if not os.path.exists(output_file):
        print(f"Warning: {output_file} does not exist", file=sys.stderr)
        return

    cmd = [
        "ffprobe", "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height",
        "-of", "csv=p=0",
        output_file,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    dims = result.stdout.strip()
    if f"{expected_width},{expected_height}" not in dims:
        print(f"  Warning: unexpected resolution for {slug}: {dims}", file=sys.stderr)
    else:
        print(f"  Resolution verified: {dims}")

    size_mb = os.path.getsize(output_file) / (1024 * 1024)
    print(f"  File size: {size_mb:.1f} MB")


def process_artwork(slug, frame_count, fps, poster_only=False):
    """Full pipeline for one artwork: render -> encode -> validate."""
    input_file = os.path.join(BASE_DIR, "data", f"{slug}.json")
    if not os.path.exists(input_file):
        print(f"Error: data file {input_file} not found. Run export_data.py first.", file=sys.stderr)
        sys.exit(1)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Render
    render_frames(slug, input_file, frame_count, poster_only=poster_only)

    # Extract poster (always — from first frame)
    extract_poster(slug)

    if not poster_only:
        # Encode video
        encode_video(slug, fps)
        # Validate
        validate_output(slug)

    print(f"  Pipeline complete for {slug}")


def main():
    parser = argparse.ArgumentParser(description="Mathematica Art 4K render pipeline")
    parser.add_argument("--slug", choices=ALL_SLUGS, help="Render a single artwork")
    parser.add_argument("--all", action="store_true", help="Render all artworks")
    parser.add_argument("--frames", type=int, default=300, help="Frames per video (default: 300)")
    parser.add_argument("--fps", type=int, default=60, help="Video framerate (default: 60)")
    parser.add_argument("--poster-only", action="store_true", help="Render only poster frame (much faster)")
    args = parser.parse_args()

    if not args.slug and not args.all:
        print("Error: specify --slug <name> or --all", file=sys.stderr)
        parser.print_help()
        sys.exit(1)

    check_dependencies()

    slugs = ALL_SLUGS if args.all else [args.slug]

    for slug in slugs:
        process_artwork(slug, args.frames, args.fps, poster_only=args.poster_only)

    print(f"\nAll done. Output in {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
