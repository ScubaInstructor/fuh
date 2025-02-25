### Server Component 

Set the values in `.env` to your liking. Important is to change at least `YOUR_SECRET_KEY` to something random.

The preset superuser is `admin` with password `admin`. Login in with this useraccount, create a new superuser and delete admin. The database containing userinformation is `instance/database.db` inside the folder where this file. 

To enable notification via Discord, create a discord-bot and apply the generated token to `.env`. Set the credentials of the channel you want to notify in `.env`, and add the bot to the channel. Please refer to the [discord developers website](https://discord.com/developers/applications) for detailed instructions!

Start server with `docker-compose up` and browse to the url you specified. The startup can take a while, as elastic needs to be fully available before the webinterface is started.