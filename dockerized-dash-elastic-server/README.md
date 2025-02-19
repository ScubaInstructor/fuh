### Server Component 

Set the values in `.env` to your liking. Important is to change at least `YOUR_SECRET_KEY` to something random.

The preset superuser is `admin` with password `admin`. Login in with this useraccount, create a new superuser and delete admin. The database containing userinformation is `instance/users.db` inside the folder where this file. 

Start server with `docker-compose up` and browse to the url you specified. The startup can take a while, as elastic needs to be fully available before the webinterface is started.