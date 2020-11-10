# Git Profile API Challenge App

## Install:

You can use a virtual environment (conda, venv, etc):
```
conda env create -f environment.yaml
conda activate code-challenge
```

Or just pip install from the requirements file
``` 
pip install -r requirements.txt
```

## Running the code

### Spin up the service

```
# start up local server
python -m run 
```

### Making Requests

```
curl -i "http://127.0.0.1:5000/health-check"
```

Swagger API:
```
http://localhost:5000/apidocs
```

## Docs 

[Implimentation Docs](implimentation.md)

## Tests

### Env
You can use a virtual environment (conda, venv, etc):
```
conda env create -f environment.test.yaml
conda activate code-challenge-tests
```

Or just pip install from the requirements file
``` 
pip install -r requirements.test.txt
```
### Running tests

```
python -m unittest
```

## What'd I'd like to improve on...

1. There is overlap in the bitbucket/github API (especially aggragate). Would probably want to clean that up and make it more DRY
2. Tests are not complete ~ need more comperhensive testing around API responses
3. Handle failure cases, currently this works or a 500 is thrown 
4. Handle API authentication in a reasonable way
