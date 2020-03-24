"""
School configuration.

This file contains everything you need to set up a nice raspberry pi.
Lightweighted...
"""
import sd_config
from subprocess import Popen, PIPE, run


"""Absolut path."""
"""
# in ~/. a.k.a users home

# check if python3 exist and ist python3.7
subprocess
echo 'alias python=python3' >> ~/.bash_aliases
sudo apt-get update
sudo apt-get upgrade - y
"""

"""
https://www.raspberryconnect.com/raspbian-packages
Educational Packages:
https://www.raspberryconnect.com/raspbian-packages/32-raspbian-educational

---
https://raspberrytips.com/best-apps-raspberry-pi/
https://raspberrytips.com/upgrade-raspbian-lite-to-desktop/

---
"""

"""
usb ssh:
ssh user@host_name.local
openssh needed
"""

# pi_data.py:
user_pw = b'raspberry\n'
user_na = 'pi'

imps = [
    'from subprocess import Popen',
    'from subprocess import PIPE',
]


def make_sudo_popen(executer: str, sudo_pw: str = user_pw):
    """Get the popen template."""
    return [
        "p = Popen('sudo -S apt-get {}',".format(executer),
        "          shell=True,",
        "          stdin=PIPE,",
        "          stdout=PIPE",
        "          )",
        "p.communicate({})".format(sudo_pw)
    ]


def os_config():
    """Set up the operations system."""
    p = Popen('sudo -S apt-get update',
              shell=True,
              stdin=PIPE,
              stdout=PIPE
              )
    p.communicate(user_pw)


def config_remote():
    """Create a python file to set up the remote environment."""
    with open('remote_school_setup.py', 'w') as f:
        [f.write(imp+'\n') for imp in imps]
        [f.write(line + '\n') for line in make_sudo_popen('update')]
        [f.write(line + '\n') for line in make_sudo_popen('upgrade')]

        # def system_connect_execute(executer_file: str = "", executer: str = 'python'):
        # def system_connect_execute(executer: str = '', ip_adress: str = ''):
    run(['cat', 'remote_school_setup.py'])


def get_pi_ip():
    """Get the IP.

    get_pi_ip() runs arp -a and returns IP of rasyberrypi.
    """
    p = run(['arp', '-a'], stdout=PIPE, encoding='utf-8')
    for each in p.stdout.split('\n'):
        if each.split(' ')[0] == 'raspberrypi':
            return (each.split(' ')[1][1:-1])
        else:
            raise 'NO Pi-iP-Adress found...'


def system_connect_execute(ip_adress: str = ''):
    """
    Connect to the system via ssh.

    Password has to be typed in by hand.
    Executes a python file if set.
    """
    print('Get the IP adress')
    if not ip_adress:
        pi_adress = get_pi_ip()
    else:
        pi_adress = ip_adress

    print("\n")
    print('Copy this in a new Terminal line...')
    print("\n\n\tssh {}@{} 'python3' < remote_school_setup.py"
          .format(user_na, pi_adress))
    print('\n\t\t...and hit ENTER')
    print("\n")
    """After this enter user password of remote machine."""


if __name__ == "__main__":
    """Run it as main."""
    # N = input('Enter the N of diskN')
    print('RUN')
    # ssd_config.setup_ssd(f'disk{N}')
    # system_connect_execute(executer_file='test_file.sh', executer='bash')
    # system_connect_execute()
    config_remote()
    system_connect_execute(ip_adress='192.168.1.73')
