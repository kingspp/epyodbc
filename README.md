<!-- Start of Badges -->
![version badge](https://img.shields.io/badge/epyodbc%20version-0.1.8-blue.svg)
![docs badge](https://img.shields.io/badge/docs-passing-green.svg)
![commits badge](https://img.shields.io/badge/commits%20since%200.1.8-5-green.svg)
![footprint badge](https://img.shields.io/badge/mem%20footprint%20-0.06%20Mb-lightgrey.svg)
<!--![build badge](https://img.shields.io/badge/build-passing-green.svg)
![coverage badge](https://img.shields.io/badge/coverage-87.78%25|%205.8k/6.6k%20lines-green.svg)
![test badge](https://img.shields.io/badge/tests-418%20total%7C418%20%E2%9C%93%7C0%20%E2%9C%98-green.svg)  -->

<!-- End of Badges -->

# EPyODBC

PyODBC is geared towards software developers with a focus on building enterprise applications.
<ul>
<li><b>Bridging Data Science</b> -  Data Scientists and Experimentalists have specific needs and to achieve the same using standard ORM tool can be an arduous task </li>

<li><b>GUI</b> - Graphical User Interface provides makes a job easy as it just takes a few clicks to learn about a feature</li>
</ul>

## Features
1. Schema Visualization (Supports both Image and Tree Format)
2. Table Autompletion, Info, Description and Head
3. Tables are lazily evaluation
4. Support for Dask Dataframe for dense tables
5. Queries returned as Pandas DF

## Requirements
Python 3.7+
Jupyter Lab (Support for custom widgets)
MSSQL instance and PyODBC drivers

## Installation
```bash
pip install git+https://github.com/kingspp/epyodbc.git#egg=epyodbc
```

## Connect to a Database
```python
# Import Database
from epyodbc import Database

# Using config
config = {
    "host": "0.0.0.0",
    "port": "1433",
    "database": 'master',
    "username": "username",
    "password": "password"
}

# Create a Database object using config
db = Database(config=config)
```

Get started with - [Starter kit Jupyter Notebook](https://github.com/kingspp/epyodbc/blob/master/notebooks/EPyODBC%20Introduction.ipynb)


