class InstallError(Exception):
    """Base exception related to service installation"""

class DependencyConflictError(InstallError):
    """Raised when a service dependency is already present on the host machine"""
    pass

class VersionError(InstallError):
    """Raised when the specified version doesn't exist for the package to be installed"""

class DbTypeError(InstallError):
    """Raised when an unsupported database is selected"""

class InstallTypeError(InstallError):
    """Raised when an unsupported install type is selected"""