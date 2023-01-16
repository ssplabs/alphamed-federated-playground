import re

import psutil
from libs.other_utils import ToSizeString
from monitor.cpu_info import CpuConstants
from libs.other_utils import ExecShellUnix


class SystemInfo(object):
    def gather_disk_info(self):
        all_used = 0
        total = 0
        device_dict = {}
        res = ExecShellUnix("df -k | awk '{print $1,$2,$3}' | grep '/dev' ")
        assert res, "gather disk into failed"
        for line in "\n".join(res).strip("\n").split("\n"):
            pre_device_name = line.split(" ")[0]
            device_total = int(line.split(" ")[1])
            device_used = int(line.split(" ")[2])
            if re.match("^/dev/disk\d{1,2}", pre_device_name):
                device_name = re.match("^/dev/disk\d{1,2}", pre_device_name).group()
            else:
                device_name = pre_device_name
            if not device_dict.get(device_name):
                device_dict[device_name] = device_total
            all_used += device_used
        for k, v in device_dict.items():
            total += v
        print(ToSizeString(all_used, start_pix="KB"), ToSizeString(total, start_pix="KB"))
        return ToSizeString(all_used, start_pix="KB"), ToSizeString(total, start_pix="KB")

    @staticmethod
    def gather_cpu_info():
        res = CpuConstants(unix=True).get_cpu_info()
        if res["cpu_core"] == res["cpu_threads"]:
            cpu_core = res["cpu_core"]
        else:
            cpu_core = res["cpu_threads"]
        return "{0} * {1}".format(res["cpu_name"], cpu_core)

    @staticmethod
    def gather_memory_info():
        res = psutil.virtual_memory()
        return ToSizeString(res.total)

    @staticmethod
    def gather_gpu_info():
        from monitor.gpu_info import GPUInfo
        res = GPUInfo(unix=True).get_info()
        return res

    def dispatch(self):
        disk_used, disk_total = self.gather_disk_info()
        cpu_info = self.gather_cpu_info()
        gpu_info = self.gather_gpu_info()

        ret_dict = {
            "disk": "{0}/{1}".format(disk_used, disk_total),
            "cpu": cpu_info.strip(),
            "memory": self.gather_memory_info(),
            "gpu": ""
        }
        if gpu_info:
            ret_dict["gpu"] = "{0} {1}".format(gpu_info["name"], gpu_info["memory_total"])
        return ret_dict
