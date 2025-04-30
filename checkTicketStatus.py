#TODO
#user or admin can delete ticket and check status
from nicegui import ui, app

def status(cur):

    username = app.storage.user.get('username', None)
    is_user_admin = app.storage.user.get('is_admin', False)

    #takes them back to home screen
    if username is None:
        return ui.navigate.to('/login?redirect_url=/admin')

    def show_status_admin():


    def show_status_user(cur):
        cur.execute("""
            SELECT t.tid, t.subject, t.location, t.description, t.priority, 
                   ts.status, ts.adminPriority, 
                   u.first_name || ' ' || u.last_name as reporter_name
            FROM tickets t
            JOIN ticketStatus ts ON t.tid = ts.tid
            JOIN reports r ON t.tid = r.tid
            JOIN users u ON r.reporterID = u.userID
            ORDER BY ts.adminPriority DESC
        """)
        tickets = cur.fetchall()

        ui.label("All Tickets").classes('text-xl font-bold mt-4')