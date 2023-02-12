# Relay server to call the Voltalis API

[Voltalis](https://www.voltalis.com/) is a solution to manage your heaters.

## Setup

Create conda environnement:

```bash
conda create --name voltalisrelay python=3.10
conda activate voltalisrelay
```

Install the requirements:

```bash
pip install -r requirements.txt
```

## Run the server

Use the following command:

```bash
export VOLTALIS_USERNAME="you@example.com"
export VOLTALIS_PASSWORD="xxx"
uvicorn app.main:app
```

Access the OpenAPI specifications to know how to use it: <http://127.0.0.1:8000/docs>

## Build docker image

Run:

```bash
docker build -t voltalisrelay .
```
