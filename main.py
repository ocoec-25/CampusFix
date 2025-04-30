import psycopg
from psycopg.rows import dict_row
from dbinfo import *
from nicegui import ui, app

# Connect to db and open curser
conn = psycopg.connect(f"host=dbclass.rhodescs.org dbname=practice user={DBUSER} password={DBPASS}")
cur = conn.cursor(row_factory=dict_row)


# PASSWORD CHECK
def get_password_for_user(username):
    cur.execute("SELECT password, userID from users where email=%s", [username])
    result = cur.fetchone()
    if result is not None:
        return result
    else:
        return None


# ADMIN CHECK
def is_admin(user_id):
    cur.execute("SELECT adminID FROM isAdmin WHERE adminID=%s", [user_id])
    result = cur.fetchone()
    return result is not None


@ui.page('/')
def homepage():
    ui.label("CampusFix: Rhodes Issue Report System").classes('text-2xl font-bold mb-4')

    # IF LOGGED IN
    username = app.storage.user.get('username', None)
    if username is not None:
        user_id = app.storage.user.get('user_id', None)
        is_user_admin = app.storage.user.get('is_admin', False)

        with ui.card().classes('w-full'):
            ui.label(f"You are logged in as: {username}").classes('font-bold')
            if is_user_admin:
                ui.label("You have administrator privileges").classes('text-green-600')

            with ui.row().classes('gap-2 mt-4'):
                ui.button('Logout', on_click=lambda: ui.navigate.to('/logout')).classes('bg-red-500 text-white')

                if is_user_admin:
                    ui.button('Admin Dashboard', on_click=lambda: ui.navigate.to('/admin')).classes(
                        'bg-blue-500 text-white')

                ui.button('Create Ticket', on_click=lambda: ui.navigate.to('/report')).classes(
                    'bg-green-500 text-white')
                ui.button('Check Ticket Status', on_click=lambda: ui.navigate.to('/status')).classes(
                    'bg-yellow-500 text-white')

                if user_id in [w['workerid'] for w in get_workers()]:
                    ui.button('Worker Dashboard', on_click=lambda: ui.navigate.to('/worker')).classes(
                        'bg-purple-500 text-white')
    else:
        with ui.card().classes('w-full'):
            ui.label("You are not logged in").classes('mb-2')
            ui.button('Login', on_click=lambda: ui.navigate.to('/login')).classes('bg-blue-500 text-white')


def get_workers():
    cur.execute("SELECT workerid FROM isworker")
    rows = cur.fetchall()
    return rows


@ui.page('/login')
def login(redirect_url='/'):
    def try_login():
        user_data = get_password_for_user(username_box.value)
        if user_data and user_data['password'] == password_box.value:
            # Store user info in session
            app.storage.user['username'] = username_box.value
            app.storage.user['user_id'] = user_data['userid']

            # Check if user is admin and store in session
            admin_status = is_admin(user_data['userid'])
            app.storage.user['is_admin'] = admin_status

            # Notify user of successful login
            if admin_status:
                ui.notify('Logged in successfully as Administrator', color='positive')
            else:
                ui.notify('Logged in successfully', color='positive')

            # Redirect to intended page or homepage
            ui.navigate.to(redirect_url)
        else:
            ui.notify('Wrong username or password', color='negative')

    with ui.card().classes('w-96 mx-auto mt-8'):
        ui.label("Login to CampusFix").classes('text-xl font-bold mb-4')
        with ui.column().classes('w-full gap-4'):
            username_box = ui.input('Email Address:').classes('w-full')
            password_box = ui.input('Password:', password=True, password_toggle_button=True).classes('w-full')

            with ui.row().classes('w-full justify-between'):
                ui.button('Back to Home', on_click=lambda: ui.navigate.to('/')).classes('bg-gray-500 text-white')
                ui.button('Log in', on_click=try_login).classes('bg-blue-500 text-white')


