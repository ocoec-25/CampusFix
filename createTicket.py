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

    def went_wrong(cur):
        ui.button("Something went wrong. Please make sure all fields are filled in. Press this to reenter")
        step1_card.set_visibility(True)
        step2_card.set_visibility(False)

    with ui.card() as step1_card:
        with ui.row():
            subject_input = ui.input(label = "Subject", placeholder = "Start Typing").classes("w-64")
            location_input = ui.input(label = "Location", placeholder = "Start Typing").classes("w-64")
            description_input = ui.input(label = "Description", placeholder = "Start Typing").classes("w-64")
            priority_input = ui.select(['1', '2', '3', '4', '5'],value = "1", label="Priority").classes("w-64")
        ui.button("Submit Ticket", on_click=lambda: step2_card.set_visibility(True))


    with ui.card() as step2_card:
        step1_card.set_visibility(False)
        if subject_input == '':
            went_wrong(cur)
        elif location_input == '':
            went_wrong(cur)
        elif description_input == '':
            went_wrong(cur)
        else:
            insert_reports(cur)
            insert_ticket(cur)

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