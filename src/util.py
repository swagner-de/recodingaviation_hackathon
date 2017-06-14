def filter_dict(d: dict, allowed_keys=set) ->dict:
    return {k: d[k] for k in allowed_keys.intersection(d.keys())}
