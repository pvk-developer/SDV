<p align="left">
<img width=15% src="https://dai.lids.mit.edu/wp-content/uploads/2018/06/Logo_DAI_highres.png" alt=“SDV” />
<i>An open source project from Data to AI Lab at MIT.</i>
</p>

[![PyPi][pypi-img]][pypi-url]
[![Travis][travis-img]][travis-url]
[![CodeCov][codecov-img]][codecov-url]
[![Downloads][downloads-img]][downloads-url]

[pypi-img]: https://img.shields.io/pypi/v/sdv.svg
[pypi-url]: https://pypi.python.org/pypi/sdv
[travis-img]: https://travis-ci.org/HDI-Project/SDV.svg?branch=master
[travis-url]: https://travis-ci.org/HDI-Project/SDV
[codecov-img]: https://codecov.io/gh/HDI-Project/SDV/branch/master/graph/badge.svg
[codecov-url]: https://codecov.io/gh/HDI-Project/SDV
[downloads-img]: https://pepy.tech/badge/sdv
[downloads-url]: https://pepy.tech/project/sdv

<h1>SDV - Synthetic Data Vault</h1>

Automated generative modeling and sampling

- License: MIT
- Documentation: https://HDI-Project.github.io/SDV
- Homepage: https://github.com/HDI-Project/RDT

## Overview

**SDV** allows the user to sample relational databases. Users can get easily access to information
about the relational database, create generative models for tables in the database and sample rows
from these models to produce synthetic data.

# Install

## Requirements

