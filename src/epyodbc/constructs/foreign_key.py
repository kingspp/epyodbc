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

class ForeignKey(BaseClass):
    def __init__(self, table, key):
        self.table = table
        self.key = key

    def pretty(self):
        return f"{self.table} -> {self.key}"
