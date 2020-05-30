from dotenv import load_dotenv
import os
from socket_client import createClient
from zephyr_connection import createStream

if __name__ == "__main__":
    load_dotenv()
    socket = createClient()
    stream = createStream(socket)
    stream.run_stream()