**SDV** has been developed and tested on [Python 3.5, 3.6 and 3.7](https://www.python.org/downloads)

Also, although it is not strictly required, the usage of a
[virtualenv](https://virtualenv.pypa.io/en/latest/) is highly recommended in order to avoid
interfering with other software installed in the system where **SDV** is run.

These are the minimum commands needed to create a virtualenv using python3.6 for **SDV**:

```bash
pip install virtualenv
virtualenv -p $(which python3.6) sdv-venv
```

Afterwards, you have to execute this command to have the virtualenv activated:

```bash
source sdv-venv/bin/activate
```

Remember about executing it every time you start a new console to work on **SDV**!

## Install with pip

After creating the virtualenv and activating it, we recommend using
[pip](https://pip.pypa.io/en/stable/) in order to install **SDV**:

```bash
pip install sdv
```

This will pull and install the latest stable release from [PyPi](https://pypi.org/).

## Install from source

With your virtualenv activated, you can clone the repository and install it from
source by running `make install` on the `stable` branch:

```bash
git clone git@github.com:HDI-Project/SDV.git
cd SDV
git checkout stable
make install
```

## Install for Development

If you want to contribute to the project, a few more steps are required to make the project ready
for development.

Please head to the [Contributing Guide](https://HDI-Project.github.io/SDV/contributing.html#get-started)
for more details about this process.

# Data Format

In order to work with **SDV** you will need to generate a `MetaData` that contains information
about the tables that you would like to sample and also provide those tables.

## Metadata

The `MetaData` can be either a `.json` file or a python `dict` object. This must contain the
following keys:

- Tables, representing a list with the keys of `headers`, `name`, `path`. `primary_key`, `use` and
`fields`.
- Fields, representing a list that contains  describes each field type.

```
{
    "tables": [
        {
            "headers": true,
            "name": "table_1",
            "path": "table_1.csv",
            "primary_key": "id",
            "use": true,
            "fields": [
                {
                    "name": "id",
                    "type": "id",
                    "subtype": "number"
                },
                {
                    "name": "date_field",
                    "type": "datetime",
                    "format": "%Y-%m-%d"
                },
                {
                    "name": "categorical_field",
                    "type": "categorical",
                    "subtype": "categorical"
                },
                {
                    "name": "integer_field",
                    "type": "number",
                    "subtype": "integer"
                },
                {
                    "name": "float_field",
                    "type": "number",
                    "subtype": "float"
                },
                ...
            ]
        },
        {
            "headers": true,
            "name": "table_2",
            "path": "table_2.csv",
            "primary_key": "id",
            "use": true,
            "fields": [
                {
                    "name": "user_id",
                    "ref": {
                        "field": "id",
                        "table": "users"
                    },
                    "type": "id",
                    "subtype": "number"
                },
                ...
            ]
        }
    ]
}
```


# Quickstart

In this short series of tutorials we will guide you through a series of steps that will help you
getting started using **SDV** to sample columns, tables and datasets.

## 1. Create some demo data and metadata

In the example below we will create a `pandas.DataFrame` that contains one of each types that
**SDV** can sample (`numerical`, `categorical`, `bool`, `datetime`).

```python
import pandas as pd
import numpy as np

data = pd.DataFrame({
    'integer': [1, None, 1, 2, 1, 2, 3, 2],
    'float': [0.1, None, 0.1, 0.2, 0.1, 0.2, 0.3, 0.1],
    'categorical': ['a', 'b', 'a', 'b', 'a', None, 'c', None],
    'bool': [False, True, False, True, False, False, False, None],
    'nullable': [1, None, 3, None, 5, None, 7, None],
    'datetime': [
        '2010-01-01', '2010-02-01', '2010-01-01', '2010-02-01',
        '2010-01-01', '2010-02-01', '2010-03-01', None
    ]
})

data['datetime'] = pd.to_datetime(data['datetime'])

tables = {
    'data': data
}
```

If we print the content of this `data` we would recieve an output like this:

```
   integer  float categorical   bool  nullable   datetime
0      1.0    0.1           a  False       1.0 2010-01-01
1      NaN    NaN           b   True       NaN 2010-02-01
2      1.0    0.1           a  False       3.0 2010-01-01
3      2.0    0.2           b   True       NaN 2010-02-01
4      1.0    0.1           a  False       5.0 2010-01-01
5      2.0    0.2        None  False       NaN 2010-02-01
6      3.0    0.3           c  False       7.0 2010-03-01
7      2.0    0.1        None   None       NaN        NaT
```

Once we have our `tables` created, let's create the `metadata` dictionary corresponding to the
table `data`.

```
metadata = {
    "path": "",
    "tables": [
        {
            "fields": [
                {
                    "name": "integer",
                    "type": "number",
                    "subtype": "integer",
                },
                {
                    "name": "float",
                    "type": "number",
                    "subtype": "float",
                },
                {
                    "name": "categorical",
                    "type": "categorical",
                    "subtype": "categorical",
                    "pii": False,
                    "pii_category": "email"
                },
                {
                    "name": "bool",
                    "type": "categorical",
                    "subtype": "bool",
                },
                {
                    "name": "nullable",
                    "type": "number",
                    "subtype": "float",
                },
                {
                    "name": "datetime",
                    "type": "datetime",
                    "format": "%Y-%m-%d"
                },
            ],
            "headers": True,
            "name": "data",
            "path": "data.csv",
            "use": True
        }
    ]
}
```

More information about `MetaData` can be found [here](https://hdi-project.github.io/MetaData.json/index).

### 2. Create SDV instance and fit

Before sampling first we have to `fit` our `SDV`, in order to do so we have to import it,
instantiate it and fit it with the `metadata` and `tables` that we created before:

```python
from sdv import SDV

sdv = SDV()
sdv.fit(metadata, tables)
```

Once we start the fitting process, logger messages with the status will be displayed:

```
INFO - modeler - Modeling data
INFO - modeler - Modeling Complete
```

Once `Modeling Complete` is displayed, we can process to sample data.

### 3. Sample data

Sampling data once we have fitted our `sdv` instance is as simple as:

```python
samples = sdv.sample_all()
```

This will generate `5` samples of all the `columns` that we had in `data`. **Notice** that this
is sampled data, so you will probably obtain different results as the ones shown below.

```python
samples['data']

   integer     float categorical   bool  nullable                      datetime
0        2  0.177919         NaN  False       NaN 2010-02-08 04:56:42.038568192
1        3  0.249520           c  False       NaN 2010-02-19 21:30:27.231292160
2        2  0.161674         NaN    NaN       NaN                           NaT
3        0  0.031763           a   True       NaN 2009-12-13 21:23:44.602550528
4        3  0.323860           c  False       NaN 2010-03-01 08:08:26.009617408
```

# What's next?

For more details about **SDV** and all its possibilities and features, please check the
[project documentation site](https://HDI-Project.github.io/SDV/)!
