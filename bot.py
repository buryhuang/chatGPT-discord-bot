import discord
import openai
import os

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


class ChatBot(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        # print('Message from {0.author}: {0.content}'.format(message))
        if message.author == self.user:
            return

        input_content = [message.content]

        if message.attachments:
            for attachment in message.attachments:
                image_bytes = await attachment.read()
                input_content.append({"image": image_bytes})

        print([{"role": "user", "content": input_content}])

        # May need to wait for updated from gpt-4
        # response = openai.ChatCompletion.create(
        #     model="gpt-4",
        #     messages=[{"role": "user", "content": input_content}]
        # )

        # Applies to gpt-3 & gpt-4
        response = openai.ChatCompletion.create(
            model="gpt-4",  # can be gpt-3.5-turbo
            messages=[{"role": "user", "content": message.content}]
        )

        assistant_response = response.choices[0]['message']['content']
        await message.channel.send(assistant_response)


client = ChatBot(intents=discord.Intents.default())
client.run(DISCORD_TOKEN)
