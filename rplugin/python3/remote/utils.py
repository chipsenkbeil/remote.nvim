# =============================================================================
# FILE: utils.py
# AUTHOR: Chip Senkbeil <chip.senkbeil at gmail.com>
# License: Apache 2.0 License
# =============================================================================
import glob
import importlib
import os


def to_int(s, default=None):
    """Attempts to convert the provided string to an integer.

    :param s: The text to convert
    :param default: Default value to return if cannot be converted
    :returns: The integer if converted, otherwise the default value
    """
    try:
        return int(s)
    except ValueError:
        pass

    return default


def is_int(s):
    """Checks if the provided string is an integer.

    :param s: The text to check
    :returns: True if an integer, otherwise False
    """
    return to_int(s) is not None


def find_subclasses(cl, include_indirect=True):
    """Finds all classes that subclass the provided class, even indirectly.

    :param cl: The class whose subclasses to find
    :param include_indirect: If True, will retrieve indirect subclasses,
                             otherwise will only return top-level subclasses
    :returns: A list of class objects representing the subclasses
    """
    assert isinstance(cl, type)
    class_list = []

    if (include_indirect):
        queue = []

        # Enqueue top-level class
        queue.append(cl)

        while (len(queue) > 0):
            next_class = queue.pop(0)  # Dequeue next class to search
            class_list.append(next_class)
            queue.extend(next_class.__subclasses__())
    else:
        class_list = [cl]
        class_list.extend(cl.__subclasses__())

    # Return all classes but the first since that is the class we started with
    return class_list[1:]


def load_all_modules(base_dir, base_pkg, exclusions=[]):
    """Dynamically loads all modules at the root of the base directory using
    the provided base package as the package to load them in.

    :param base_dir: The directory whose python files to load as modules
    :param base_pkg: The base package to use when loading modules
    :param exclusions: If included, will exclude any module whose package name
                       matches the provided
    :returns: The loaded modules
    """
    mods = []

    # Load all modules immediately
    glob_str = os.path.join(base_dir, '**', '*.py')
    for location in glob.iglob(glob_str, recursive=True):
        name = base_pkg + '.' + os.path.splitext(os.path.basename(location))[0]

        if (name in exclusions):
            continue

        spec = importlib.util.spec_from_file_location(name, location)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        mods.append(mod)

    # Return loaded modules
    return mods
