# Copyright (c) 2021, Drakecall. All rights reserved.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; version 2 of the
# License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
# 02110-1301  USA

# MySQL Workbench Plugin - Written in MySQL Workbench 6.2.3

# An utility to generate data dictionaries (DBDoc)

# Install it through Scripting/Install Plugin/Module menu
# select DBDocPy.py file, restart MWB for the change to take effect.

# It can be accessed through Tools/Utilitere menu, there are 2 options:
# A text version, displayed at MWB console
# An HTML version, exported to a file

# https://github.com

from wb import *
import grt
import ntpath
from mforms import FileChooser
import mforms

ModuleInfo = DefineModule(name="Drake DBDocPy2", author="Fernando Leal", version="1.0", description="Data Dictionary")


@ModuleInfo.plugin("drake.DBDocPy2.htmlDataDictionary", caption="DBDoc: As HTML File",
                   description="Data Dictionary as HTML", input=[wbinputs.currentDiagram()], pluginMenu="Utilities")

@ModuleInfo.export(grt.INT, grt.classes.db_Catalog)
def htmlDataDictionary(diagram):
    # Put plugin contents here
    htmlOut = ""
    filechooser = FileChooser(mforms.SaveFile)
    if filechooser.run_modal():
        htmlOut = filechooser.get_path()
        print("HTML File: {html}".format(html=htmlOut))
    if len(htmlOut) <= 1:
        return 1
    # iterate through columns from schema
    tables =''
    for figure in diagram.figures:
        if hasattr(figure, "table") and figure.table:
            tables += writeTableDoc(figure.table)
    htmlFile = open("%s.html" % (htmlOut), "w")
    htmlFile.write("<html><head>")
    htmlFile.write("<title>Data dictionary: {dic}</title>".format(dic=path_leaf(htmlOut)))

    htmlFile.write("""<style>
    td,th {
      text-align:center;
      vertical-align:middle;
    }
    table {
      border-collapse: collapse;
    }
    caption, th, td {
      padding: .2em .8em;
      border: 1px solid #fff;
    }
    caption {
      background: #dbb768;
      font-weight: bold;
      font-size: 1.1em;
    }
    th {
      font-weight: bold;
      background: #f3ce7d;
    }
    td {
      background: #ffea97;
    }
    </style>
    </head>
    <body>""")
    htmlFile.write("<img src='{name}.png'>".format(name=path_leaf(htmlOut)))

    htmlFile.write(tables)

    htmlFile.write("</body></html>")

    print(htmlFile)
    return 0

def writeTableDoc(table):
        htmlFile = ''
        htmlFile += "<table><caption>Table: {name} -{comment}</caption>".format(name=table.name, comment=table.comment)
        htmlFile += """<tr><td colspan=\"7\">Attributes</td></tr>
        <tr>
        <th>Name</th>
        <th>Type</th>
        <th>Not Null</th>
        <th>PK</th>
        <th>FK</th>
        <th>Default</th>
        <th>Comment</th>
        </tr>"""
        for column in table.columns:
            pk = ('No', 'Yes')[bool(table.isPrimaryKeyColumn(column))]
            fk = ('No', 'Yes')[bool(table.isForeignKeyColumn(column))]
            nn = ('No', 'Yes')[bool(column.isNotNull)]
            htmlFile += "<tr><td>{name}</td><td>{type}</td><td>nn</td><td>pk</td><td>fk</td><td>default</td><td>comment</td></tr>".format(
            name=column.name, type=column.formattedType, nn=nn, pk=pk, fk=fk, default=column.defaultValue, comment=column.comment)

        if (len(table.indices)):
            htmlFile += "</table></br>"
            for index in table.indices:
                htmlFile += "<table><caption>Index: {name}</caption>".format(name=index.name)
                htmlFile += """<tr><td colspan=\"4\">Attributes</td></tr>
                <tr>
                <th>Name</th>
                <th>Columns</th>
                <th>Type</th>
                <th>Description</th>
                </tr>
                """
                htmlFile += "<tr><td>{name}</td><td>ref</td><td>type</td><td>comment</td></tr>".format(
                name=index.name, ref=map(lambda x: "`" + x.referencedColumn.name + "`", index.columns),type=index.indexType,comment=index.comment)
                htmlFile += "</table></br>"

        htmlFile += "</table></br>"
        return htmlFile

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)
