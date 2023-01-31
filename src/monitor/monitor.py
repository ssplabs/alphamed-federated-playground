import os
import platform

from cachelib import SimpleCache
from monitor.cpu_info import CpuConstants
from monitor.memory_info import MemoryInfo
from monitor.disk_info import DiskInfo
from monitor.net_info import NetInfo
from monitor.gpu_info import GPUInfo

cache = SimpleCache()

UNIX: bool = os.name == 'posix'
SYS: str = platform.system()


def monitor():
    print(CpuConstants(unix=UNIX).get_cpu_info())
    print(MemoryInfo(unix=UNIX).get_memory_info())
    print(DiskInfo(unix=UNIX).get_info())
    # print(NetInfo().get_info())
    print(GPUInfo(unix=UNIX).get_info())

