from nicegui import ui, app


def ticket(cur):
    username = app.storage.user.get("username", None)
    if username is None:
        return ui.navigate.to('/login?redirect_url=/admin')

    def get_new_tid(cur):
        cur.execute("SELECT MAX(tid) FROM tickets")
        result = cur.fetchone()
        print("Result from DB:", result)
        if result and result['max'] is not None:
            new_tid = result['max'] + 1
        else:
            new_tid = 1
        print(f"New TID: {new_tid}")
        return new_tid

    def insert_reports(cur, new_tid):

        user_id = app.storage.user.get("user_id", None)

        cur.execute("INSERT INTO reports (reporterid, tid) VALUES (%s, %s)", (user_id, new_tid))
        cur.connection.commit()


    def insert_ticket(cur, subject, location, description, priority):
        new_tid = get_new_tid(cur)
        cur.execute(
            "INSERT INTO tickets (tid, subject, location, description, priority) VALUES (%s, %s, %s, %s, %s)",
            (new_tid, subject, location, description, priority)
        )
        # Also add an entry to ticketStatus with default values
        cur.execute(
            "INSERT INTO ticketStatus (tid, status, adminPriority) VALUES (%s, %s, %s)",
            (new_tid, "open", priority)  # Setting initial status as "open" and adminPriority same as user priority
        )
        cur.connection.commit()

        return new_tid

    def submit_ticket():
        subject = subject_input.value
        location = location_input.value
        description = description_input.value
        priority = int(priority_input.value)



        # Insert the ticket data
        new_tid = insert_ticket(cur, subject, location, description, priority)
        # Insert the report data
        insert_reports(cur, new_tid)

        # Show success message
        step1_card.set_visibility(False)
        step2_card.set_visibility(True)

        success_message.text = f"Ticket #{new_tid} created successfully!"


    def reset_form():
        subject_input.value = ''
        location_input.value = ''
        description_input.value = ''
        priority_input.value = '1'
        step1_card.set_visibility(True)
        step2_card.set_visibility(False)
        error_card.set_visibility(False)

    with ui.card() as step1_card:
        ui.label("Create New Ticket").classes("text-xl font-bold")
        with ui.row():
            subject_input = ui.input(label="Subject", placeholder="Enter ticket subject").classes("w-64")
            location_input = ui.input(label="Location", placeholder="Enter location").classes("w-64")
        with ui.row():
            description_input = ui.input(label="Description", placeholder="Enter detailed description").classes(
                "w-full")
        with ui.row():
            priority_input = ui.select(['1', '2', '3', '4', '5'], value="1",
                                       label="Priority (1-5, 5 is highest)").classes("w-64")
        with ui.row():
            ui.button("Submit Ticket", on_click=submit_ticket).classes("bg-blue-500 text-white")
            ui.button('Back to Home', on_click=lambda: ui.navigate.to('/')).classes('bg-green-500 text-white')

    with ui.card() as step2_card:
        step2_card.set_visibility(False)
        success_message = ui.label("Ticket created successfully!")
        ui.button("Create Another Ticket", on_click=reset_form).classes("bg-green-500 text-white")
        ui.button('Back to Home', on_click=lambda: ui.navigate.to('/')).classes('bg-green-500 text-white')

    with ui.card() as error_card:
        error_card.set_visibility(False)
        error_message = ui.label("Something went wrong. Please make sure all fields are filled in.")
        ui.button("Try Again", on_click=reset_form).classes("bg-red-500 text-white")