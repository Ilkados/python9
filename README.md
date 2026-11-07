# Python data validation

Space-themed Pydantic models validate station records, alien contacts, and crew data. Start with the station model to see field constraints on crew size, power, and oxygen.

## Try the first example

From the repository root on a Unix-like system, create a fresh environment with Python 3.10 or newer.

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install 'pydantic>=2,<3'
python ex0/space_station.py
```

Read the [example source](ex0/space_station.py).
