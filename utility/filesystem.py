"""Provides the DisableFileSystemRedirection class."""

import ctypes


class DisableFileSystemRedirection:
    """Class for disabling the windows file system redirection of System32/SysWOW64."""

    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection

    def __enter__(self):
        """Disable the windows file system redirection in the with statement."""
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))

    def __exit__(self, type, value, traceback):
        """Enable the windows file system redirection after the with statement."""
        if self.success:
            self._revert(self.old_value)