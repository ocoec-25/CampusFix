
--DROP TABLE IF EXISTS users;
--DROP TABLE IF EXISTS isAdmin;
--DROP TABLE IF EXISTS isWorker;
--DROP TABLE IF EXISTS tickets;
--DROP TABLE IF EXISTS ticketStatus;
--DROP TABLE IF EXISTS reports;
--DROP TABLE IF EXISTS assigns;

CREATE TABLE users (
    userID INT PRIMARY KEY NOT NULL, --R# for students, faculty, staff? or we can use other unique identifier
	email VARCHAR(50) NOT NULL, --we can use email address as username
	password VARCHAR(50) NOT NULL,
	role VARCHAR(50) NOT NULL, --this tells us if the person is a student, faculty, staff, or worker from outside of rhodes (like terminex)
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL
);

CREATE TABLE isAdmin (
	adminID INT PRIMARY KEY NOT NULL --list of user IDs that have admin privelages?
);

CREATE TABLE isWorker (
	workerID INT PRIMARY KEY NOT NULL REFERENCES users(userID),
	department VARCHAR(50) NOT NULL,
	specialty VARCHAR(50) NOT NULL --specialties will match subjects of tickets
);

CREATE TABLE tickets (
	tid INT PRIMARY KEY NOT NULL,
	subject VARCHAR(50),
	location VARCHAR(50),
	description VARCHAR(50),
	priority INT NOT NULL --scale 1 to 5 
);

CREATE TABLE ticketStatus (
	tid INT PRIMARY KEY NOT NULL REFERENCES tickets(tid),
	status VARCHAR(50), --open/closed
	adminPriority INT NOT NULL --admin can set their own priorities for these tickets
);

CREATE TABLE reports (
	reporterID INT NOT NULL REFERENCES users(userID),
	tid INT NOT NULL REFERENCES tickets(tid),
	PRIMARY KEY (reporterID, tid)
);

CREATE TABLE assigns (
	tid INT NOT NULL REFERENCES tickets(tid),
	workerID INT NOT NULL REFERENCES isWorker(workerID),
	PRIMARY KEY (tid, workerID)
);

