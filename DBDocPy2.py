# Copyright (c) 2016, Drakecall. All rights reserved.
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

ModuleInfo = DefineModule(name="Drake DBDocPy2", author="Fernando Leal - Mod. Nicolas Bustos", version="2.0", description="Data Dictionary")


@ModuleInfo.plugin("drake.DBDocPy2.htmlDataDictionary", caption="DBDoc: As HTML File",
                   description="Data Dictionary as HTML", input=[wbinputs.currentDiagram()], pluginMenu="Utilities")
@ModuleInfo.export(grt.INT, grt.classes.db_Catalog)
def htmlDataDictionary(diagram):
    # Put plugin contents here
    htmlOut = ""
    filechooser = FileChooser(mforms.SaveFile)
    if filechooser.run_modal():
        htmlOut = filechooser.get_path()
        print "HTML File: %s" % (htmlOut)
    if len(htmlOut) <= 1:
        return 1

    # iterate through columns from schema
    tables =''
    for figure in diagram.figures:
        if hasattr(figure, "table") and figure.table:
            tables += writeTableDoc(figure.table)


    htmlFile = open("%s.html" % (htmlOut), "w")
    print >> htmlFile, "<html>"
    print >> htmlFile, "<head>"
    print >> htmlFile, "<title>Data dictionary: %s</title>" % (path_leaf(htmlOut))

    print >> htmlFile, """
        <link rel="stylesheet" href="bower_components/bootstrap/dist/css/bootstrap.min.css">
        <!-- Theme style -->
        <link rel="stylesheet" href="dist/css/AdminLTE.min.css">
<style>
        
</style>
</head>
<body>
        <div class="wrapper">
                <section class="content">
                        <div class="row">
                                <div class="col-xs-12">"""
    print >> htmlFile, "<img src='%s.png'>" % (path_leaf(htmlOut))

    print >> htmlFile, "%s" % (tables)

    print >> htmlFile, """
					                                </div>
                                <!-- /.col -->
                        </div>
                        <!-- /.row -->
                </section>
                <!-- /.content -->
        </div>
        <h3>Style got from <a href="https://adminlte.io/themes/AdminLTE/index.html">AdminLTE</a></h3>
</body>

</html>
	"""

    return 0

def writeTableDoc(table):
        htmlFile = ''
        htmlFile += "<!-- Table: %s %s --><caption></caption>" % (table.name, table.comment)
        htmlFile += "<div class=\"box\"><div class=\"box-header\"><h3 class=\"box-title\">Table: %s</h3></div><!-- /.box-header -->" % (table.name)
        htmlFile += """<div class="box-body">
		<table class="table table-bordered table-striped">
        <tr><td colspan=\"7\">Attributes</td></tr>
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
            htmlFile += "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (
            column.name, column.formattedType, nn, pk, fk, column.defaultValue, column.comment)

        if (len(table.indices)):
            htmlFile += "</table>"
            for index in table.indices:
                htmlFile += "<div class=\"col-sm-12 col-md-6 col-lg-4\"><table class=\"table table-bordered table-striped\"><caption>Index: %s</caption>" % (index.name)
                htmlFile += """<tr><td colspan=\"4\">Attributes</td></tr>
                <tr>
                <th>Name</th>
                <th>Columns</th>
                <th>Type</th>
                <th>Description</th>
                </tr>
                """
                htmlFile += "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (
                index.name, map(lambda x: "`" + x.referencedColumn.name + "`", index.columns),index.indexType, index.comment)
                htmlFile += "</table></div>"

        htmlFile += "</div></div>"
        return htmlFile

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)
