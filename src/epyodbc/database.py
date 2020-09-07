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

__all__ = ['Database']

import pyodbc
import IPython.display
from epyodbc.constructs import Schema, Table, Column, ForeignKey
import pandas as pd
from graphviz import Source
import pydot
import typing
import dask.dataframe as dd
import os
import json


class Database(object):
    """

    """

    def __init__(self, config: dict = None, config_file_path: str = None):
        try:
            if config is None:
                if config_file_path is None:
                    if 'EPYODBC_DBCONFIG' not in os.environ:
                        raise Exception(
                            "Server credentials missing! Set EPYODBC_DBCONFIG Environment variable or pass configs/config_file_path to the constructor")
                    else:
                        config_file_path = os.environ['EPYODBC_DBCONFIG']
                print(f"Loading server config from : {config_file_path}")
                config = json.load(open(config_file_path))
        except Exception as e:
            print(e)
            exit(1)

        assert "host" in config, f"host key missing in config file: {config_file_path}"
        assert "port" in config, f"port key missing in config file: {config_file_path}"
        assert "database" in config, f"database key missing in config file: {config_file_path}"
        assert "username" in config, f"username key missing in config file: {config_file_path}"
        assert "password" in config, f"password key missing in config file: {config_file_path}"

        self.host = config["host"]
        self.port = config["port"]
        self.database = config["database"]
        self.username = config["username"]
        self.password = config["password"]
        self.conn = self.connect()
        self.SKIP_TABLES = ['MSreplication_options', 'spt_fallback_db', 'spt_fallback_dev', 'spt_fallback_usg',
                            'spt_monitor', 'trace_xe_action_map', 'trace_xe_event_map']
        self.tables = []
        self.index_cols = {}
        for row in self.conn.cursor().tables(tableType='TABLE'):
            if row.table_name not in self.SKIP_TABLES:
                self.tables.append(row.table_name)
        for table in self.tables:
            self.index_cols[table] = list(self.conn.cursor().primaryKeys(table))[0][3]
        for table in self.tables:
            self.__setattr__(f"{table}_", dd.read_sql_table(table=f"{table}",
                                                            uri=f'mssql+pyodbc://{config["username"]}:{config["password"]}@{config["host"]}:{config["port"]}/{config["database"]}?DRIVER={{ODBC Driver 17 for SQL Server}};',
                                                            index_col=self.index_cols[table]))

    def connect(self):
        try:
            conn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + self.host + ',' + self.port + ';DATABASE=' + self.database + ';UID=' + self.username + ';PWD=' + self.password)
            print("Connected to DB Successfully")
            return conn
        except Exception as e:
            print("Unable to connect to DB")
            print(e)
            exit(1)

    def query(self, query: str):
        return pd.read_sql(query, con=self.conn)

    def visualize(self, tables: typing.Union[str, typing.List[str]] = None, render=True):
        start = "digraph {" \
                'graph [pad="0.5", nodesep="0.5", ranksep="2"];' \
                'node [shape=plain]' \
                'rankdir=LR;'
        end = '}'
        str_buffer = [start]
        schema = self.describe(pretty=False, jupyter=False, return_schema=True)

        # check if table is a str
        if isinstance(tables, str):
            tables = [tables]
        else:
            tables = self.tables

        for table in schema.tables:
            if table.table_name in tables:
                table_str = f'{table.table_name} [label=<<table border="0" cellborder="1" cellspacing="0">' \
                            f'<tr><td bgcolor="lightblue2"><font face="Times-bold" point-size="20">{table.table_name}</font></td></tr>'
                for e, column in enumerate(table.columns):
                    if column.is_primary_key:
                        table_str += f'<tr><td bgcolor="#FFCCCB" port="{e}">{column.column_name}&nbsp;&nbsp;<i>&lt;{column.dtype}({column.length})&gt;</i></td></tr>'
                    elif column.is_foreign_key:
                        table_str += f'<tr><td bgcolor="#FFED83" port="{e}">{column.column_name}&nbsp;&nbsp;<i>&lt;{column.dtype}({column.length})&gt;</i></td></tr>'
                    else:
                        table_str += f'<tr><td port="{e}">{column.column_name}&nbsp;&nbsp;<i>&lt;{column.dtype}({column.length})&gt;</i></td></tr>'

                table_str += f'</table>>];'
                str_buffer.append(table_str)

        # Build Relationships
        for table in schema.tables:
            if table.table_name in tables:
                for fk in table.foreign_keys:
                    from_table = table.table_name
                    from_port = [e for e, column in enumerate(table.columns) if column.column_name == fk.column_name][0]
                    to_table = fk.foreign_key.table
                    f_table = [table for table in schema.tables if table.table_name == fk.foreign_key.table][0]
                    to_port = \
                        [e for e, column in enumerate(f_table.columns) if column.column_name == fk.foreign_key.key][0]
                    str_buffer.append(f'{from_table}:{from_port} -> {to_table}:{to_port};')
        str_buffer.append(end)
        str_buffer = "\n".join(str_buffer)
        if render:
            g = pydot.graph_from_dot_data(str_buffer)[0]
            return Source(g)
        else:
            return str_buffer

    def describe(self, tables: typing.Union[str, typing.List[str]] = None, pretty=True, jupyter=True, debug=False,
                 return_json=False, return_schema=False):
        if isinstance(tables, str):
            tables = [tables]
        else:
            tables = self.tables

        schema = Schema(database=self.database)
        cursor = self.conn.cursor()
        # Add tables

        for t_name in self.tables:
            if t_name in tables:
                table = Table(table_name=t_name)
                if debug:
                    print(f"Processing table: {table.table_name}")
                table_primary_key = list(cursor.primaryKeys(t_name))[0][3]
                table_foreign_keys = []
                for fk in cursor.foreignKeys(t_name):
                    table_foreign_keys.append((fk[3], ForeignKey(table=fk[6], key=fk[7])))

                for row in cursor.columns(t_name):
                    is_primary_key = True if row.column_name == table_primary_key else False
                    is_foreign_key = [fk[1] for fk in table_foreign_keys if fk[0] == row.column_name]
                    col = Column(column_name=row.column_name, dtype=row.type_name, length=row.column_size,
                                 allow_null=bool(row.nullable),
                                 is_primary_key=is_primary_key,
                                 is_foreign_key=bool(is_foreign_key),
                                 foreign_key=is_foreign_key[0] if bool(is_foreign_key) else None)
                    table.add_column(column=col)
                    if is_primary_key:
                        table.set_primary_key(column=col)

                    if bool(is_foreign_key):
                        table.add_foreign_key(column=col)

                schema.add_table(table=table)
        if pretty:
            data = schema.pretty()
        else:
            data = schema.toJSON()

        if jupyter:
            return IPython.display.JSON(data, root="Schema")
        elif return_schema:
            return schema
        elif return_json:
            return data
        else:
            print(data)
