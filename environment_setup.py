"""Set up the environment.

update, upgrade,
"""
from subprocess import Popen, PIPE  # , run
import pi_data

# add a check if .bash_aliases eexist and python alread has an alias
# run(['echo', '"python=python3"', '> .bash_aliases'])
p = Popen('sudo -S apt-get install tree',
          shell=True,
          stdin=PIPE,
          stdout=PIPE
          )
p.communicate('{}'.format(pi_data.pw, 'b'))

# run(['rm', pi_data.py])
