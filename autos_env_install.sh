#!/bin/bash

apt-get install python-virtualenv
virtualenv Autos/flask
Autos/flask/bin/pip install flask
Autos/flask/bin/pip install flask-wtf
echo "from wtforms.fields.html5 import *" >> Autos/flask/lib/python2.7/site-packages/wtforms/fields/__init__.py
cd Autos && gnome-terminal -e ./run.py &

