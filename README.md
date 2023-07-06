# Process chemicals

Gets and processes chemical data for use in the OTT

## Implementation steps

- Create and activate a virtual environment, e.g.

  `python3 -m venv venv/`

  `source venv/bin/activate`

## Installation

- Install necessary Python modules via `pip3 install -r requirements.txt`

## Environment variable settings:

- CSV_PATH = where the commodity code CSV file is stored.
- REMOTE_URL = path template to access the chemicals

## Usage

### To download raw data

`python3 download.py`

### To process that data

`python3 process.py`
