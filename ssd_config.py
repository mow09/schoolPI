"""SD config."""
from subprocess import run
from subprocess import PIPE
from subprocess import Popen
# from os import path
import personal_data

PROTECTED_DISK = ['/dev/disk0', '/dev/disk1']
IMAGE_FILE_PATH = 'data/2020-02-13-raspbian-buster-lite.img'


def get_disk_name(disk_size: int = 16) -> str:
    """Get the ssd dev by size and not in protected."""
    proc = run(['diskutil', 'list'], stdout=PIPE, encoding='utf-8')
    for each_info in (proc.stdout.strip().split('\n\n')):
        each_info_list = each_info.split('\n')
        disk_name = each_info_list[0].split(' ')[0]
        if (disk_name not in PROTECTED_DISK):
            for each in each_info_list[2].split(' '):
                size_range = [disk_size-1, disk_size, disk_size+1]
                if len(each) > 0:
                    for number in size_range:
                        if each.find(str(number)) > 0:
                            print(each_info)
                            return disk_name


def burn_disk(disk_name: str):
    """Unmount and burn the disk."""
    # unmoutn the disk
    run(['diskutil', 'unmountDisk', disk_name])
    # burn the image
    proc = Popen('sudo -S dd bs=1m if={} of={} conv=sync'
                 .format(IMAGE_FILE_PATH, disk_name),
                 shell=True,
                 stdin=PIPE,
                 stdout=PIPE
                 )
    proc.communicate(personal_data.pw)


def setup_ssd(set_disk: str = ''):
    """Configurat SD for RaspberryPi."""
    if set_disk:
        # [assert (each == 'word') for each in PROTECTED_DISK]
        disk_name = '/dev/' + set_disk
        print(disk_name)
        assert all([each != disk_name for each in PROTECTED_DISK])
    else:
        disk_name = get_disk_name()
    print(disk_name)
    burn_disk(disk_name)
    # run(['touch', '/Volumes/boot/ssh'])
    run(['cp', 'data/config_files/*', '/Volumes/boot/.'])
    run(['diskutil', 'unmountDisk', disk_name])


if __name__ == "__main__":
    """Run it as main."""
    print('RUN ssd_config')
    setup_ssd()
