"""Main module from the bde-recovery package.

Can be used as application or package.
"""

import sys
# My packages:
import utility.static
import utility.recovery
import utility.filesystem


def start(drive_letter, recovery_method):
    """Recovers an encrypted BitLocker drive.

    Arguments:
        drive_letter -- The BitLocker drive letter.
        recovery_method -- How the drive should be recovered.
    """
    # Simple recovery method.
    if recovery_method == utility.static.recovery_methods[0]:
        recovery_method_function = utility.recovery.simple_recovery
    # Random recovery method.
    elif recovery_method == utility.static.recovery_methods[1]:
        recovery_method_function = utility.recovery.random_recovery
    else:
        sys.exit("Unknown recovery method!\nMethods: {0}".format(', '.join(utility.static.recovery_methods)))

    # Start with disabling the System32/SysWOW64 file system redirection.
    with utility.filesystem.DisableFileSystemRedirection():
        # Add the drive letter to the command_pattern.
        utility.static.command_pattern += drive_letter
        recovery_method_function()


if __name__ == "__main__":
    if len(sys.argv) == 3:
        start(sys.argv[1], sys.argv[2])
    else:
        sys.exit("Wrong number of arguments!\nUsage: bde-recovery.py <Drive> <Recovery method>")
