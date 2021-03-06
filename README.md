**Overview:**
This program creates a virtual mood tracker. The idea comes from Bullet Journaling (the popular style of day planner). People commonly put a page in their planner where they write down their mood every day, so they can look back and reflect on their feelings for the week/month/year. This program does just that, in virtual format!

**Instructions:**
The database I included contains two users:
Username |Password
----------|---------
admin	|pass
user	|password

The admin user has the extra functionality of being able to add/remove users and view a list of all users in the database.

I also included some entries in the admin file, but the user file does not exist yet, so you can see how the program creates a new file for new users.

**To run the program:**
1.	Run the server program using python myserver.py
1.	Run the client program using python myclient.py
This sets up the socket and encryption.
1.	Begin entering commands (start with ‘help’ for a list of possible commands)
Note that the list of commands given with ‘help’ changes when a user logs in.
Typical client usage of the program would go something like:
1.	login (client enters username and password)
1.  newentry (client enters current mood) 
1.  showdata (client reviews their past entries)
1.	logout
1.	q
Any functions that require arguments will prompt the user to enter additional information.
Additional functions such as adduser and changepass are documented below in the Command Parsing section.

**Command Parsing**
The parser recognizes the following commands:
*	login
*	logout
*	help (gives a list of commands and a brief description)
*	adduser (restricted to admin only)
*	delete (restricted to admin only)
*	listall (restricted to admin only)
*	changepass
*	newentry (creates a new entry into the user’s virtual diary)
*	showdata (displays all of the user’s previous entries)
*	q (quit)

Any other input is recognized as invalid.
On the server side, all functions return a string which is then sent (encrypted) to the client and printed to the screen. This way the client gets feedback from the server after every command they use. 

