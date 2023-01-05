from typing import List, Dict, Any

import os
import time
import psutil
import platform
import hashlib
import re
import sys

from cachelib import SimpleCache
from cpu_info import CpuConstants
from memory_info import MemoryInfo
from disk_info import DiskInfo
from net_info import NetInfo

cache = SimpleCache()

UNIX: bool = os.name == 'posix'
SYS: str = platform.system()


if __name__ == "__main__":
    print(CpuConstants(unix=UNIX).get_cpu_info())
    print(MemoryInfo(unix=UNIX).get_memory_info())
    print(DiskInfo(unix=UNIX).get_info())
    print(NetInfo().get_info())
