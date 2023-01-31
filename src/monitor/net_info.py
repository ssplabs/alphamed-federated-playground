import re
import threading
import time
from collections import deque

import psutil


class NetInfo(object):

    def __init__(self):
        self.interface_dict = dict()

    def get_interface_dict(self):
        net_if_dict = psutil.net_if_addrs()
        for if_device_name, if_device in net_if_dict.items():
            if re.match(r"^(en|eth)\d", if_device_name):
                self.interface_dict[if_device_name] = {
                    "address": net_if_dict[if_device_name][0].address,
                    "netmask": net_if_dict[if_device_name][0].netmask,
                    "broadcast": net_if_dict[if_device_name][0].broadcast
                }

    def print_rate(self, rate):
        try:
            print("{0}  UL: {1:.0f} kB/s / DL: {2:.0f} kB/s".format(*rate[-1]))
        except IndexError:
            "UL: - kB/s/ DL: - kB/s"

    def get_info(self):
        self.get_interface_dict()
        # Create the ul/dl thread and a deque of length 1 to hold the ul/dl- values
        q_len = len(list(self.interface_dict.keys()))
        transfer_rate = deque(maxlen=q_len)
        for interface, info in self.interface_dict.items():
            t = threading.Thread(target=self.calc_ul_dl, args=(transfer_rate, interface))
            # The program will exit if there are only daemonic threads left.
            t.daemon = True
            t.start()
        end = time.time() + 10
        while True:
            self.print_rate(transfer_rate)
            time.sleep(0.2)
            if time.time() > end:
                return True


    def calc_ul_dl(self, rate, interface, dt=3):
        t0 = time.time()
        counter = psutil.net_io_counters(pernic=True)[interface]
        tot = (counter.bytes_sent, counter.bytes_recv)
        while True:
            last_tot = tot
            time.sleep(dt)
            counter = psutil.net_io_counters(pernic=True)[interface]
            t1 = time.time()
            tot = (counter.bytes_sent, counter.bytes_recv)
            ul, dl = [
                (now - last) / (t1 - t0) / 1000.0
                for now, last in zip(tot, last_tot)
            ]
            rate.append((interface, ul, dl))
            t0 = time.time()
