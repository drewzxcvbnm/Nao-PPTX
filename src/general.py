def flatlist(obj):
    if not isinstance(obj, list):
        return [obj]
    ret = []
    for i in obj:
        [ret.append(j) for j in flatlist(i)]
    return ret

