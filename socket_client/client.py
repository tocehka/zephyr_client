import socketio
import os
import time


class ClientSocket:
    def __init__(self):
        self.sio = socketio.Client()
        self.sio = self.__event_wrapper(self.sio)

    def __event_wrapper(self, sio):
        @sio.event
        def connect():
            print('Zephyr connected to server')

        # @sio.on("new meas", namespace="/rec")
        # def new_meas(data):
        #     print('message received with ', data)
        #     #sio.emit('my response', {'response': 'my response'})

        @sio.event
        def disconnect():
            print('Zephyr disconnected from server')
        return sio
    
    def connect(self):
        while True:
            try:
                self.sio.connect(os.environ.get("SERVER") + "?key=" + os.environ.get("CONNECTION_KEY") + "&name=" + os.environ.get("ZEPHYR"),
                            namespaces=["/zephyr"])
                break
            except Exception as e:
                print("Error with socket connection: ", e)
                print("Reconnection after 5 seconds...")
                time.sleep(5)
                continue

    def send_data(self, data):
        try:
            self.sio.emit("data reciever", data, namespace="/zephyr")
            print("Data from Zephyr was sucessfully sent")
        except Exception as e:
                print("Error with sending data to server: ", e)
                print("Error was occured at ", time.strftime("%H:%M:%S"))
