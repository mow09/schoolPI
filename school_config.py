"""
School configuration.

This file contains everything you need to set up a nice raspberry pi.
Lightweighted...
"""
import ssd_config

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
ssh mow@mowsome.local
"""


if __name__ == "__main__":
    """Run it as main."""
    print('RUN')
    ssd_config.setup_ssd('disk2')
