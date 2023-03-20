# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any
# later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program. If not,
# see <https://www.gnu.org/licenses/>.

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

        if not message.content or len(message.content) == 0:
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

        system_role = """
You are a senior blockchain developer to create solidity smart contract given a specification.

- Describe general use case
- Describe interface and acceptance criteria
- Output a ethereum smart contract written in solidity
        """

        # Applies to gpt-3 & gpt-4
        response = openai.ChatCompletion.create(
            model="gpt-4",  # can be gpt-3.5-turbo, gpt-4
            messages=[
                {"role": "system", "content": system_role},
                {"role": "user", "content": message.content}
            ]
        )

        assistant_response = response.choices[0]['message']['content']
        await message.channel.send(assistant_response)


client = ChatBot(intents=discord.Intents.default(), heartbeat_timeout=600)
client.run(DISCORD_TOKEN)
