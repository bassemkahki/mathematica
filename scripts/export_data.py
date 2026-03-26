import urllib.request
import json
import os
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description="Export JSON data from engine")
    parser.add_argument("--type", choices=["primes", "fractal"], default="primes", help="Type of sequence to export")
    args = parser.parse_args()

    os.makedirs('data', exist_ok=True)

    if args.type == "primes":
        url = "http://127.0.0.1:8000/api/v1/sequences/primes?n=100"
        filename = "data/primes.json"
    elif args.type == "fractal":
        url = "http://127.0.0.1:8000/api/v1/sequences/fractal?iterations=3"
        filename = "data/fractal.json"
    else:
        print(f"Unknown type: {args.type}")
        sys.exit(1)

    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            data = response.read()
            json_data = json.loads(data.decode('utf-8'))
            
            with open(filename, 'w') as f:
                json.dump(json_data, f, indent=4)
                
        print(f"Successfully exported data to {filename}")
        
    except Exception as e:
        print(f"Error fetching data: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
