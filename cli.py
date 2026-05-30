#!/usr/bin/env python3
"""Run ELIZA in the terminal.

Usage:
    python cli.py          # German DOCTOR script (default)
    python cli.py en       # original English DOCTOR script
"""

import sys

from eliza import load_doctor


def main():
    language = sys.argv[1] if len(sys.argv) > 1 else 'de'
    load_doctor(language).run()


if __name__ == '__main__':
    main()
