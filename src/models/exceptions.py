class InstallError(Exception):
    """"""
    pass


class DependencyConflictError(InstallError):
    """Raised when a service dependency is already present on the host machine"""
    pass


class VersionError(InstallError):
    """Raised when the specified version doesn't exist for the package to be installed"""