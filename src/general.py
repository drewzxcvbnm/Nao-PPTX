import psutil


def flatlist(obj):
    if not isinstance(obj, list):
        return [obj]
    ret = []
    for i in obj:
        [ret.append(j) for j in flatlist(i)]
    return ret


def kill_process(name):
    pass
    for proc in psutil.process_iter():
        if proc.name().lower() == name.lower():
            proc.kill()
