# -*- coding: utf-8 -*-
"""Generic utility methods
"""


def sanitize_search_string(search_string: str = None) -> str:
    """Simple string cleaning (only spaces)

    Args:
        search_string (str, optional): string to be cleaned.
        Defaults to None.

    Returns:
        str: cleaned string
    """
    return ' '.join(search_string.split())


def update_progress(count: int = 0, total: int = 100):
    """This generates a progress bar with '#' and prints the same line

    Args:
        count (int, optional): [description]. Defaults to 0.
        total (int, optional): [description]. Defaults to 100.
    """
    progress = count * int(100 / int(total))

    if progress > 100 or count == total:
        progress = 100

    print(progress_bar(progress), end='')

    if progress == 100:
        print("")  # kind of eol


def progress_bar(progress: int = 0) -> str:
    """This method prepares progress bar as string
    with `#` and space and percentage value.

    Args:
        progress (int): progress over 100

    Returns:
        str: progres bar with percentage info.
    """
    completed = '#'*(progress//10)
    not_completed = ' '*(10-progress//10)
    return f"\r [{completed}{not_completed}] {progress}%"


def pprint_dict(dict_to_print: dict = None) -> None:
    """This prints the given dict in formatted way where
    it calculates the max for the keys and fills with spaces
    if the key has less chars than max

    Args:
        dict_to_print (dict): dict to print
    """
    max_title_length = 0
    for key, value in dict_to_print.items():
        if len(key) > max_title_length:
            max_title_length = len(key)

    for key, value in dict_to_print.items():
        print("\t%s - %s", str(key).ljust(max_title_length), value)


def yes_or_no(question: str = None, default: str = "yes") -> bool:
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
            It must be "yes" (the default), "no" or None (meaning
            an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError(f"invalid default answer: '{default}'")

    while True:
        choice = input(question + prompt).lower()
        if default is not None and choice == "":
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            print("Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n")
