# -*- coding: utf-8 -*-
"""
| **@created on:** 9/4/20,
| **@author:** prathyushsp,
| **@version:** v0.0.1
|
| **Description:**
| 
|
| **Sphinx Documentation Status:** 
"""
from epyodbc.constructs.base_class import BaseClass
from epyodbc.constructs.table import Table


class Schema(BaseClass):
    def __init__(self, database: str):
        self.database = database
        self.tables = []

    def add_table(self, table: Table):
        self.tables.append(table)

    def pretty(self):
        return {
            "database": self.database,
            "tables": {t.table_name: t.pretty() for t in self.tables}
        }
