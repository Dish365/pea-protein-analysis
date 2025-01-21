import pytest
import sys

def main():
    """Run the test suite"""
    args = [
        "-v",
        "--log-cli-level=INFO",
        "tests/api/process_analysis/",
    ]
    
    # Add any command line arguments
    args.extend(sys.argv[1:])
    
    # Run pytest
    exit_code = pytest.main(args)
    sys.exit(exit_code)

if __name__ == "__main__":
    main() 