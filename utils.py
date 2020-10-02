# -*- coding: utf-8; -*-
'''A selection of general purpose functions.'''

import subprocess
import numpy as np
from os import path, makedirs

__author__ = "Pedro Inácio"
__copyright__ = "Copyright 2015"
__version__ = "1.0"
__maintainer__ = "Pedro Inácio"
__email__ = "pedromiragaia@gmail.com"
__status__ = "Development"

def call(cmd, live=False):
    """
    Execute a command in the shell and returns stdout as string.
    Optional argument live directly prints stdout througt python's terminal.
    If the command fails, an exception is raised with stderr.
    """

    if live:
        # call command
        return_code = subprocess.call(cmd, shell=True)

        # output already printed to the terminal
        output = ["", ""]
    else:
        # create call object
        callObj = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, shell=True)

        # wait for execution to finish and get (stdout,stderr) tuple
        output = callObj.communicate()

        # collect return code
        return_code = callObj.returncode

    # check return code
    if return_code != 0:
        # return stderr
        raise RuntimeError(output[1])
    else:
        # return stdout
        return output[0]


def check_available(prg):
    """
    Check if prg is available in the system.
    Note that it only works on linux.
    """

    try:
        call("type "+prg)
    except RuntimeError, e:
        raise Exception("Could not find '"+prg+"' available in this system")

def makedir_if_not_exist(d):
    '''
    create a directory if is does not exist
    return the directory
    '''

    if not path.isdir(d):
        makedirs(d)

    return d


def confirm(prompt=None, resp=False):
    """
    Prompts for 'yes' or 'no' response from the user. Returns True for 'yes'
    and False for 'no'.

    'resp' should be set to the default value assumed by the caller when
    user simply types ENTER.

    >>> confirm(prompt='Create Directory?', resp=True)
    Create Directory? [y]|n:
    True
    >>> confirm(prompt='Create Directory?', resp=False)
    Create Directory? [n]|y:
    False
    >>> confirm(prompt='Create Directory?', resp=False)
    Create Directory? [n]|y: y
    True
    """
    # Created by Raghuram Devarakonda
    # Obtained from:
    # http://code.activestate.com/recipes/541096-prompt-the-user-for-confirmation/
    if prompt is None:
        prompt = 'Confirm'

    if resp:
        prompt = '%s [%s]|%s: ' % (prompt, 'y', 'n')
    else:
        prompt = '%s [%s]|%s: ' % (prompt, 'n', 'y')

    while True:
        ans = raw_input(prompt)
        if not ans:
            return resp
        if ans not in ['y', 'Y', 'n', 'N']:
            print 'please enter y or n.'
            continue
        if ans == 'y' or ans == 'Y':
            return True
        if ans == 'n' or ans == 'N':
            return False

def num_equal_rel(a,b,rthrs=1E-14):
    """
    check that two floating-point numbers are equal up to a relative threshold value
    """

    return np.abs( a - b ) <= (np.abs(a) + np.abs(b))*rthrs/2.0;

def num_equal_abs(a,b,athrs=1E-14):
    """
    check that two floating-point numbers are equal up to an absolute threshold value
    """

    return np.abs( a - b ) <= athrs;

def num_equal(a,b,athrs=1E-14,rthrs=1E-14):
    """
    check that floating point numbers a and b are equal up some threshold
    """

    return num_equal_abs(a,b,athrs) or num_equal_rel(a,b,rthrs)