class InstallError(Exception):
    """Base exception related to service installation"""

class DockerError(Exception):
    """Base exception related to dockerized installation"""

class SystemdError(Exception):
    """Base exception related to systemd service manipulation"""


class DependencyConflictError(InstallError):
    """Raised when a service dependency is already present on the host machine"""
    pass

class VersionError(InstallError):
    """Raised when the specified version doesn't exist for the package to be installed"""

class DbTypeError(InstallError):
    """Raised when an unsupported database is selected"""

class InstallTypeError(InstallError):
    """Raised when an unsupported install type is selected"""
    

class ContainerNameInUseError(DockerError):
    """Raised when a Docker container with the provided name already exists."""


class ServiceActionError(SystemdError):
    """Raised when an unsupported action is performed on a systemd service"""