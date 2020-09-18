# -*- coding: utf-8 -*-
"""
| **@created on:** 9/17/20,
| **@author:** prathyushsp,
| **@version:** v0.0.1
|
| **Description:**
| 
|
| **Sphinx Documentation Status:** 
"""
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from bs4 import BeautifulSoup
import bs4

from collections import Counter

class Table():
    def __init__(self, iD, name, parent, x, y):
        """
            <mxCell id="4" style="table" parent="1" vertex="1">
      <Table name="LoadCell" as="value" />
      <mxGeometry x="4.5" y="105" width="200" height="80" as="geometry">
        <mxRectangle width="200" height="28" as="alternateBounds" />
      </mxGeometry>
    </mxCell>

        :param iD:
        :param name:
        """
        self.id = iD
        self.name = name
        self.elem = SubElement(parent, "mxCell",
                               {"id": str(iD), "parent": "1", "vertex": '1', "connectable": "0", "style":"table"})
        SubElement(self.elem, "Table", {"name": self.name, "as": "value"})
        geometry = SubElement(self.elem, "mxGeometry",
                              {"x": str(abs(x)), "y": str(abs(y)), "width": "200", "height": "80", "as": "geometry"})
        SubElement(geometry, "mxRectangle", {"width": "200", "height": "28", "as": "alternateBounds"})

    # def add_column(self, column):
    #     # SubElement()
    #     SubElement(self.elem)


class Column():
    """

    <mxCell id="5" parent="4" vertex="1" connectable="0">
      <Column name="TABLE2_ID" type="INTEGER" primaryKey="1" autoIncrement="1" as="value" />
      <mxGeometry y="28" width="200" height="26" as="geometry" />
    </mxCell>
    """

    def __init__(self, iD: int, parent, column_name: str, table: Table):
        self.cell = SubElement(parent, "mxCell",
                               {"id": str(iD), "parent": str(table.id), "vertex": '1', "connectable": "0"})
        column = SubElement(self.cell, "Column", {"name": column_name, "as": "value"})
        geometry = SubElement(self.cell, "mxGeometry",
                              {"name": column_name, "y": "28", "width": "200", "height": "26", "as": "geometry"})


class XMLGenerator():
    def __init__(self, svg, schema):
        """<mxGraphModel>
          <root>
            <mxCell id="0" />
            <mxCell id="1" parent="0" />
        """
        self.main = Element('mxGraphModel')
        root = SubElement(self.main, "root")
        SubElement(root, "mxCell", {"id": "0"})
        SubElement(root, "mxCell", {"id": "1", "parent": "0"})
        table_names  = [i.table_name for i in schema.tables]
        # Generate x and y
        xy_coords = {}
        self.parsed_svg = BeautifulSoup(svg, 'xml')
        for elems in self.parsed_svg.find('svg'):
            for inner_elem in elems:
                if isinstance(inner_elem, bs4.Tag):
                    for e, inner_2_elem in enumerate(inner_elem):
                        if isinstance(inner_2_elem, bs4.Tag):
                            # print(inner_2_elem, table_names)
                            if (inner_2_elem.name=='title' and list(inner_2_elem.children)[0] in table_names):
                                for pol in list(inner_elem.children)[e+1:]:
                                    if (pol.name=="polygon"):
                                        # print(inner_2_elem, pol)
                                        xy_coords[list(inner_2_elem.children)[0]]=pol.get("points").split(" ")[0]
        print(xy_coords)
        colId = len(table_names)+10
        for e, table in enumerate(schema.tables):
            # if (e>2):
            #     break
            xy = xy_coords[table.table_name].split(",")
            tb = Table(iD=e+2, name=table.table_name, parent=root, x=float(xy[0]), y=float(xy[1]))
            for column in table.columns:
                Column(column_name=column.column_name, parent=root, iD=colId, table=tb)
                colId+=1
            # tb.add_column(col)
            # table.add




        # print("-- ", type(elems))
        # print(elems)

    def generate(self):
        f = open("/Users/prathyushsp/Git/arl/adhesives/epyodbc/src/epyodbc/server/assets/data.xml", 'w')
        return f.write(BeautifulSoup(tostring(self.main), 'xml').prettify())
