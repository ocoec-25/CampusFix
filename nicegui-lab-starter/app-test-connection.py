import psycopg
from nicegui import ui
from dbinfo import *

ui.label('Welcome to NiceGUI!')
conn = psycopg.connect(f"host=dbclass.rhodescs.org dbname=practice user={DBUSER} password={DBPASS}")

# Print the connection status
ui.label(f"Database: {conn.info.dbname}")
ui.label(f"User: {conn.info.user}")
ui.label(f"Host: {conn.info.host}")
ui.label(f"Port: {conn.info.port}")
ui.label(f"Backend PID: {conn.info.backend_pid}")
ui.label(f"Server version: {conn.info.server_version}")
ui.label(f"Default client encoding: {conn.info.encoding}")

ui.run()