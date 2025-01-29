### Server Component 

Set the values in `.env` to your liking. Important is to change at least `YOUR_SECRET_KEY` to something random.

Run `python  user_creator.py {username} {password}` in this folder to create a user and add it to the userdatabase. After that there should be a database `instance/users.db` inside the folder where this script and the server is located. 

Start server with `docker-compose up` and browse to the url you specified. The startup can take a while, as elastic needs to be fully available before the webinterface is started.