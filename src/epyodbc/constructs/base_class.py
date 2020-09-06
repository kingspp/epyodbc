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
from abc import ABCMeta, abstractmethod
import json


class BaseClass(metaclass=ABCMeta):

    @abstractmethod
    def pretty(self):
        pass

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=2)
