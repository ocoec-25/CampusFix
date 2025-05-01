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
        insert_ticket(cur)
        step2_card.set_visibility(True)

    def insert_ticket(cur):
        new_tid = get_new_tid(cur)
        cur.execute("INSERT INTO tickets (tid, subject, location, description, priority) VALUES (%d, %s, %s, %s, %d)", [new_tid, subject_input, location_input, description_input, priority_input])
        return


    with ui.card() as step1_card:
        with ui.row():
            subject_input = ui.input(label = "Subject", placeholder = "Start Typing").classes("w-64")
            location_input = ui.input(label = "Location", placeholder = "Start Typing").classes("w-64")
            description_input = ui.input(label = "Description", placeholder = "Start Typing").classes("w-64")
            priority_input = ui.select(['1', '2', '3', '4', '5'],value = "1", label="Priority").classes("w-64")
        ui.button("Submit Ticket", on_click=lambda: insert_reports(cur))

    with ui.card() as step2_card:

#add function that finds the most recent ticket number and adds one
#TODO
def get_new_tid(cur):
    cur.execute("SELECT MAX(tid) from reports")
    new_tid = cur.fetchall
    new_tid = new_tid + 1
    return new_tid

"""
def insert_reports(cur):
    new_tid = get_new_tid(cur)
    user_id = app.storage.user.get("userid", None)
    cur.execute("INSERT INTO reports (reporterid, tid) VALUES (%d, %d)", [user_id, new_tid])

def insert_ticket(cur):
    cur.execute("")
"""