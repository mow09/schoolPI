"""SD config."""
from subprocess import run
from subprocess import PIPE
from subprocess import Popen
# from os import path
from time import sleep
from os import path
# personal_data is not in repository
import personal_data


PROTECTED_DISK = ['/dev/disk0', '/dev/disk1']
IMAGE_FILE_PATH = 'data/2020-02-13-raspbian-buster-lite.img'
network_content = ['country=DE',
                   'ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev',
                   'update_config=1',
                   'network={',
                   '    ssid="o2-WLAN67"',
                   '    scan_ssid=1',
                   '    psk="73B66E8P646GT94H"',
                   '    key_mgmt=WPA-PSK',
                   '}']
# BOOT_VOLUME_PATH = '/Volumes/boot/'


def wait_for(what_for: str = '', secs: int = 3):
    """Just wait."""
    if what_for:
        print(what_for)
    for amount in range(secs):
        sleep(1)


def setup_network(boot_volume: str = '/Volumes/boot/'):
    """Write the networkfile into boot."""
    file_name = boot_volume+'wpa_supplicant.conf'
    with open(file_name, 'w') as f:
        for line in network_content:
            f.write(line)
            f.write('\n')
    wait_for(secs=1)
    p = run(['touch', boot_volume+'ssh'], stderr=PIPE)
    print(p.stderr)


def get_disk_name(disk_size: int = 16) -> str:
    """Get the sd dev by size and not in protected."""
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
                            # print(each_info)
                            return disk_name


def burn_disk(disk_name: str):
    """Unmount and burn the disk."""
    # unmoutn the disk
    p = run(['diskutil', 'unmountDisk', disk_name], stderr=PIPE)
    if p.stderr:
        raise 'Could not unmount - close all windows on this disk'
    print('Burn SD')
    # burn the image
    proc = Popen('sudo -S dd bs=1m if={} of={} conv=sync'
                 .format(IMAGE_FILE_PATH, disk_name),
                 shell=True,
                 stdin=PIPE,
                 # # stdout=PIPE,
                 # # stderr=PIPE,
                 )
    proc.communicate(personal_data.pw)
    # if proc.stderr:
    #     raise


def setup_sd(set_disk: str = ''):
    """Configurat SD for RaspberryPi."""
    if set_disk:
        # [assert (each == 'word') for each in PROTECTED_DISK]
        disk_name = '/dev/' + set_disk
        # print(disk_name)
        assert all([each != disk_name for each in PROTECTED_DISK])
    else:
        disk_name = get_disk_name()
    print(disk_name)
    burn_disk(disk_name)
    wait_for('setting up the network', 3)
    setup_network()
    wait_for('unmount disk', 3)
    # run(['diskutil', 'unmountDisk', disk_name])


if __name__ == "__main__":
    """Run it as main."""
    print('RUN sd_config')
    setup_sd()
