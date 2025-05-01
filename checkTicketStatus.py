from nicegui import ui, app
#TODO
#user or admin can delete ticket and check status

def ticket_details(tid, cur):
    print("showing detail")
    pass


def status(cur):

    username = app.storage.user.get('username', None)
    userid = app.storage.user.get('user_id', None)
    is_user_admin = app.storage.user.get('is_admin', False)

    #takes them back to home screen
    if username is None:
        return ui.navigate.to('/login?redirect_url=/admin')

    cur.execute("""
        SELECT t.tid, t.subject, t.location, t.description, status
        FROM tickets t
        JOIN reports r ON t.tid=r.tid 
        JOIN ticketstatus s ON t.tid=s.tid
        WHERE r.reporterid=%s
    """, [userid])
    tickets = cur.fetchall()

    columns = [
         {'name': 'tid', 'label': 'Ticket ID', 'field': 'tid', 'sortable': True},
         {'name': 'subject', 'label': 'Subject', 'field': 'subject', 'sortable': True},
         {'name': 'location', 'label': 'Location', 'field': 'location', 'sortable': True},
         {'name': 'description', 'label': 'Description', 'field': 'description', 'sortable': True},
         {'name': 'status', 'label': 'Status', 'field': 'status', 'sortable': True},
         #{'name': 'reporterid', 'label': 'Reporter ID', 'field': 'reporterid', 'sortable': True},
    ]

    rows = [{
        'tid': t['tid'],
        'subject': t['subject'],
        'location': t['location'],
        'description': t['description'],
        'status': t['status'],
        #'reporterid': t['reporterid']
    } for t in tickets]

    with ui.card().classes('mt-6'):
        ui.label("My Tickets").classes('text-xl font-bold')
        table = ui.table(columns=columns, rows=rows, row_key='tid', selection='single', on_select = lambda e: click_ticket(t)).classes('w-full')

        ui.button('Back to Home', on_click=lambda: ui.navigate.to('/')).classes('bg-green-500 text-white')


