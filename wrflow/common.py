from hashlib import sha1

__all__ = [
    'hash_dict',
]


def hash_dict(dict_obj):
    hash = sha1()
    for k in sorted(dict_obj.keys()):
        hash.update(k)
        hash.update('\0')
        hash.update(dict_obj[k])
        hash.update('\0')
    return hash.hexdigest()


def hash_set(set_obj):
    hash = sha1()
    for k in sorted(set_obj):
        hash.update(k)
        hash.update('\0')
    return hash.hexdigest()


def hash_list(list_obj):
    hash = sha1()
    for k in list_obj:
        hash.update(k)
        hash.update('\0')
    return hash.hexdigest()
