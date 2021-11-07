## Virtual Mood Tracker
### Overview:
Log your mood everyday (or every minute) and keep the data encrypted so no one ever knows how you feel!

The idea of a mood tracker comes from Bullet Journaling (a popular style of day planner). A mood tracker is a planner page where you write down your mood every day, so you can look back and reflect on your feelings for the week/month/year. This program does just that, in virtual format!

### Instructions
The included database has two users:
Username |Password
----------|---------
admin	|pass
user	|password

Use the admin login to add/remove users, view a list of all users in the database, or view the sample diary.


### To run the program:
1.	Run the server program using python myserver.py
1.	Run the client program using python myclient.py
This sets up the socket and encryption.
1.	Begin entering commands (start with ‘help’ for a list of possible commands) Note that the list of commands given with ‘help’ changes when a user logs in.


Typical client usage of the program would go something like:
1.	login (client enters username and password)
1.  newentry (client enters current mood) 
1.  showdata (client reviews their past entries)
1.	logout
1.	q (quit)

*When additional information is required, the server will prompt the client.*

### Commands
The parser recognizes the following commands:
*	login
*	logout
*	help (gives a list of commands and a brief description)
*	adduser (adds a new user to the database - restricted to admin only)
*	delete (deletes a user from the database - restricted to admin only)
*	listall (lists all users in the database - restricted to admin only)
*	changepass (allows a user to change their password)
*	newentry (creates a new entry into the user’s virtual diary)
*	showdata (displays all of the user’s previous entries)
*	q (quit)

Any other input is recognized as invalid.

On the server side, all functions return a string which is then sent (encrypted) to the client and printed to the screen. This way the client gets feedback from the server after every command they use. 

