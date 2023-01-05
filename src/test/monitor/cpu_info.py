import psutil
import re
import time
from typing import List, Dict, Any
from utils import readFile, ExecShellUnix


class CpuConstants:
    def __init__(self, unix=False):
        '''
        初始化CPU常量（多平台）

        Returns
        -------
        self.

        '''
        self.WMI = None
        self.cpuList: list = []  # windows only

        self.cpuCount: int = 0  # 物理cpu数量
        self.cpuCore: int = 0  # cpu物理核心数
        self.cpuThreads: int = 0  # cpu逻辑核心数
        self.cpuName: str = ''  # cpu型号
        self.unix = unix

    def get_cpu_info(self) -> Dict[str, Any]:
        if self.unix:
            self.GetCpuConstantsUnix(True)
        else:
            self.GetCpuConstantsWindows(True)

        self.cpuThreads: int = psutil.cpu_count()

        # cpu物理核心数
        self.cpuCore: int = psutil.cpu_count(logical=False)

        time.sleep(0.5)
        total_percent: float = psutil.cpu_percent(interval=1)

        thread_percent: List[float] = psutil.cpu_percent(percpu=True)

        return {
            'cpu_count': self.cpuCount,
            'cpu_name': self.cpuName,
            'cpu_core': self.cpuCore,
            'cpu_threads': self.cpuThreads,
            'total_percent': total_percent,
            'thread_percent': thread_percent
        }

    def GetCpuConstantsUnix(self, update: bool = False) -> None:
        '''
        获取unix下的cpu信息

        Parameters
        ----------
        update : bool, optional
            DESCRIPTION. The default is False.

        Returns
        -------
        None
            DESCRIPTION.

        '''

        ids: list = re.findall("processor.+", readFile('/proc/cpuinfo'))
        # 物理cpu个数
        self.cpuCount: int = len(set(ids))

        # cpu型号（名称）
        self.cpuName: str = self.getCpuTypeUnix()

    def GetCpuConstantsWindows(self, update: bool = False) -> None:
        '''
        获取windows平台的cpu信息

        Parameters
        ----------
        update : bool, optional
            强制更新数据. The default is False.

        Returns
        -------
        None
            DESCRIPTION.

        '''
        # 初始化wmi
        try:
            import wmi
            if self.WMI == None:
                self.WMI = wmi.WMI()
            # cpu列表
            self.cpuList: list = self.WMI.Win32_Processor()
        except ImportError as e:
            print(e)

        # 物理cpu个数
        self.cpuCount: int = len(self.cpuList)

        # cpu型号（名称）
        self.cpuName: str = self.cpuList[0].Name

    @staticmethod
    def getCpuTypeUnix() -> str:
        '''
        获取CPU型号（unix）

        Returns
        -------
        str
            CPU型号.

        '''
        cpuinfo: str = readFile('/proc/cpuinfo')
        rep: str = 'model\s+name\s+:\s+(.+)'
        tmp = re.search(rep, cpuinfo, re.I)
        cpuType: str = ''
        if tmp:
            cpuType: str = tmp.groups()[0]
        else:
            cpuinfo = ExecShellUnix('LANG="en_US.UTF-8" && lscpu')[0]
            rep = 'Model\s+name:\s+(.+)'
            tmp = re.search(rep, cpuinfo, re.I)
            if tmp: cpuType = tmp.groups()[0]
        return cpuType
