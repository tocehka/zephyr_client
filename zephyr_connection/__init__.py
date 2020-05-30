from .stream import ZephyrStream

def createStream(socket_client):
    return ZephyrStream(socket_client)