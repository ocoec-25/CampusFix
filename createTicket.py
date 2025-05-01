#TODO
from nicegui import ui, app
def ticket(cur):
    username = app.storage.user.get("username", None)
    if username is None:
        return ui.navigate.to('/login?redirect_url=/admin')

    def insert_reports(cur):
        new_tid = get_new_tid(cur)
        user_id = app.storage.user.get("userid", None)
        cur.execute("INSERT INTO reports (reporterid, tid) VALUES (%d, %d)", [user_id, new_tid])

    def insert_ticket(cur):
        cur.execute("")

#add function that finds the most recent ticket number and adds one
#TODO
def get_new_tid(cur):
    cur.execute("SELECT MAX(tid) from reports")
    new_tid = cur.fetchall
    new_tid += 1
    return new_tid

"""
def insert_reports(cur):
    new_tid = get_new_tid(cur)
    user_id = app.storage.user.get("userid", None)
    cur.execute("INSERT INTO reports (reporterid, tid) VALUES (%d, %d)", [user_id, new_tid])

def insert_ticket(cur):
    cur.execute("")
"""