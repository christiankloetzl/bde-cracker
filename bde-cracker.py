"""Main module from the bde-cracker package.

Can be used as application or package.
"""

import sys
# My packages:
import utility.static
import utility.cracking
import utility.filesystem


def start(drive_letter, cracking_method):
    """Brute force an encrypted BitLocker drive.

    Arguments:
        drive_letter -- The BitLocker drive letter.
        cracking_method -- How the drive should be brute forced.
    """
    # Simple brute force.
    if cracking_method == utility.static.cracking_methods[0]:
        cracking_method_function = utility.cracking.simple_brute_force
    # Random brute force.
    elif cracking_method == utility.static.cracking_methods[1]:
        cracking_method_function = utility.cracking.random_brute_force
    else:
        sys.exit("Unknown cracking method!\nMethods: {0}".format(', '.join(utility.static.cracking_methods)))

    # Start with disabling the System32/SysWOW64 file system redirection.
    with utility.filesystem.DisableFileSystemRedirection():
        cracking_method_function(drive_letter)


if __name__ == "__main__":
    if len(sys.argv) == 3:
        start(sys.argv[1], sys.argv[2])
    else:
        sys.exit("Wrong number of arguments!\nUsage: bde-cracker.py <Drive> <Cracking method>")
