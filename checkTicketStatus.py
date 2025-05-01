from nicegui import ui, app
#TODO
#user or admin can delete ticket and check status

def status(cur):

    username = app.storage.user.get('username', None)
    userid = app.storage.user.get('user_id', None)
    is_user_admin = app.storage.user.get('is_admin', False)
    #cur.execute("SELECT userid FROM users where email=%s", [username])
    #userid = cur.fetchone()
    #print(userid[0])
    #takes them back to home screen
    if username is None:
        return ui.navigate.to('/login?redirect_url=/admin')

    cur.execute("""
        SELECT t.tid, t.subject, r.reporterid
        FROM tickets t
        JOIN reports r ON t.tid=r.tid 
        WHERE r.reporterid=%s
    """, [userid])
    tickets = cur.fetchall()

    columns = [
         {'name': 'tid', 'label': 'ID', 'field': 'tid', 'sortable': True},
         {'name': 'subject', 'label': 'Subject', 'field': 'subject', 'sortable': True},
         {'name': 'reporterid', 'label': 'Reporter ID', 'field': 'reporterid', 'sortable': True},
    ]

    rows = [{'tid': t['tid'], 'subject': t['subject'], 'reporterid': t['reporterid']} for t in tickets]

    with ui.card().classes('mt-6'):
        ui.label("My Tickets").classes('text-xl font-bold')
        ui.table(columns=columns, rows=rows).classes('w-full')


