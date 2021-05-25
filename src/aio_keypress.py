import asyncio
import contextlib
import sys
import termios


@contextlib.contextmanager
def raw_mode(file):
    old_attrs = termios.tcgetattr(file.fileno())
    new_attrs = old_attrs[:]
    new_attrs[3] = new_attrs[3] & ~(termios.ECHO | termios.ICANON)
    try:
        termios.tcsetattr(file.fileno(), termios.TCSADRAIN, new_attrs)
        yield
    finally:
        termios.tcsetattr(file.fileno(), termios.TCSADRAIN, old_attrs)


class AIOKeyPress:

    def __init__(self, task_func=None):
        self.task_func = task_func
        self.closed = False

    def close(self):
        self.closed = True

    async def listen(self):
        with raw_mode(sys.stdin):
            reader = asyncio.StreamReader()
            loop = asyncio.get_event_loop()
            await loop.connect_read_pipe(lambda: asyncio.StreamReaderProtocol(reader), sys.stdin)

            while (not reader.at_eof()) or (not self.closed):
                ch = await reader.read(1)
                # '' means EOF, chr(4) means EOT (sent by CTRL+D on UNIX terminals)
                if self.task_func:
                    self.task_func(ord(ch))
                if not ch or ord(ch) <= 4:
                    break
        print('AIOKeyPress closed')