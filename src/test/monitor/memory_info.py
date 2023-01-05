import psutil
from typing import List, Dict, Any
from utils import ToSizeString


class MemoryInfo(object):

    def __init__(self, unix=False):
        self.unix = unix

    def get_memory_info(self):
        if self.unix:
            return self.get_memory_info_unix()
        else:
            return self.get_memory_info_windows()

    def get_memory_info_unix(self) -> Dict[str, int]:
        '''
        获取内存信息（unix）

        Returns
        -------
        dict
            DESCRIPTION.


        '''
        mem = psutil.virtual_memory()
        memInfo: dict = {'memTotal': ToSizeString(mem.total),
                         'memFree': ToSizeString(mem.free)
                         }
        memInfo['memRealUsed'] = ToSizeString(mem.total - mem.free)

        memInfo['memUsedPercent'] = (1 - mem.free * 1.0 / mem.total) * 100

        return memInfo

    def get_memory_info_windows(self) -> dict:
        '''
        获取内存信息（windows）

        Returns
        -------
        dict
            DESCRIPTION.

        '''
        mem = psutil.virtual_memory()
        memInfo: dict = {
            'memTotal': ToSizeString(mem.total),
            'memFree': ToSizeString(mem.free),
            'memRealUsed': ToSizeString(mem.used),
            'menUsedPercent': mem.used / mem.total * 100
        }

        return memInfo
