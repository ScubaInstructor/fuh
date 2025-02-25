# This example requires the 'members' privileged intents
# Set Channel ID accordingly
# Set token
# Remove DEBUG

import discord

DEBUG = 1


class DiscordClient(discord.Client):

    def __init__(self, channel_id: str, *args, **kwargs):
        intents = discord.Intents.default()
        intents.members = True
        super().__init__(intents=intents, *args, **kwargs)
        self.channel: discord.channel
        self.channel_id = channel_id
        self.message_id = (
            0  # ID of the message that can be reacted to. Will be set in on_message()
        )
        self.reaction_emoji = {
            discord.PartialEmoji(
                name="👍"
            ): 2,  # ID of the role associated with unicode emoji '👍'.
        }

    async def on_ready(self):
        self.channel = self.get_channel(self.channel_id)
        m = await self.channel.send("Zum Annehmen des Tickets bitte mit 👍 reagieren!")
        self.message_id = m.id

    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        # Make sure that the message the user is reacting to is the one we care about.
        if payload.message_id != self.message_id:
            return

        guild = self.get_guild(payload.guild_id)
        if guild is None:
            # Check if we're still in the guild and it's cached.
            return

        if payload.emoji in self.reaction_emoji:
            if DEBUG:
                print("accepted")
            message = await self.channel.fetch_message(payload.message_id)
            print(message)
            await message.edit(
                content=f"Task is being worked on by {payload.member.global_name}"
            )
        else:
            # If the emoji isn't the one we care about then exit as well.
            if DEBUG:
                print("wrong Emoji")
            return

    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        """React on removal of a reaction emoji."""
        # Make sure that the message the user is reacting to is the one we care about.
        if payload.message_id != self.message_id:
            return

        guild = self.get_guild(payload.guild_id)
        if guild is None:
            # Check if we're still in the guild and it's cached.
            return

        if payload.emoji in self.reaction_emoji:
            if DEBUG:
                print("removed")
            pass
        else:
            # If the emoji isn't the one we care about then exit as well.
            return

    async def on_message(self, message: discord.Message):
        if message.author.id == self.user.id:
            self.message_id = message.id


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv

    load_dotenv()
    TOKEN = os.getenv("DISCORD_TOKEN")
    CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))
    client = DiscordClient(channel_id=CHANNEL_ID)
    client.run(token=TOKEN)
