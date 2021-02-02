# Convert xml to csv
The simple converter from xml registers for the bank to csv register for another bank program.

## Requirements
- python 3.8+
- clik
- loguru
- more requirements in requirements.txt

## Install
```
pip install -r requirements.txt
```

## Use
Run command with full path. For example
```
python cli.py ~/Desktop/sample.xml
```

## Linter
Run command local
```
flake8 --count
```
or run linter in docker
```
docker build -t converter . && docker run -it converter flake8 --count
```

## Test
Run command local
```
pytest
```
or run test in docker
```
docker build -t converter . && docker run -it converter pytest
```
