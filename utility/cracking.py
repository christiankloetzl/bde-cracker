"""Provides different password cracking methods."""
import subprocess
# My packages:
import utility.static


def simple_brute_force(drive):
    """Brute forces a BitLocker drive with a simple brute force mechanism."""
    drive_is_encrypted = True
    numeric_plain_recovery_key = 0
    # Add the drive letter to the command_pattern.
    utility.static.command_pattern += drive
    # Start the brute force attack.
    while drive_is_encrypted:
        # Build the recovery key
        recovery_key = make_recovery_key_from_int(numeric_plain_recovery_key)
        # Try the recovery_key
        recovery_key_works = try_recovery_key(recovery_key)
        if recovery_key_works:
            drive_is_encrypted = False
            print(recovery_key)
        numeric_plain_recovery_key += 1


def random_brute_force(drive):
    pass


def try_recovery_key(recovery_key):
    """Tries to open the BitLocker drive with the manage-bde command and the recovery key."""
    command = utility.static.command_pattern.format(recovery_key)
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    process.wait()
    if process.returncode == 0:
        return True
    else:
        return False


def make_recovery_key_from_int(numeric_recovery_key):
    """Builds a BitLocker recovery key from a integer value."""
    rc = str(numeric_recovery_key).zfill(48)
    recovery_key = rc[0:6] + '-' + rc[6:12] + '-' + rc[12:18] + '-' + rc[18:24] + '-' + rc[24:30] + '-' + rc[30:36] +\
        '-' + rc[36:42] + '-' + rc[42:48]
    return recovery_key
