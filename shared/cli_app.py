from __future__ import annotations

import argparse
import time
from collections.abc import Callable


def build_parser(description: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--mode", choices=["manual", "auto"], default="auto")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--step-delay", type=float, default=0.0)
    return parser


def auto_pause(delay: float) -> None:
    if delay > 0:
        time.sleep(delay)
