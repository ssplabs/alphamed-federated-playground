import hashlib


def md5(strings: str) -> str:
    '''
    生成md5

    Parameters
    ----------
    strings : TYPE
        要进行hash处理的字符串

    Returns
    -------
    str[32]
        hash后的字符串.

    '''

    m = hashlib.md5()
    m.update(strings.encode('utf-8'))
    return m.hexdigest()


def readFile(filename: str) -> str:
    '''
    读取文件内容

    Parameters
    ----------
    filename : str
        文件名.

    Returns
    -------
    str
        文件内容.

    '''
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    except:
        pass

    return ''


def ExecShellUnix(cmdstring: str, shell=True):
    '''
    执行Shell命令（Unix）

    Parameters
    ----------
    cmdstring : str
        DESCRIPTION.
    shell : TYPE, optional
        DESCRIPTION. The default is True.

    Returns
    -------
    a : TYPE
        DESCRIPTION.
    e : TYPE
        DESCRIPTION.

    '''
    a: str = ''
    e: str = ''
    import subprocess, tempfile

    try:
        rx: str = md5(cmdstring)
        succ_f = tempfile.SpooledTemporaryFile(
            max_size=4096,
            mode='wb+',
            suffix='_succ',
            prefix='btex_' + rx,
            dir='/tmp'
        )
        err_f = tempfile.SpooledTemporaryFile(
            max_size=4096,
            mode='wb+',
            suffix='_err',
            prefix='btex_' + rx,
            dir='/tmp'
        )
        sub = subprocess.Popen(
            cmdstring,
            close_fds=True,
            shell=shell,
            bufsize=128,
            stdout=succ_f,
            stderr=err_f
        )
        sub.wait()
        err_f.seek(0)
        succ_f.seek(0)
        a = succ_f.read()
        e = err_f.read()
        if not err_f.closed: err_f.close()
        if not succ_f.closed: succ_f.close()
    except Exception as err:
        print(err)
    try:
        if type(a) == bytes: a = a.decode('utf-8')
        if type(e) == bytes: e = e.decode('utf-8')
    except Exception as err:
        print(err)

    return a, e


def ToSizeInt(byte: int, target: str) -> int:
    '''
    将字节大小转换为目标单位的大小

    Parameters
    ----------
    byte : int
        int格式的字节大小（bytes size）
    target : str
        目标单位，str.

    Returns
    -------
    int
        转换为目标单位后的字节大小.

    '''
    return int(byte / 1024 ** (('KB', 'MB', 'GB', 'TB').index(target) + 1))


def ToSizeString(byte: int) -> str:
    '''
    获取字节大小字符串

    Parameters
    ----------
    byte : int
        int格式的字节大小（bytes size）.

    Returns
    -------
    str
        自动转换后的大小字符串，如：6.90 GB.

    '''
    units: tuple = ('b', 'KB', 'MB', 'GB', 'TB')
    re = lambda: '{:.2f} {}'.format(byte, u)
    for u in units:
        if byte < 1024: return re()
        byte /= 1024
    return re()


def ToSizeString(byte: int, start_pix="byte") -> int:
    '''
    将字节大小转换为目标单位的大小
    '''
    pix_list = ["byte", "KB", "MB", "GB", "TB"]
    if start_pix not in pix_list:
        print("Invalid start_pix not in pix_list")
        return False
    pix_list = pix_list[pix_list.index(start_pix):]
    for pix in pix_list:
        if byte < 1024:
            return f"{byte:<.1f}{pix}"
        else:
            byte = byte * 1.0 / 1024

    return f"{byte:<.1f}{pix}"
