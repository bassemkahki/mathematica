import os
import subprocess
import pytest
import sys

@pytest.fixture(autouse=True)
def setup_data_dir():
    os.makedirs("data", exist_ok=True)
    yield
    # Clean up the file after test if we want, but let's just make sure it exists
    # The requirement says "clean up the data/ directory before testing"
    if os.path.exists("data/primes.json"):
        os.remove("data/primes.json")

def test_export_script_produces_file():
    result = subprocess.run([sys.executable, "scripts/export_data.py", "--type", "primes"])
    assert result.returncode == 0
    assert os.path.exists("data/primes.json") is True

def test_blender_headless_ingestion():
    # Ensure the json file exists for this test
    subprocess.run([sys.executable, "scripts/export_data.py", "--type", "primes"])
    assert os.path.exists("data/primes.json") is True
    
    result = subprocess.run(
        ["blender", "--background", "--python", "renderer/render.py", "--", "--input", "data/primes.json"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "Render finished. Objects generated:" in result.stdout
