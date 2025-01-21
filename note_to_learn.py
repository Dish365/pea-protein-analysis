# uvicorn main:app --reload --port 8001 --log-level debug

# pytest tests/api/process_analysis/test_integration.py -v --log-cli-level=DEBUG


# # Close any running Python processes
# taskkill /F /IM python.exe

# Or on Linux/Mac
# pkill python

# Then try cleaning and rebuilding again
# cargo clean
# cargo build --release