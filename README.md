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


