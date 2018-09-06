# DBDoc
Mysql Workbench DBDoc to html

#MySQL Workbench Model Document Generation
A Python script to generate documentation from MySQL Workbench ERR diagram.

##Installation
* Download the latest release from [Github](https://github.com/ferleal/DBDoc/releases)
* Extract the downloaded file and find a file named DBDocPy2.py
* Open the MySQL Workbench
* Navigate to menu Scripting > Install Plugin/Module...
* Browse and select the extracted .py file
* Restart the Workbench
* Files bower_components/bootstrap/dist/css/bootstrap.min.css and dist/css/AdminLTE.min.css are required to table style.

###Usage
* Open Modal
* Export your modal as png
* Click Tools / Utilities / DBDoc as Html
* Go to the same folder you export your png, and use the same name example : modal.png , on file browser , type : modal

###It was a quick and dirty join of two scripts
* [DBDocPy](https://github.com/rsn86/MWB-DBDocPy)
* [mysql-workbench-plugin-doc-generating](https://github.com/letrunghieu/mysql-workbench-plugin-doc-generating)

