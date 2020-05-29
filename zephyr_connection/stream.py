import pygatt
from time import strftime
from numpy import mean
from config import conf


class ZephyrStream:
    def __init__(self, socket_client):
        self.adapter = pygatt.GATTToolBackend()
        self.socket_client = socket_client
        print("Experiment was started at {}".format(strftime("%H:%M:%S")))

    def __handle_data(self, handle, value):
        try:
            if value == None:
                raise ValueError
            flags = value.pop(0)
            hr_format = (flags >> 0) & 1
            contact_status = (flags >> 1) & 3
            expended_present = (flags >> 3) & 1
            rr_present = (flags >> 4) & 1
            meas = {"hr": value.pop(0)}
            if hr_format:
                meas["hr"] += 256 * value.pop(0)
            if contact_status & 2:
                meas["sensor_contact"] = bool(contact_status & 1)
            if expended_present:
                e = value.pop(0)
                e += 256 * value.pop(0)
                meas["energy_expended"] = e
                meas["rr"] = []
            if rr_present:
                rr = []
            while len(value) > 0:
                rr_val = value.pop(0)
                rr_val += 256 * value.pop(0)
                rr_val /= 1000.
                rr.append(rr_val)
                meas["rr"] = rr
            meas_data = {}
            if "rr" in meas:
                meas_data = {"hr": meas["hr"], "rr": mean(meas["rr"]), "contact": meas["sensor_contact"]}
                print(meas_data)
                self.socket_client.send_data(meas_data)
        except ValueError:
            print("/nNothing to return/n")
    
    def run_stream(self):
        while True:
            try:
                print("Trying to connect to Zephyr")
                self.adapter.start()
                device = self.adapter.connect(conf["MAC_adress"], timeout=10, auto_reconnect=True)
                #print(device.discover_characteristics())
                self.socket_client.connect()
                while True:
                    device.subscribe(conf["HEART_UUID"],
                                callback=self.__handle_data)
            except Exception as e:
                print("Error with Bluetooth Zephyr connection: ", e)
                print("Reconnecting to Zephyr...")
                self.adapter.stop()
                continue
