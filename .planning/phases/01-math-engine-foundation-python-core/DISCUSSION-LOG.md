# Phase 1 Discussion Log

**Date:** 2026-03-26

## Gray Area: General Execution and Output
**Question:** Which areas do you want to discuss for Phase 1?
1. Execution Interface — How will the engine be run and triggered? (e.g. CLI vs importable module)
2. Dependencies Strategy — Use standard library or allow 3rd-party C-extensions like gmpy2?
3. JSON Output Structure — Flat arrays, rich documents, or batched frames?
4. All of the above

**User Response:**
1. webpage for project
2. Standard library
3. Rich documents

## Area: Execution Interface (Clarification)
**Question:**
Building the actual web gallery is scheduled for Phase 6 (WEB-01 to WEB-04). For this current Phase 1, we just need the invisible math engine to calculate the numbers and generate the JSON files that the webpage will eventually load.
How should this "invisible" math engine be triggered to generate those files?
1. Command-Line Interface (e.g. `python -m math_engine generate fibonacci`)
2. Importable Python module (so a future backend API can import and call it)
3. Standalone API server (the engine hosts its own local server)

**User Response:**
3 (Standalone API server)
