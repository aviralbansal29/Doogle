from dotenv import load_dotenv

load_dotenv()


if __name__ == "__main__":
    import discord
    import os

    from bot import chat_processors as chat

    client = discord.Client()

    @client.event
    async def on_ready():
        print('We have logged in as {0.user}'.format(client))


    @client.event
    async def on_message(message):
        # If message author is bot, do not process message
        if message.author == client.user:
            return

        response = chat.process_chat(message)
        if response:
            await message.channel.send(response)

    client.run(os.getenv('TOKEN'))
