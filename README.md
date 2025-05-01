# CampusFix: Rhodes College Issue Report System

## Project Overview
CampusFix is a comprehensive issue tracking system designed for Rhodes College. The platform allows users to report various campus issues, from Wi-Fi problems to maintenance requests. Administrators can manage tickets and assign workers, while workers can view and update tickets assigned to them.


## Features and Functionality

### User Management
- **Login System**: Secure authentication for students, faculty, staff, and external workers
- **Role-Based Access**: Different interfaces for regular users, workers, and administrators

### For All Users
- **Create Tickets**: Report issues with subject, location, description, and priority
- **Track Ticket Status**: View status updates on submitted tickets
- **User-Friendly Navigation**: Intuitive interface to prevent users from getting "stuck"

### For Administrators
- **Admin Dashboard**: Comprehensive view of all tickets in the system
- **Ticket Management**: Update ticket priority and status
- **Worker Management**: View and manage worker information
- **User Management**: Access to all user information

### For Workers
- **Worker Dashboard**: View tickets assigned specifically to them
- **Prioritized View**: See tickets ordered by admin-assigned priority

## Database Operations

### SELECT Operations
- View user tickets (in `checkTicketStatus.py`)
- Display all tickets for administrators (in `adminDashboard.py`)
- View workers assigned to tickets (in `workerDashboard.py`)
- View all users in the system (in `adminDashboard.py`)

### INSERT Operations
- Create new tickets with user-defined parameters (in `createTicket.py`)
- Insert reporter information when creating tickets (in `createTicket.py`)

### UPDATE Operations
- Update ticket status (Open/In Progress/Closed) by administrators (in `adminDashboard.py`)
- Update ticket priority by administrators (in `adminDashboard.py`)

### DELETE Operations
- We purposly decided that delete operations are not necessary for our system. Instead, we maintain a history of all tickets and their statuses. This allows us to keep track of all issues reported, even if they are resolved or closed. This decision was made to ensure transparency and accountability in the ticketing process.

## Database Schema
Our system utilizes 7 interconnected tables:
- **users**: Stores user information (200 records)
- **isAdmin**: Records which users have admin privileges (2 records)
- **isWorker**: Identifies users who are workers and their specialties (13 records)
- **tickets**: Contains ticket information and details (20 records)
- **ticketStatus**: Tracks the current status of each ticket (20 records)
- **reports**: Links reporters to their tickets (20 records)
- **assigns**: Maps tickets to assigned workers (20 records)

## Technical Implementation
- **Backend**: Python with NiceGUI framework
- **Database**: PostgreSQL
- **Authentication**: Session-based with role checking

## Running the Application
1. Ensure PostgreSQL is installed
2. Set up the database using the SQL scripts in `db/`
3. Update `dbinfo.py` with your database credentials
4. Install dependencies: `pip install psycopg nicegui`
5. Run the application: `python login.py`

## Project Requirements Compliance

| Requirement | Implementation |
|-------------|----------------|
| SQL SELECT | Multiple views for tickets, users, and workers |
| SQL INSERT | Ticket creation functionality |
| SQL UPDATE | Status and priority modification |
| SQL DELETE | Not implemented, but justified by maintaining records |
| Table Size Requirements | All tables meet or exceed required record counts |
| Intuitive Navigation | Home button on all pages, clear navigation structure |
| All Tables Used | Every table in the schema is utilized in the application |

## Team Members
- Echo O'Connor
- Jack Seigerman
- Allen Osoinach
