def req_filter(value, data):
    return list(filter(lambda l: value in l, [line for line in data]))


def req_map(value, data):
    return list(map(lambda l: l[int(value)], [line.split() for line in data if len(line) > 0]))


def req_unique(data):
    res = [line for line in data]
    return set(res)


def req_sort(value, data):
    if value == 'desc':
        return sorted([line for line in data], reverse=True)
    else:
        return sorted([line for line in data], reverse=False)


def req_limit(value, data):
    return [line for line in data][:int(value)]
