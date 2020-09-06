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


class Database(object):
    def __init__(self, database: str, server: str, username: str, password: str):
        self.database = database
        self.server = server
        self.username = username
        self.password = password
        self.conn = self.connect()

    def connect(self):
        try:
            conn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + self.server + ';DATABASE=' + self.database + ';UID=' + self.username + ';PWD=' + self.password)
            print("Connected to DB Successfully")
            return conn
        except Exception as e:
            print("Unable to connect to DB")
            print(e)
            exit(1)

    def query(self, query: str):
        return pd.read_sql(query, con=self.conn)

    def visualize(self, tables: typing.Union[str, typing.List[str]] = None):
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

        for table in schema.tables:
            if table.table_name in tables:
                table_str = f'{table.table_name} [label=<<table border="0" cellborder="1" cellspacing="0">' \
                            f'<tr><td bgcolor="lightblue2"><font face="Times-bold" point-size="20">{table.table_name}</font></td></tr>'
                for e, column in enumerate(table.columns):
                    if column.is_primary_key:
                        table_str += f'<tr><td bgcolor="#FFCCCB" port="{e}">{column.column_name} <i>&lt;{column.dtype}({column.length})&gt;</i></td></tr>'
                    elif column.is_foreign_key:
                        table_str += f'<tr><td bgcolor="#FFED83" port="{e}">{column.column_name} <i>&lt;{column.dtype}({column.length})&gt;</i></td></tr>'
                    else:
                        table_str += f'<tr><td port="{e}">{column.column_name} <i>&lt;{column.dtype}({column.length})&gt;</i></td></tr>'

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
                    to_port = [e for e, column in enumerate(f_table.columns) if column.column_name == fk.foreign_key.key][0]
                    str_buffer.append(f'{from_table}:{from_port} -> {to_table}:{to_port};')
        str_buffer.append(end)
        g = pydot.graph_from_dot_data("\n".join(str_buffer))[0]
        return Source(g)

    def describe(self, pretty=True, jupyter=True, debug=False, return_json=False, return_schema=False):
        SKIP_TABLES = ['MSreplication_options', 'spt_fallback_db', 'spt_fallback_dev', 'spt_fallback_usg',
                       'spt_monitor',
                       'trace_xe_action_map', 'trace_xe_event_map']

        schema = Schema(database=self.database)
        cursor = self.conn.cursor()
        # Add tables
        temp_tables = []
        for row in cursor.tables(tableType='TABLE'):
            if row.table_name not in SKIP_TABLES:
                temp_tables.append(row.table_name)

        for t_name in temp_tables:
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
