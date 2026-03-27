import urllib.request
import json
import math
import os
import argparse
import sys


def fibonacci_to_spiral_points(sequence_strings):
    """Convert a Fibonacci integer sequence to 3D Archimedes spiral coordinates.

    Each Fibonacci number F(i) maps to a point on a golden-angle spiral:
        angle = i * golden_angle
        radius = sqrt(F(i) + 1)   (sqrt keeps scale sane for large values)
        x = radius * cos(angle)
        y = radius * sin(angle)
        z = i * 0.1               (slight vertical rise for 3D depth)

    This produces the iconic sunflower/phyllotaxis pattern that Fibonacci is
    famous for, making the data-driven geometry visually meaningful.
    """
    golden_angle = math.pi * (3.0 - math.sqrt(5.0))  # ~2.399963 radians
    points = []
    for i, val_str in enumerate(sequence_strings):
        val = int(val_str)
        radius = math.sqrt(val + 1)
        angle = i * golden_angle
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        z = i * 0.1
        points.append({"x": x, "y": y, "z": z})
    return points


def main():
    parser = argparse.ArgumentParser(description="Export JSON data from engine")
    parser.add_argument("--type", choices=["primes", "fractal", "fibonacci"], default="primes", help="Type of sequence to export")
    args = parser.parse_args()

    os.makedirs('data', exist_ok=True)

    if args.type == "primes":
        url = "http://127.0.0.1:8000/api/v1/sequences/primes?n=100"
        filename = "data/primes.json"
    elif args.type == "fractal":
        url = "http://127.0.0.1:8000/api/v1/sequences/fractal?iterations=3"
        filename = "data/fractal.json"
    elif args.type == "fibonacci":
        url = "http://127.0.0.1:8000/api/v1/sequences/fibonacci?n=100"
        filename = "data/fibonacci.json"
    else:
        print(f"Unknown type: {args.type}")
        sys.exit(1)

    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            data = response.read()
            json_data = json.loads(data.decode('utf-8'))

        if args.type == "fibonacci":
            # The fibonacci endpoint returns a flat sequence of integers (strings).
            # Convert them to 3D spiral points so render.py can visualize them.
            sequence_strings = json_data.get("data", {}).get("sequence", [])
            spiral_points = fibonacci_to_spiral_points(sequence_strings)
            json_data["data"]["points"] = spiral_points

        with open(filename, 'w') as f:
            json.dump(json_data, f, indent=4)

        print(f"Successfully exported data to {filename}")

    except Exception as e:
        print(f"Error fetching data: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
