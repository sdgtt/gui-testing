class PyGUItError(Exception):
    """Base exception for PyGUIt."""


class WindowNotFoundError(PyGUItError):
    """Raised when a window with the given title cannot be found."""


class ProcessNotFoundError(PyGUItError):
    """Raised when attempting to stop a process that was not started."""


class DisplayNotAvailableError(PyGUItError):
    """Raised when no display is available and virtual display cannot be created."""


class PlatformNotSupportedError(PyGUItError):
    """Raised when calling a platform-specific method on an unsupported OS."""


class ValidationError(PyGUItError):
    """Raised when validation checks fail."""
