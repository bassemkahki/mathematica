import urllib.request
import json
import math
import os
import argparse
import sys


def fibonacci_to_spiral_points(sequence_strings):
    """Convert a Fibonacci integer sequence to 3D golden-angle spiral coordinates.

    Uses index-based radius (not Fibonacci value) to keep the spiral compact
    and visually appealing. The golden angle ensures optimal packing, producing
    the iconic sunflower/phyllotaxis pattern.

    Radius grows as sqrt(index), keeping point density roughly uniform.
    A gentle vertical rise adds 3D depth.
    """
    golden_angle = math.pi * (3.0 - math.sqrt(5.0))  # ~2.399963 radians
    points = []
    n = len(sequence_strings)
    # Scale factor so the outermost point is at radius ~15
    scale = 15.0 / math.sqrt(max(n, 1))
    for i, val_str in enumerate(sequence_strings):
        radius = math.sqrt(i + 1) * scale
        angle = i * golden_angle
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        z = i * 0.08  # gentle vertical rise for 3D depth
        points.append({"x": x, "y": y, "z": z})
    return points


def main():
    parser = argparse.ArgumentParser(description="Export JSON data from engine")
    parser.add_argument("--type", choices=["primes", "fractal", "fibonacci", "all"],
                        default="all", help="Type of sequence to export (default: all)")
    args = parser.parse_args()

    os.makedirs('data', exist_ok=True)

    types_to_export = ["primes", "fractal", "fibonacci"] if args.type == "all" else [args.type]

    for seq_type in types_to_export:
        if seq_type == "primes":
            url = "http://127.0.0.1:8000/api/v1/sequences/primes?n=200"
            filename = "data/primes.json"
        elif seq_type == "fractal":
            url = "http://127.0.0.1:8000/api/v1/sequences/fractal?iterations=4"
            filename = "data/fractal.json"
        elif seq_type == "fibonacci":
            url = "http://127.0.0.1:8000/api/v1/sequences/fibonacci?n=200"
            filename = "data/fibonacci.json"
        else:
            print(f"Unknown type: {seq_type}")
            continue

        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req) as response:
                data = response.read()
                json_data = json.loads(data.decode('utf-8'))

            if seq_type == "fibonacci":
                # The fibonacci endpoint returns a flat sequence of integers (strings).
                # Convert them to 3D spiral points so render.py can visualize them.
                sequence_strings = json_data.get("data", {}).get("sequence", [])
                spiral_points = fibonacci_to_spiral_points(sequence_strings)
                json_data["data"]["points"] = spiral_points

            with open(filename, 'w') as f:
                json.dump(json_data, f, indent=4)

            point_count = len(json_data.get("data", {}).get("points", []))
            seq_count = len(json_data.get("data", {}).get("sequence", []))
            print(f"Exported {seq_type} -> {filename} ({point_count} points, {seq_count} sequence items)")

        except Exception as e:
            print(f"Error fetching {seq_type}: {e}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
