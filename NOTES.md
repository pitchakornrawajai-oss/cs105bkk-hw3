# HW3 notes

Answer each question in a few sentences. Be specific: name the function, the error or the command.

## What did you try?
Making sure I did not loop over `walks` more than once when it is a generator, and writing `saved_safely` so a `.tmp` file only replaces the real file if nothing fails. It was also important to use `utf-8` when reading the CSV so Thai place names do not break on Windows.

## What broke, and how did you fix it?
Rows with `steps` as `"0"` should still be allowed, while negative numbers like `"-300"`, decimals like `"12.5"`, text like `"abc"`, or an empty `date` must raise `ValueError`. Also, when saving a report, if an error happens halfway through or if no walks are given, the old `report.json` should stay untouched.

## What would you do differently next time?
I practiced reading and writing UTF-8 CSV and JSON files safely, writing a decorator (`none_on_error`), generator functions (`read_rows`, `good_walks`), and a `@contextmanager` (`saved_safely`), and writing my own `pytest` tests using a fixture and `@pytest.mark.parametrize`.
