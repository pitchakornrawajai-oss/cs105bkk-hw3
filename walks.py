"""HW3 · walks.py: read the step counter's CSV file and keep only the good rows. Practises
Session 7 (reading a CSV file, cleaning data) and Session 9 (a generator and a decorator)."""

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable, Iterator, TypeVar

T = TypeVar("T")


@dataclass
class Walk:
    date: str
    steps: int
    place: str


def parse_walk(row: dict[str, str]) -> Walk:
    date = (row.get("date") or "").strip()
    if not date:
        raise ValueError("date is missing or empty")

    raw_steps = row.get("steps")
    if raw_steps is None:
        raise ValueError("steps is missing")

    raw_steps_str = str(raw_steps).strip()
    if not raw_steps_str:
        raise ValueError("steps is empty")

    steps = int(raw_steps_str)
    if steps < 0:
        raise ValueError(f"steps is below 0: {steps}")

    place = (row.get("place") or "").strip()
    return Walk(date=date, steps=steps, place=place)


def none_on_error(func: Callable[..., T]) -> Callable[..., T | None]:
    def wrapper(*args, **kwargs) -> T | None:
        try:
            return func(*args, **kwargs)
        except ValueError:
            return None

    return wrapper


def read_rows(path: Path | str) -> Iterator[dict[str, str]]:
    with open(path, encoding="utf-8", newline="") as file:
        yield from csv.DictReader(file)


def good_walks(rows: Iterable[dict[str, str]]) -> Iterator[Walk]:
    safe_parse = none_on_error(parse_walk)
    for row in rows:
        walk = safe_parse(row)
        if walk is not None:
            yield walk
