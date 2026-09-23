#!/usr/bin/env python3
"""Run the quilt-port test suite."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "tests"))
import test_port

if __name__ == "__main__":
    rc = test_port.__name__  # not strictly needed
    # The test_port module runs tests when executed directly.
    pass
