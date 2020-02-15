import os


def construct_path(paths):
    work_paths = paths.copy()
    result = work_paths.pop(0)
    while work_paths:
        result = os.path.join(result, length_check(work_paths.pop(0).replace("/", "_")))
    return result


def length_check(path_elem):
    result = ""
    BYTE_LENGTH_LIMIT = 255
    CODEC = "utf-8"
    byte_length = len(path_elem.encode(CODEC))
    if byte_length > BYTE_LENGTH_LIMIT:
        i = BYTE_LENGTH_LIMIT
        while not result:
            try:
                result = path_elem.encode(CODEC)[:i].decode(CODEC)
            except UnicodeDecodeError:
                i = i - 1
                continue
    else:
        result = path_elem
    return result


def prepare_folder(paths):
    path = construct_path(paths)
    try:
        os.makedirs(path)
    except FileExistsError:
        pass
