from psutil import cpu_count, virtual_memory, disk_usage
from requests import get
import platform
import distro

mb = 1048576


os_title = distro.name()
os_name = distro.id()
os_version = distro.version()
os_codename = distro.codename()

cpu_cores = cpu_count()
cpu_arch = platform.machine()

total_memory = int(virtual_memory().total / mb)
free_memory = int(virtual_memory().free / mb)

total_disk_space = int(disk_usage('/').total / mb)
free_disk_space = int(disk_usage('/').free / mb)

external_ip = get('https://api.ipify.org').content.decode('utf8')

print(f"""
Linux distribution: {os_name}
OS version: {os_version}
OS codename: {os_codename}

CPU architecture: {cpu_arch}
CPU cores: {cpu_cores}

Total memory: {total_memory}
Free memory: {free_memory}

Total disk space: {total_disk_space}
Free disk space: {free_disk_space}

External IP address: {external_ip}
""")