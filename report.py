"""HW3 · report.py: add up the steps and save a report as JSON. Practises Session 7 (writing
and reading JSON) and Session 9 (a context manager)."""

from contextlib import contextmanager
import json
from pathlib import Path
from typing import Iterable, Iterator

from walks import Walk, good_walks, read_rows


def steps_per_day(walks: Iterable[Walk]) -> dict[str, int]:
    """Total steps for each date, with the dates in order, earliest first."""
    totals: dict[str, int] = {}
    for walk in walks:
        totals[walk.date] = totals.get(walk.date, 0) + walk.steps

    return {day: totals[day] for day in sorted(totals)}


def best_day(totals: dict[str, int]) -> str:
    """The date with the most steps. On a tie, the earliest of those dates."""
    if not totals:
        raise ValueError("totals is empty")

    max_steps = max(totals.values())
    return min(day for day, total in totals.items() if total == max_steps)


@contextmanager
def saved_safely(path: Path | str) -> Iterator:
    """Write to a new file, and put it in place of `path` only if the with block ends without an error."""
    target = Path(path)
    tmp_path = target.with_name(target.name + ".tmp")
    try:
        with open(tmp_path, "w", encoding="utf-8") as file:
            yield file
        tmp_path.replace(target)
    except Exception:
        tmp_path.unlink(missing_ok=True)
        raise


def write_report(path: Path | str, walks: Iterable[Walk]) -> dict:
    """Save the week's report to a JSON file, and return it as a dict."""
    days = steps_per_day(walks)
    best = best_day(days)
    total_steps = sum(days.values())

    report = {
        "total_steps": total_steps,
        "best_day": best,
        "days": days,
    }

    with saved_safely(path) as file:
        json.dump(report, file, indent=2)

    return report


def load_report(path: Path | str) -> dict | None:
    """The report saved last time, or None if there is no file or it is not valid JSON."""
    try:
        with open(path, encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


if __name__ == "__main__":
    # Provided: runs only with `python report.py`, not on import.
    here = Path(__file__).parent
    last_time = load_report(here / "report.json")
    report = write_report(here / "report.json", good_walks(read_rows(here / "walks.csv")))
    print(f"{report['total_steps']} steps this week. Best day: {report['best_day']}.")
    if last_time is not None:
        print(f"Last time you saved {last_time['total_steps']} steps.")