#!/bin/sh
. ./server/venv_ubuntu/bin/activate
/bin/python3 ./server/management/facade_db_admin.py populate_tables