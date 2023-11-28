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

We don't need Python's latest features. We prefer stability.

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
