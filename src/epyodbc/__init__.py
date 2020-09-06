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

__all__ = ['Database', '__version__', 'EPYODBC_MODULE_PATH']

from epyodbc.database import Database
import os
import json

EPYODBC_MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
metadata = json.load(open(EPYODBC_MODULE_PATH + "/metadata.json"))
__version__ = metadata['version']
