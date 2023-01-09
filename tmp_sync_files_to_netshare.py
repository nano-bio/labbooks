from os import system
from pathlib import Path
from time import sleep

MEDIA_ROOT_OLD = Path('/var/opt/labbooks/mediaroot')

MEDIA_ROOT = Path('/mnt/bigshare/Temp/labbooks')
# MEDIA_ROOT.mkdir(exist_ok=True, parents=True)

FOLDERS = [
    [MEDIA_ROOT_OLD, MEDIA_ROOT],
    [Path("/var/storage/clustof"), MEDIA_ROOT / 'clustof' / 'tof']
]


def rsync_folder(folder_from: Path, folder_to: Path):
    # folder_to.mkdir(exist_ok=True, parents=True)
    command = [
        "rsync -av",
        f'{folder_from.as_posix()}/',
        folder_to.as_posix()]
    print(" ".join(command))
    # sleep(4)
    return 0
    # return int(system(" ".join(command)))


errors = 0
for folder in FOLDERS:
    errors += rsync_folder(folder[0], folder[1])
print(f"Total errors: {errors}")
