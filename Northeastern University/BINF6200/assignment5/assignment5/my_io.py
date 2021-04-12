#!/usr/bin/env python3
# my_io.py

"""
A helper for file operation
"""

import os
from assignment5 import config


def get_fh(infile, mode):
    """
    This function opens the file based on the mode passed in
    the argument and returns filehandle.
    @param file: The file to open for the mode
    @parm mode: They way to open the file, e.g. reading, writing, etc
    @return: filehandle
    """
    try:
        file_handle = open(infile, mode=mode)
        return file_handle
    except IOError as error:
        config.get_error_string_4_IOError(infile, mode)
        raise error
    except ValueError as error:
        config.get_error_string_4_ValueError()
        raise error
    except TypeError as error:
        config.get_error_string_4_TypeError()
        raise error


def is_valid_gene_file_name(path):
    """
    test whether a path is valid
    """
    return bool(os.path.exists(path))
