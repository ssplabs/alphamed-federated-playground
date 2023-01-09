import psutil
from libs.other_utils import ExecShellUnix


class GPUInfo(object):
    def __init__(self, unix=False):
        self.unix = unix

    def get_info(self):
        try:
            if self.unix:
                return self.get_gpu_info()
            else:
                print("暂时不支持Windows系统")
        except Exception as err:
            print('获取GPU信息异常（unix: {}）：'.format(self.unix), err)
            return []

    def get_gpu_info(self):
        res = ExecShellUnix("nvidia-smi --query-gpu=gpu_name,memory.used,memory.total,gpu_uuid --format=csv")
        assert res, "only support nvidia gpu"
        assert "command not found" not in "".join(res), "only support nvidia gpu"
        import pdb
        pdb.set_trace()
