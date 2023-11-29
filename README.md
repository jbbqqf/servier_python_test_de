# Drugs data pipelines

## Getting started

This documentation is written for Ubuntu/Debian based distributions.

If you're on Windows, we highly recommend using WSL (Windows Subsystem for
Linux) in order to be as close as possible to the production environment. Setup
everything (git, Python, etc.) on WSL to avoid hard drive latency issues.

### Why Python3.8.12?

Because it's the Python version supported by the latest version of Cloud
Composer
(https://cloud.google.com/composer/docs/concepts/versioning/composer-versions#images).

If the digital strategy of our company is based on GCP and that company is using airflow,
then we should be interested to deploy in production on composer at some point.

We don't need Python's latest features. We prefer stability. It is important to stick
as close as possible to the production in a development environment.

### How to install Python3.8.12?

You can manually compile Python versions. pyenv is a nice alternative that
allows to install any Python version in one command.

Install pyenv:
```
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev \
libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python3-openssl

curl https://pyenv.run | bash

pyenv install 3.8.12
```

How to use the version installed with pyenv?
```
pyenv exec python
```

How to create a virtualenv with pyenv?
```
pyenv shell 3.8.12 && pyenv exec python -m venv venv
```

You can then activate your virtualenv and fallback with standard virtualenv
commands.
```
source venv/bin/activate
deactivate
```

Note: Once in your virtualenv, make sure pip is upgraded to the latest version.
```
pip install --upgrade pip
```

Troubleshooting:
```
which python

pyenv versions

pyenv exec which python
```

### Install a development environment

```
git clone git@github.com:jbbqqf/servier_python_test_de.git
cd servier_python_test_de
pyenv shell 3.8.12 && pyenv exec python -m venv venv
pip install --upgrade pip
pip install --no-deps -r requirements.txt
```

Set `AIRFLOW_HOME` to the appropriate directory:
```
echo "export AIRFLOW_HOME=`pwd`/src/" >> ~/.bashrc
```

Ensure the variable `AIRFLOW__CORE__LOAD_EXAMPLES` is set to `False` to hide
Airflow's example dags:
```
echo "export AIRFLOW__CORE__LOAD_EXAMPLES=False" >> ~/.bashrc
```

Make sure to reload your environment variables:
```
source ~/.bashrc
```

Run Airflow in local:
```
airflow standalone
```

## Procedures

### How to compile dependencies ?

We want our builds to be deterministic (for reproductibility).

In order to achieve this, dependencies are compiled with pip-tools. This allows
us to maintain only direct dependencies pinning while benefiting from indirect
dependencies pinning with a surgical precision.

```
pyenv shell 3.8.12 && pyenv exec python -m venv venv_build
source venv_build/bin/activate
pip install --upgrade pip
pip install -r requirements-build.txt
pip-compile --generate-hashes requirements.in
```

This will generate the `requirements.txt` file from which developers can install
dependencies.

## How to improve this project?

### How to handle large volumes of data?

We should consider ELT and execute SQL queries in a well dimensioned database to help with scaling issues.

The data warehouse / lakehouse can be Postgresql if we're dealing with < 1 To. There would be a lot of
conditions for Postgresql to be a viable option. But it would have some niche advantages such as
frequent updates or a flat price. Moreover, if we stick to standard SQL, that would ease a hypothetical
migration to BigQuery.

The go-to choice for a data warehouse in GCP is of course BigQuery. That would ensure that we can query
Po of data in minutes. Among all other interesting features, BigQuery is well suited for small use cases
and don't require to manage the infra in order for it to scale.

What to look for if we're dealing with BigData ? Partitioning the data. Clustering the data. Designing
tasks with backfill in mind. Idempotency will help to support backfills.

If for a specific reason we should stick with ETL and process data in python, then we might want to rewrite
the processing to avoid loading everything in RAM at once.

### DevOps

- CODEOWNERS file
- dependabot file
- use GCS buckets instead of local files
- terraform folder with IaC for composer, IAM, etc.

### CI

Add more tests.

Track (enforce?) coverage.

### CD

Add a github action to push from github to composer's GCS bucket (considering this project will be scheduled
with google cloud composer).

The CD can be a simple workflow based on the `gcloud utils rsync` command.

The workflow can be triggered when a user pushes a new tag with a pattern like `drugs/vX.Y.Z`.

### Data Quality

I made a lot of assumptions that the data is clean in my implementation.

In order to take the decision to implement quality checks, I would need to know the level of
confidence that we expect (is there an SLO to define with the product owner?).

Then, we could decide whether it's worth it or not to protect the pipeline (data contracts?).

Since we're dealing with analytical use cases (!= operational), we can also keep the implementation
lightweight, monitor the quality downstream and ship fixes only when proven necessary.

### Data Catalog

I chose to split the pipelines with the bronze/silver/gold pattern. In a production context, I should
make sure to use the good business terms and check that the data exposed in the gold layer is documented.

### Atomicity

I'm not sure about the atomicity of the dag's tasks. Since it's a small use case I tried to keep
the implementation simple.

### Incident management

I didn't explicitly handle failures (thanks to airflow's `on_failure_callback` or with trigger rules).
In a production scenario with Composer, I would suggest using Google Cloud Monitoring to detect dag
failures and send monitoring alerts.

Of course, it depends on the company's digital strategy to handle failures.

I should also add an SLA on the dag (thanks to airflow's SLA feature). This would cover the case
when we don't have a python exception but a particularly slow dag run.
