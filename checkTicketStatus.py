#TODO
#user or admin can delete ticket and check status
from nicegui import ui, app

def status(cur):

    username = app.storage.user.get('username', None)
    is_user_admin = app.storage.user.get('is_admin', False)

    #takes them back to home screen
    if username is None:
        return ui.navigate.to('/login?redirect_url=/admin')

    ui.label("My Tickets").classes('text-2xl font-bold mb-4')

    def show_user_tickets(cur):
        cur.execute("""
            SELECT t.tid, t.subject, t.reporterid
            FROM tickets t
            JOIN reports r
            WHERE t.tid = r.tid
            and t.reporterid=%s"
        """, [username])
        tickets = cur.fetchall()

        ui.label("All Tickets").classes('text-xl font-bold mt-4')

        columns = [
            {'name': 'tid', 'label': 'ID', 'field': 'tid', 'sortable': True},
            {'name': 'subject', 'label': 'Subject', 'field': 'subject', 'sortable': True},
            {'name': 'reporterid', 'label': 'Reporter ID', 'field': 'reporterid', 'sortable': True},
        ]

        with ui.table(columns=columns, rows=tickets, row_key='tid').classes('w-full') as table:
            table.add_slot('body-cell-status', '''
                    <q-td :props="props">
                        <q-chip :color="props.value === 'open' ? 'green' : 'gray'">
                            {{ props.value }}
                        </q-chip>
                    </q-td>
                ''')

