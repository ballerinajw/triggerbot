# vibecoded project, i take no credit for it

import asyncio
import discord
from detection import score_message, get_threshold
from logger import log_block

class DMFilter:
    def __init__(self, token: str, level: int, on_ready_cb=None, on_block_cb=None, on_error_cb=None):
        self.token = token
        self.level = level
        self.threshold = get_threshold(level)
        self.on_ready_cb = on_ready_cb
        self.on_block_cb = on_block_cb
        self.on_error_cb = on_error_cb
        self.client = None
        self.loop = None

    def start(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.client = discord.Client()

        @self.client.event
        async def on_ready():
            if self.on_ready_cb:
                self.on_ready_cb(str(self.client.user))

        @self.client.event
        async def on_message(message):
            if message.guild is not None or message.author == self.client.user:
                return
            score, hits = score_message(message.content, self.level)
            if score >= self.threshold:
                log_block(message.author, message.author.id,
                          self.level, score, hits, message.content)
                await message.author.block()
                if self.on_block_cb:
                    self.on_block_cb()

        try:
            self.loop.run_until_complete(self.client.start(self.token))
        except Exception as e:
            if self.on_error_cb:
                self.on_error_cb(str(e))

    def stop(self):
        if self.loop and self.client:
            asyncio.run_coroutine_threadsafe(self.client.close(), self.loop)
