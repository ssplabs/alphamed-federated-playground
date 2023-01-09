import re

import psutil
from libs.other_utils import ToSizeString
from monitor.cpu_info import CpuConstants


class SystemInfo(object):
    def gather_disk_info(self):
        all_used = 0
        total = 0
        part_list = psutil.disk_partitions()
        device_dict = {}
        for item in part_list:
            it_usage = psutil.disk_usage(item.mountpoint)
            all_used += it_usage.used
            if re.match("^/dev/disk\d{1,2}", item.device):
                device_name = re.match("^/dev/disk\d{1,2}", item.device).group()
            else:
                device_name = item.device
            if not device_dict.get(device_name):
                device_dict[device_name] = it_usage.total
        for k, v in device_dict.items():
            total += v
        return ToSizeString(all_used), ToSizeString(total)

    def gather_cpu_info(self):

        res = CpuConstants(unix=True).get_cpu_info()
        return "{0}*{1}".format(res["cpu_name"], res["cpu_core"])

    def dispatch(self):
        disk_used, disk_total = self.gather_disk_info()
        cpu_info = self.gather_cpu_info()

        {
            "disk": "{0}/{1}".format(disk_used, disk_total),
            "cpu": cpu_info
        }
        import pdb
        pdb.set_trace()
