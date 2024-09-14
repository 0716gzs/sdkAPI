from typing import List, Dict


def arglist_to_dict(arglist: List[str]) -> Dict[str, str]:
    """Convert a list of arguments like ['arg1=val1', 'arg2=val2', ...] to a
    dict
    """
    return dict(x.split("=", 1) for x in arglist)