@ui.page('/logout')
def logout():
    # Clear all user data from session
    app.storage.user.clear()

    with ui.card().classes('w-96 mx-auto mt-8'):
        ui.label("You have been logged out successfully").classes('text-lg mb-4')
        ui.button('Back to homepage', on_click=lambda: ui.navigate.to('/')).classes('bg-blue-500 text-white')


@ui.page('/admin')
def admin():
    # Check if user is logged in and is admin
    username = app.storage.user.get('username', None)
    is_user_admin = app.storage.user.get('is_admin', False)

    if username is None:
        return ui.navigate.to('/login?redirect_url=/admin')

    if not is_user_admin:
        with ui.card().classes('w-96 mx-auto mt-8 bg-red-100'):
            ui.label("Access Denied: Administrator privileges required").classes('text-red-600 font-bold')
            ui.button('Back to Home', on_click=lambda: ui.navigate.to('/')).classes('bg-blue-500 text-white mt-4')
        return

    # Admin dashboard content
    ui.label("Administrator Dashboard").classes('text-2xl font-bold mb-4')

    # Add your admin functionality here
    with ui.tabs().classes('w-full') as tabs:
        tickets_tab = ui.tab('Tickets')
        workers_tab = ui.tab('Workers')
        users_tab = ui.tab('Users')

    with ui.tab_panels(tabs, value=tickets_tab).classes('w-full'):
        with ui.tab_panel(tickets_tab):
            show_tickets_admin()

        with ui.tab_panel(workers_tab):
            show_workers_admin()

        with ui.tab_panel(users_tab):
            show_users_admin()


def show_tickets_admin():
    # Get all tickets
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

    # Display tickets in a sortable table
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

    # Add table with action buttons
    with ui.table(columns=columns, rows=tickets, row_key='tid').classes('w-full') as table:
        # Add row buttons for edit/update
        table.add_slot('body-cell-status', '''
            <q-td :props="props">
                <q-chip :color="props.value === 'open' ? 'green' : 'gray'">
                    {{ props.value }}
                </q-chip>
            </q-td>
        ''')


def show_workers_admin():
    # Get all workers with their departments and specialties
    cur.execute("""
        SELECT w.workerID, u.first_name, u.last_name, w.department, w.specialty, u.email, u.role
        FROM isWorker w
        JOIN users u ON w.workerID = u.userID
        ORDER BY w.department, w.specialty
    """)
    workers = cur.fetchall()

    ui.label("Workers Management").classes('text-xl font-bold mt-4')

    columns = [
        {'name': 'workerID', 'label': 'ID', 'field': 'workerid', 'sortable': True},
        {'name': 'name', 'label': 'Name', 'field': 'first_name',
         'format': lambda v, r: f"{r['first_name']} {r['last_name']}", 'sortable': True},
        {'name': 'department', 'label': 'Department', 'field': 'department', 'sortable': True},
        {'name': 'specialty', 'label': 'Specialty', 'field': 'specialty', 'sortable': True},
        {'name': 'email', 'label': 'Email', 'field': 'email', 'sortable': True},
        {'name': 'role', 'label': 'Role', 'field': 'role', 'sortable': True},
    ]

    ui.table(columns=columns, rows=workers, row_key='workerid').classes('w-full')


def show_users_admin():
    # Get all users
    cur.execute("""
        SELECT userID, email, first_name, last_name, role
        FROM users
        ORDER BY role, last_name, first_name
    """)
    users = cur.fetchall()

    ui.label("User Management").classes('text-xl font-bold mt-4')

    columns = [
        {'name': 'userID', 'label': 'ID', 'field': 'userid', 'sortable': True},
        {'name': 'name', 'label': 'Name', 'field': 'first_name',
         'format': lambda v, r: f"{r['first_name']} {r['last_name']}", 'sortable': True},
        {'name': 'email', 'label': 'Email', 'field': 'email', 'sortable': True},
        {'name': 'role', 'label': 'Role', 'field': 'role', 'sortable': True},
    ]

    ui.table(columns=columns, rows=users, row_key='userid').classes('w-full')


# Run the app
ui.run(reload=False, storage_secret='THIS_NEEDS_TO_BE_CHANGED')