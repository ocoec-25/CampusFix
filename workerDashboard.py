from nicegui import ui, app


def worker(cur):
    username = app.storage.user.get('username', None)
    is_user_worker = app.storage.user.get('is_worker', False)

    if username is None:
        return ui.navigate.to('/login?redirect_url=/admin')

    if not is_user_worker:
        with ui.card().classes('w-96 mx-auto mt-8 bg-red-100'):
            ui.label("Access Denied: Administrator privileges required").classes('text-red-600 font-bold')
            ui.button('Back to Home', on_click=lambda: ui.navigate.to('/')).classes('bg-blue-500 text-white mt-4')
        return

    ui.label("Worker Dashboard").classes('text-2xl font-bold mb-4')

    with ui.tabs().classes('w-full') as tabs:
        tickets_tab = ui.tab('Tickets assigned to me')


    with ui.tab_panels(tabs, value=tickets_tab).classes('w-full'):
        with ui.tab_panel(tickets_tab):
            show_tickets_worker(cur)



def show_tickets_worker(cur):
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

    columns = [
        {'name': 'tid', 'label': 'ID', 'field': 'tid', 'sortable': True},
        {'name': 'subject', 'label': 'Subject', 'field': 'subject', 'sortable': True},
        {'name': 'location', 'label': 'Location', 'field': 'location', 'sortable': True},
        {'name': 'status', 'label': 'Status', 'field': 'status', 'sortable': True},
        {'name': 'reporter', 'label': 'Reporter', 'field': 'reporter_name', 'sortable': True},
        {'name': 'priority', 'label': 'Priority', 'field': 'priority', 'sortable': True},
        {'name': 'adminPriority', 'label': 'Admin Priority', 'field': 'adminpriority', 'sortable': True},
    ]

    with ui.table(columns=columns, rows=tickets, row_key='tid').classes('w-full') as table:
        table.add_slot('body-cell-status', '''
            <q-td :props="props">
                <q-chip :color="props.value === 'open' ? 'green' : 'gray'">
                    {{ props.value }}
                </q-chip>
            </q-td>
        ''')

