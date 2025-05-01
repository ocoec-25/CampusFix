from nicegui import ui, app


def admin(cur):
    username = app.storage.user.get('username', None)
    is_user_admin = app.storage.user.get('is_admin', False)

    if username is None:
        return ui.navigate.to('/login?redirect_url=/admin')

    if not is_user_admin:
        with ui.card().classes('w-96 mx-auto mt-8 bg-red-100'):
            ui.label("Access Denied: Administrator privileges required").classes('text-red-600 font-bold')
            ui.button('Back to Home', on_click=lambda: ui.navigate.to('/')).classes('bg-blue-500 text-white mt-4')
        return

    ui.label("Administrator Dashboard").classes('text-2xl font-bold mb-4')

    with ui.tabs().classes('w-full') as tabs:
        tickets_tab = ui.tab('Tickets')
        workers_tab = ui.tab('Workers')
        users_tab = ui.tab('Users')

    with ui.tab_panels(tabs, value=tickets_tab).classes('w-full'):
        with ui.tab_panel(tickets_tab):
            show_tickets_admin(cur)

        with ui.tab_panel(workers_tab):
            show_workers_admin(cur)

        with ui.tab_panel(users_tab):
            show_users_admin(cur)
def show_tickets_admin(cur):
    def update_priority(e):
        tid = e.args[0]
        new_priority = e.args[1]
        cur.execute("UPDATE tickets SET priority = %s WHERE tid = %s", (new_priority, tid))
        cur.connection.commit()
        ui.notify(f"Priority for ticket {tid} updated to {new_priority}", type='positive')
        ui.run_javascript("location.reload()")

    cur.execute("""
        SELECT t.tid, t.subject, t.location, t.description, t.priority, 
               ts.status, 
               u.first_name || ' ' || u.last_name as reporter_name
        FROM tickets t
        JOIN ticketStatus ts ON t.tid = ts.tid
        JOIN reports r ON t.tid = r.tid
        JOIN users u ON r.reporterID = u.userID
        ORDER BY t.priority DESC
    """)
    tickets = cur.fetchall()

    ui.label("All Tickets").classes('text-xl font-bold mt-4')

    columns = [
        {'name': 'tid', 'label': 'ID', 'field': 'tid', 'sortable': True},
        {'name': 'subject', 'label': 'Subject', 'field': 'subject', 'sortable': True},
        {'name': 'location', 'label': 'Location', 'field': 'location', 'sortable': True},
        {'name': 'status', 'label': 'Status', 'field': 'status', 'sortable': True},
        {'name': 'reporter', 'label': 'Reporter', 'field': 'reporter_name', 'sortable': True},
        {'name': 'priority', 'label': 'Priority', 'field': 'priority', 'sortable': False},
    ]

    with ui.table(columns=columns, rows=tickets, row_key='tid').classes('w-full') as table:
        table.add_slot('body-cell-priority', '''
            <q-td :props="props">
                <q-select
                    :options="[1,2,3,4,5]"
                    v-model="props.row.priority"
                    dense
                    outlined
                    emit-value
                    map-options
                    @update:model-value="value => $parent.$emit('update-priority', props.row.tid, value)"
                    style="width: 80px;"
                />
            </q-td>
        ''')
        table.on('update-priority', update_priority)


def show_workers_admin(cur):
    cur.execute("""
        SELECT w.workerID, u.first_name, u.last_name, w.department, w.specialty, u.email, u.role
        FROM isWorker w
        JOIN users u ON w.workerID = u.userID
        ORDER BY w.department, w.specialty
    """)
    workers = cur.fetchall()

    for w in workers:
        w['name'] = f"{w['first_name']} {w['last_name']}"

    ui.label("Workers Management").classes('text-xl font-bold mt-4')

    columns = [
        {'name': 'workerID', 'label': 'ID', 'field': 'workerid', 'sortable': True},
        {'name': 'name', 'label': 'Name', 'field': 'name', 'sortable': True},
        {'name': 'department', 'label': 'Department', 'field': 'department', 'sortable': True},
        {'name': 'specialty', 'label': 'Specialty', 'field': 'specialty', 'sortable': True},
        {'name': 'email', 'label': 'Email', 'field': 'email', 'sortable': True},
        {'name': 'role', 'label': 'Role', 'field': 'role', 'sortable': True},
    ]

    ui.table(columns=columns, rows=workers, row_key='workerid').classes('w-full')


def show_users_admin(cur):
    cur.execute("""
        SELECT userID, email, first_name, last_name, role
        FROM users
        ORDER BY role, last_name, first_name
    """)
    users = cur.fetchall()

    for u in users:
        u['name'] = f"{u['first_name']} {u['last_name']}"

    ui.label("User Management").classes('text-xl font-bold mt-4')

    columns = [
        {'name': 'userID', 'label': 'ID', 'field': 'userid', 'sortable': True},
        {'name': 'name', 'label': 'Name', 'field': 'name', 'sortable': True},
        {'name': 'email', 'label': 'Email', 'field': 'email', 'sortable': True},
        {'name': 'role', 'label': 'Role', 'field': 'role', 'sortable': True},
    ]

    ui.table(columns=columns, rows=users, row_key='userid').classes('w-full')
