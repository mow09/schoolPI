"""
School configuration.

This file contains everything you need to set up a nice raspberry pi.
Lightweighted...
"""
import ssd_config
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


def os_config():
    """Set up the operations system."""
    p = run(['arp', '-a'], stdout=PIPE, encoding='utf-8')
    for each in p.stdout.split('\n'):
        if each.split(' ')[0] == 'raspberrypi':
            pi_adress = (each.split(' ')[1][1:-1])

    user_pw = b'raspberry\n'
    user_na = 'pi'
    p = Popen(['ssh', '{}@{}'.format(user_na, pi_adress)], stdin=PIPE)
    p.communicate(user_pw)

    proc = Popen('sudo -S apt-get update',
                 shell=True,
                 stdin=PIPE,
                 stdout=PIPE
                 )
    proc.communicate(user_pw)


if __name__ == "__main__":
    """Run it as main."""
    # N = input('Enter the N of diskN')
    print('RUN')
    # ssd_config.setup_ssd(f'disk{N}')
    os_config()
