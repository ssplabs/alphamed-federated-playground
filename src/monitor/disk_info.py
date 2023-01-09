import psutil
from libs.other_utils import ExecShellUnix


class DiskInfo(object):
    def __init__(self, unix=False):
        self.unix = unix

    def get_info(self):
        try:
            if self.unix:
                return self.get_disk_info_unix()
            else:
                return self.get_disk_info_windows()
        except Exception as err:
            print('获取磁盘信息异常（unix: {}）：'.format(self.unix), err)
            return []

    def get_disk_info_windows(self) -> list:
        '''
        获取磁盘信息Windows

        Returns
        -------
        diskInfo : list
            列表.

        '''
        diskIo: list = psutil.disk_partitions()
        diskInfo: list = []
        for disk in diskIo:
            tmp: dict = {}
            try:
                tmp['path'] = disk.mountpoint.replace("\\", "/")
                usage = psutil.disk_usage(disk.mountpoint)
                tmp['size'] = {
                    'total': usage.total,
                    'used': usage.used,
                    'free': usage.free,
                    'percent': usage.percent
                }
                tmp['fstype'] = disk.fstype
                tmp['inodes'] = False
                diskInfo.append(tmp)
            except:
                pass
        return diskInfo

    def get_disk_info_unix(self) -> list:
        '''
       获取硬盘分区信息（unix）

       Returns
       -------
       list
           DESCRIPTION.

       '''

        temp: list = (
            ExecShellUnix("df -h -P|grep '/dev'|grep -v tmpfs")[0]).split('\n')
        diskInfo: list = []
        n: int = 0
        cuts: list = [
            '/mnt/cdrom',
            '/boot',
            '/boot/efi',
            '/dev',
            '/dev/shm',
            '/run/lock',
            '/run',
            '/run/shm',
            '/run/user'
        ]
        for tmp in temp:
            n += 1
            try:
                disk: list = tmp.split()
                if len(disk) != 5 or disk[1].find('M') != -1 or disk[1].find('K') != -1 or len(
                        disk[5].split('/')) > 10 or disk[5] in cuts or disk[5].find('docker') != -1:
                    continue
                arr = {}
                arr['path'] = disk[5]
                arr['device'] = disk[0]
                arr['total'] = disk[1]
                arr['used'] = disk[2]
                arr['used'] = disk[2]
                arr['free'] = disk[3]
                arr['used_percent'] = float(disk[4][:-2])

                diskInfo.append(arr)
            except Exception as ex:
                print('信息获取错误：', str(ex))
                continue
        return diskInfo
