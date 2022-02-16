# utils.py


def update_progress(count: int = 0, total: int = 100):
    """This generates a progress bar with '#' and prints the same line

    Args:
        count (int, optional): [description]. Defaults to 0.
        total (int, optional): [description]. Defaults to 100.
    """
    progress = count * int(100 / int(total))

    if progress > 100 or count == total:
        progress = 100

    print("\r [{0}{1}] {2}%".format('#'*(progress//10),
                                    ' '*(10 - progress//10),
                                    progress), end='')
    if progress == 100:
        print("")  # kind of eol


def pprint_dict(dict_to_print: None) -> None:
    max_title_length = 0
    for key, value in dict_to_print.items():
        if len(key) > max_title_length:
            max_title_length = len(key)

    for key, value in dict_to_print.items():
        print("\t{} - {}".format(str(key).ljust(max_title_length), value))


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
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        choice = input(question + prompt).lower()
        if default is not None and choice == "":
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            print("Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n")
