class InstallError(Exception):
    """"""
    pass


class DependencyConflictError(InstallError):
    """Raised when a service dependency is already present on the host machine"""
    pass