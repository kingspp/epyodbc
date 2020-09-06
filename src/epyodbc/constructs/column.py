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
from epyodbc.constructs.foreign_key import ForeignKey
import json


class Column(BaseClass):

    def __init__(self, column_name: str,
                 dtype: str,
                 length: int,
                 allow_null: bool,
                 is_primary_key: bool,
                 is_foreign_key: bool,
                 foreign_key: ForeignKey,
                 # is_unique: bool,
                 # default: typing.Optional
                 ):
        self.column_name = column_name
        self.dtype = dtype
        self.length = length
        self.allow_null = allow_null
        self.is_primary_key = is_primary_key
        self.is_foreign_key = is_foreign_key
        self.foreign_key = foreign_key

        # self.is_unique = is_unique
        # self.default = default

    def pretty(self):
        # ret = f"{self.column_name} {self.dtype}({self.length})"
        ret = f"{self.dtype}({self.length})"
        if self.is_primary_key:
            ret += "| PRIMARY "
        if self.is_foreign_key:
            ret += f"| FK ({self.foreign_key.pretty()})"
        return ret
