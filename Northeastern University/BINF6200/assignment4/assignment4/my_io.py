#!/usr/bin/env python3
# my_io.py
"""
This function opens the file based on the mode passed in
the argument and returns filehandle.
@param file: The file to open for the mode
@parm mode: They way to open the file, e.g. reading, writing, etc
@return: filehandle
"""


def get_fh(infile, mode):
    """get the file handle"""
    try:
        file_handle = open(infile, mode=mode)
        return file_handle
    except IOError as error:
        print('cannot open', infile)
        raise error
    except ValueError as error:
        print('wrong open mode')
        raise error
