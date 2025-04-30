import psycopg
from psycopg.rows import dict_row
from dbinfo import *
from nicegui import ui, app
from adminDashboard import admin
from workerDashboard import worker

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

# WORKER CHECK
def is_worker(user_id):
    cur.execute("SELECT workerID FROM isworker WHERE workerID=%s", [user_id])
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
            # IF ADMIN
            if is_user_admin:
                ui.label("You have administrator privileges").classes('text-green-600')

            with ui.row().classes('gap-2 mt-4'):
                ui.button('Logout', on_click=lambda: ui.navigate.to('/logout')).classes('bg-red-500 text-white')
                # IF ADMIN
                if is_user_admin:
                    ui.button('Admin Dashboard', on_click=lambda: ui.navigate.to('/admin')).classes(
                        'bg-blue-500 text-white')

                ui.button('Create Ticket', on_click=lambda: ui.navigate.to('/report')).classes(
                    'bg-green-500 text-white')
                ui.button('Check Ticket Status', on_click=lambda: ui.navigate.to('/status')).classes(
                    'bg-yellow-500 text-white')
                # IF WORKER
                if user_id in [w['workerid'] for w in get_workers()]:
                    ui.button('Worker Dashboard', on_click=lambda: ui.navigate.to('/worker')).classes(
                        'bg-purple-500 text-white')
    else:
        with ui.card().classes('w-full'):
            ui.label("You are not logged in").classes('mb-2')
            ui.button('Login', on_click=lambda: ui.navigate.to('/login')).classes('bg-blue-500 text-white')

#check if worker
def get_workers():
    cur.execute("SELECT workerid FROM isworker")
    rows = cur.fetchall()
    return rows




#login page
@ui.page('/login')
def login(redirect_url='/'):
    def try_login():
        user_data = get_password_for_user(username_box.value)
        if user_data and user_data['password'] == password_box.value:
            # STORE DATA
            app.storage.user['username'] = username_box.value
            app.storage.user['user_id'] = user_data['userid']

            #IF ADMIN (store info in session)
            admin_status = is_admin(user_data['userid'])
            app.storage.user['is_admin'] = admin_status

            #IF WORKER (store info in session)
            worker_status = is_worker(user_data['userid'])
            app.storage.user['is_worker'] = worker_status

            # LOGIN SUCCESS
            if admin_status:
                ui.notify('Logged in successfully as Administrator', color='positive')
            else:
                ui.notify('Logged in successfully', color='positive')

            #HOMEPAGE
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

#CREATE TICKET PAGE
@ui.page('/createticket')
def createTicket():
    createTicket(cur)

#CHECK TICKET STATUS PAGE
@ui.page('/checkticketstatus')
def checkTicketStatus():
    checkTicketStatus(cur)

#ADMIN DASHBOARD PAGE
@ui.page('/admin')
def admin_page():
    admin(cur)

#WORKER DASHBOARD PAGE
@ui.page('/worker')
def worker_page():
    worker(cur)


@ui.page('/logout')
def logout():
    # Clear all user data from session
    app.storage.user.clear()

    with ui.card().classes('w-96 mx-auto mt-8'):
        ui.label("You have been logged out successfully").classes('text-lg mb-4')
        ui.button('Back to homepage', on_click=lambda: ui.navigate.to('/')).classes('bg-blue-500 text-white')



# Run the app
ui.run(reload=False, storage_secret='secret')