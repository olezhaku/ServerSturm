import psutil


def sys_mon() -> dict:
    cpu_cores = psutil.cpu_count(logical=False)
    cpu_percent = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    # Processes
    # for proc in psutil.process_iter(["pid", "name", "cpu_percent"]):
    #     print(proc.info)

    def as_gb(value):
        return round(value / 1024 / 1024 / 1024, 1)

    return {
        "CPU": f"{cpu_cores} cores - {cpu_percent}%",
        "RAM": f"({as_gb(mem.total)} / {as_gb(mem.total) - as_gb(mem.used)}) GB - {mem.percent}%",
        "Disk": f"({as_gb(disk.total)} / {as_gb(disk.free)}) GB - {disk.percent}%",
    }
