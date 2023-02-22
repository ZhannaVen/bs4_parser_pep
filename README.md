# Parsing - educational project

### Description

The project implements parsing of command line arguments to select the program operation mode. There are four modes available in total:

- whats-new (links to articles about innovations in Python)
- latest-versions (links to documentation for all versions of Python)
- download (download the documentation archive for the latest version of Python)
- pep (obtaining data on the statuses of all PEPs)

Logging is configured.

### Used frameworks and libraries:
- Python 3.7
- requests_cache
- Beautiful Soup
- tqdm
- prettytable

### How to start a project (Unix) 
- Clone repository:
```bash
git clone git@github.com:ZhannaVen/bs4_parser_pep.git
```
- Activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```
- Install dependencies:
```bash
pip install -r requirements.txt
```
- The parser is launched from the ./src/
```bash
python src/main.py --help
```

## Operating modes
- Help call:
```bash
python src/main.py --h
```
- Operating modes:
```bash
python src/main.py whats-new
python src/main.py latest-versions
python src/main.py download
python src/main.py pep
```
Optional arguments:
 - **-o {pretty, file}, --output {pretty, file}**: additional ways for data output (pretty - table, file - in .csv). Default output - line by line to terminal.
 - **-с, --clear-cache**: clearing the cache. 


## Author

- [Zhanna - Python-Developer](https://github.com/ZhannaVen)

