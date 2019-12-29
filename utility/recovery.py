"""Provides different password recovery methods."""
import gc
import random
import subprocess
# My packages:
import utility.static


def simple_recovery():
    """Recovers a BitLocker drive with a simple brute force mechanism."""
    drive_is_encrypted = True
    numeric_plain_recovery_key = 0
    # Start the brute force attack.
    while drive_is_encrypted:
        # Build the recovery key
        recovery_key = make_recovery_key(str(numeric_plain_recovery_key).zfill(48))
        # Try the recovery_key
        recovery_key_works = try_recovery_key(recovery_key)
        if recovery_key_works:
            drive_is_encrypted = False
            print(recovery_key)
        numeric_plain_recovery_key += 1


def random_brute_force():
    """Recovers a BitLocker drive with random recovery keys."""
    processes = []
    process_count = 100
    drive_is_encrypted = True
    # Minimum and maximum length of the numeric recovery key.
    minimum_length_of_recovery_key = 100000000000000000000000000000000000000000000000
    maximum_length_of_recovery_key = 999999999999999999999999999999999999999999999999
    # Start the brute force attack.
    while drive_is_encrypted:
        # Build the recovery key
        numeric_recovery_key = random.randint(minimum_length_of_recovery_key, maximum_length_of_recovery_key)
        recovery_key = make_recovery_key(str(numeric_recovery_key))
        # Start the processes.
        for _ in range(0, process_count):
            command = utility.static.command_pattern.format(recovery_key)
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
            processes.append(process)
        # Wait for all processes.
        for process in processes:
            process.wait()
            # If nothing is written in stdout or stderr an exception occurs.
            try:
                # Close file descriptors.
                process.stdout.close()
                process.stderr.close()
            except AttributeError:
                pass
            if process.returncode == 0 and drive_is_encrypted is True:
                drive_is_encrypted = False
                print(process.args.split()[-2])
        gc.collect()


def try_recovery_key(recovery_key):
    """Tries to open the BitLocker drive with the manage-bde command and the recovery key."""
    command = utility.static.command_pattern.format(recovery_key)
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    process.wait()
    if process.returncode == 0:
        return True
    else:
        return False


def make_recovery_key(numeric_recovery_key):
    """Builds a BitLocker recovery key from a integer value."""
    rc = numeric_recovery_key
    recovery_key = rc[0:6] + '-' + rc[6:12] + '-' + rc[12:18] + '-' + rc[18:24] + '-' + rc[24:30] + '-' + rc[30:36] +\
        '-' + rc[36:42] + '-' + rc[42:48]
    return recovery_key
