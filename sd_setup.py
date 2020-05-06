"""SD config."""
from subprocess import run
from subprocess import PIPE
from subprocess import Popen
from time import sleep
import os
# personal_data is not in repository
import personal_data


PROTECTED_DISK = ['/dev/disk0', '/dev/disk1']
IMAGE_FILE_PATH = 'data/2020-02-13-raspbian-buster-lite.img'
network_insert = ['country=DE',
                   'ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev',
                   'update_config=1',
                   'network={',
                   '    ssid="{{ wlan_name }}"',
                   '    scan_ssid=1',
                   '    psk="{{ wlan_pw }}"',
                   '    key_mgmt=WPA-PSK',
                   '}']
network_content = ['country=DE',
                   'ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev',
                   'update_config=1',
                   'network={',
                   '    ssid="o2-WLAN67"',
                   '    scan_ssid=1',
                   '    psk="73B66E8P646GT94H"',
                   '    key_mgmt=WPA-PSK',
                   '}',
                   'network={',
                   '    ssid="ASS-PN"',
                   '    scan_ssid=1',
                   '    psk="#HdWwhWidS!?"',
                   '    key_mgmt=WPA-PSK',
                   '}']


def wait_for(what_for: str = '', secs: int = 3):
    """Just wait."""
    if what_for:
        print(what_for)
    for amount in range(secs):
        sleep(1)


def setup_network(boot_volume: str):
    """Write the networkfile into boot."""
    p = run(['uname', '-s'], stdout=PIPE, encoding='utf-8')
    # print(p.stdout.strip())
    if not boot_volume:
        if p.stdout.strip() == 'Darwin':
            boot_volume = '/Volumes/boot/'
        elif p.stdout.strip() == 'Linux':
            boot_volume = '/media/boot/'
    while not boot_volume:
        ...
    file_name_wpa = os.path.join(boot_volume, 'wpa_supplicant.conf')
    print('Put network files.')
    with open(file_name_wpa, 'w') as f:
        for line in network_content:
            f.write(line)
            f.write('\n')
    wait_for(secs=1)
    file_name_ssh = os.path.join(boot_volume, 'ssh')
    p = run(['touch', file_name_ssh], stderr=PIPE)
    print(p.stderr)


def get_disk_name(disk_size: int = 16) -> str:
    """Get the SD dev by size and not in protected."""
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


def choose_image():
    """Menu to choose the image."""
    menu_holder = {}
    counter = 1
    for file in (os.listdir('data/')):
        if 'raspbian' in file:
            # print(file)
            if file.endswith('.img'):
                menu_holder[counter] = file
            counter += 1
    menu_display = 'Press number:\n'
    for key, val in menu_holder.items():
        menu_display += f'\t{key}: {val}\n'

    try:
        file_nr = int(input(f"{menu_display}"))
        if file_nr not in [key for key in menu_holder.keys()]:
            print(f'Number must be in {[key for key in menu_holder.keys()]}')
            choose_image()
    except ValueError:
        print('It must be a number.')
        print('It must be an integer')
        choose_image()

    return menu_holder[file_nr]


def burn_disk(disk_name: str):
    """Unmount and burn disk.

    Make sure you set up your personal_data.py with pw=str().
    """
    image_path = os.path.join('data/', choose_image())
    # unmoutn the disk
    p = run(['diskutil', 'unmountDisk', disk_name], stderr=PIPE)
    if p.stderr:
        raise 'Could not unmount - close all windows on this disk'
    print('Burn SD')
    # burn the image
    proc = Popen('sudo -S dd bs=1m if={} of={} conv=sync'
                 .format(image_path, disk_name),
                 shell=True,
                 stdin=PIPE,
                 # # stdout=PIPE,
                 # # stderr=PIPE,
                 )
    proc.communicate(personal_data.pw)


def setup_sd(set_disk: str = ''):
    """Configurat SD for RaspberryPi.

    Enter diskN like disk2 or disk3 in /dev/diskN to burn it.
    """
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
    run(['diskutil', 'unmountDisk', disk_name])


def insert_settings(network_insert):
    """Fill settings network_insert in template."""
    ...


def insert_dir():
    """Insert file path to save."""
    ...


if __name__ == "__main__":
    """Run it as main."""
    print('RUN sd_config')
    create_files = input(f'Create files Y[n]: ')
    if create_files == 'Y':
        insert_settings()
        insert_dir()
    else:
        x = input('Enter a disk number or let it run/search for it\n')
        if x == '':
            setup_sd()
        else:
            # x = 'disk' + x
            setup_sd(set_disk=x)
        # print(choose_image())
        # print(BOOT_VOLUME_PATH)
