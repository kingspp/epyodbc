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
from epyodbc.constructs.column import Column


class Table(BaseClass):

    def __init__(self, table_name: str):
        self.table_name = table_name
        self.columns = []
        self.primary_key = None
        self.foreign_keys = []

    def add_column(self, column: Column):
        self.columns.append(column)

    def set_primary_key(self, column: Column):
        self.primary_key = column

    def add_foreign_key(self, column: Column):
        self.foreign_keys.append(column)

    def pretty(self):
        return {
            "table_name": self.table_name,
            "primary_key": self.primary_key.pretty(),
            "columns": [col.pretty() for col in self.columns],
            "foreign_keys": [fk.pretty() for fk in self.foreign_keys]
        }
