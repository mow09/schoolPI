from subprocess import Popen
from subprocess import PIPE
from subprocess import run
# p = Popen('sudo -S apt-get update',
#          shell=True,
#          stdin=PIPE,
#          stdout=PIPE
#          )
# p.communicate(b'raspberry\n')
# p = Popen('sudo -S apt-get upgrade',
#          shell=True,
#          stdin=PIPE,
#          stdout=PIPE
#          )
# p.communicate(b'raspberry\n')
run(['bash', 'bash_stuff.sh'])
