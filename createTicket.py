#TODO
from nicegui import ui, app
def ticket(cur):
    username = app.storage.user.get("username", None)
    userid = app.storage.user.get("userid", None)

    if username is None:
        return ui.navigate.to('/login?redirect_url=/admin')




#add function that finds the most recent ticket number and adds one
#TODO



def insert_ticket(cur):
    cur.execute("""Insert
    """)