
# from subprocess import Popen
from subprocess import PIPE, STDOUT
from subprocess import run
import pi_data
# import os
from sd_setup import wait_for


def get_pi_ip():
    """Get the IP.

    get_pi_ip() runs arp -a and returns IP of rasyberrypi.
    """
    p = run(['arp', '-a'], stdout=PIPE, stderr=STDOUT, encoding='utf-8')
    for each in p.stdout.split('\n'):
        # print(each)
        if each.split(' ')[0] == 'raspberrypi':
            return (each.split(' ')[1][1:-1])

# TODO: NOT NEEDED ANYMORE !! YEA
# def first_connection(ip_adress):
#     """Connect to the Raspberry Pi for the first time.
#
#     Except key fingerprint with entering 'yes'.
#     """
#     with open('.bash_first_excess.sh', 'w') as f:
#         f.write('ssh pi@{}'.format(ip_adress)+'\n')
#
#     print('\n\n\tJust enter yes!\n\n')
#
#     run(['bash', '.bash_first_excess.sh'], shell=False)
#     run(['rm', '.bash_first_excess.sh'], shell=False)
#
#     # p = run(['bash', '.bash_first_excess.sh'], shell=False,
#     #         stdout=PIPE,  # stdout=open('comp_info.txt', 'w'),bufsize=4096,
#     #         stderr=PIPE, encoding='utf-8')
#     # stdout, stderr = p.communicate()
#     # print('the err:', p.stderr)
#     # print('the out:', p.stdout)


ask_ip_connection = [
    "\n\n\tRaspberry is ON?? Micro SD is set up?\n\n",
    "\n\n\tMaybe disconnect and connect the RaspberryPi from powersupply?\n\n",
    "\n\tCheck everything around the RaspberryPi.\n",
]


def connect_to_pi():
    """Connect to the Pi.

    ...
    """
    counter = 0
    waiter = 3
    ip_adress = ''
    while not ip_adress:
        ip_adress = get_pi_ip()
        if counter > 0:
            wait_for('No RaspberryPi IP-adress found...', waiter)
        counter += 1
        if counter == 45:
            wait_for('Program will stop!', waiter)
            print(ask_ip_connection[2])
            raise "NO RASPBERRY IP FOUND"
        elif counter % 20 == 0:
            print(ask_ip_connection[1])
        elif counter % 10 == 0:
            print(ask_ip_connection[0])

    environment_update = [
        'update',
        'upgrade -y',
    ]
    environment_install = [
        'tree',
        'xfce4 -y'  # xfce4-all',
        'xfce4-goodies -y'
    ]
    environment_install_2 = [
        'arc-theme -y',
        # 'arc-icons'
    ]
    environment_remove = [
        "lxappearance",
        "lxde",
        "lxde-*",
        "lxinput",
        "lxmenu-data",
        "lxpanel",
        "lxpolkit",
        "lxrandr",
        "lxsession*",
        "lxsession",
        "lxshortcut",
        "lxtask",
        "lxterminal",
    ]


"""
    scp data/plus/minecraft-pi-0.1.1.tar pi@192.168.1.85:Desktop/.
"""
   with open('bash_environment.sh', 'w') as f:
        for each in environment_update:
            f.write('sudo apt-get '+each+' \n')
        for each in environment_install:
            f.write('sudo apt-get install '+each+' \n')
        # choose between three
        # f.write('sudo update-alternatives --config x-session-manager' + ' \n')
        for each in environment_install_2:
            f.write('sudo apt-get install '+each+' \n')
        # f.write('sudo apt-get remove '+' '.join(environment_remove)+' \n')
        # f.write('sudo apt-get install ' + 'pistore' + ' \n')
        # f.write('sudo autoremove '+' \n')
        # f.write('sudo autoclean '+' \n')
        f.write('sudo reboot '+'\n')

        # create echo 'python=python3' >> .bash_aliases
        # push pi_data file
    cmd_pyth = 'sshpass -p {} ssh {} {}@{} '.format(
        pi_data.pw,
        pi_data.keyoff,
        pi_data.user,
        ip_adress,

    ) + '"' + pi_data.pyalias + '"'
    cmd_copy = 'sshpass -p {} scp {} ./{} {}@{}:.'.format(
        pi_data.pw,
        pi_data.keyoff,
        pi_data.file_name,
        pi_data.user,
        ip_adress,
    )

    cmd_load = 'sshpass -p {} ssh {} {}@{} {}'.format(
        pi_data.pw,
        pi_data.keyoff,
        pi_data.user,
        ip_adress,
        pi_data.run_script(True),
    )
    cmd_bash = 'sshpass -p {} ssh {} {}@{} {}'.format(
        pi_data.pw,
        pi_data.keyoff,
        pi_data.user,
        ip_adress,
        pi_data.scripter_bash
    )
    # print(cmd_pyth)
    # print(cmd_copy)
    # print(cmd_load)
    print(cmd_bash)
    with open('.bash_pyal.sh', 'w') as f:
        f.write(cmd_pyth+'\n')
    with open('.bash_copy.sh', 'w') as f:
        f.write(cmd_load+'\n')
    with open('.bash_load.sh', 'w') as f:
        f.write(cmd_load+'\n')
    with open('.bash_load_bash.sh', 'w') as f:
        f.write(cmd_load+'\n')
        # f.write('yes'+'\n')
    # run(['bash', '.bash_pyal.sh'], shell=False, stderr=PIPE)
    # run(['bash', '.bash_copy.sh'], shell=False, stderr=PIPE)
    # run(['bash', '.bash_load.sh'], shell=False, stderr=PIPE)
    run(['bash', '.bash_load_bash.sh'], shell=False, stderr=PIPE)

    # run(['rm', '.bash_copy.sh'], shell=False, stderr=PIPE)
    # run(['rm', '.bash_load.sh'], shell=False, stderr=PIPE)
    # print(p.stderr)
    # p = run(['whoami'], stdout=PIPE, encoding='utf-8')
    # print(p.stdout.strip())
    # p = run(['bash', '.bash_excess.sh'],  # shell=False,
    #         stdout=PIPE,  # stdout=open('comp_info.txt', 'w'),bufsize=4096,
    #         stderr=PIPE, encoding='utf-8')
    # stdout, stdoerr = p.communicate()

    # run(['rm', '.bash_excess.sh'])
    # stdout, stderr = p.communicate()
    # print('the err:', p.stderr)
    # print('the out:', p.stdout)

    # p = Popen('bash .bash_first_excess.sh',  shell=True,
    #           stdout=PIPE, stderr=PIPE, encoding='utf-8')

# p = Popen(['bash', '.bash_first_excess.sh'], shell=True,stdin=PIPE)
# p = run(['bash', '.bash_first_excess.sh'], input=b'yes\n')
#    f.write('{}'.format(pi_data.pw)+'\n')
# f.write('sshpass -p {} ssh pi@{}'.format(pi_data.pw, get_pi_ip()))


# p = Popen('sudo -S apt-get update',
#          shell=True,
#          stdin=PIPE,
#          stdout=PIPE
#          )
# p.communicate(b'raspberry\n')

    # p = Popen('sudo -S apt-get upgrade',
    #           shell=True,
    #           stdin=PIPE,
    #           stdout=PIPE
    #           )
    # p.communicate({}.format(pi_data.pw, 'b'))
# run(['rm', '.bash_first_excess.sh'])
# os.system('rm .bash_first_excess.sh')

    run(['ssh-keygen', '-R', '{}'.format(ip_adress)], shell=False)


if __name__ == "__main__":
    connect_to_pi()

"""




sshpass -p raspberry ssh pi@192.168.1.85

ssh -o UserKnownHostsFile=~/.ssh/known_hosts -o StrictHostKeyChecking=no pi@192.168.1.85


sshpass -p raspberry ssh -o UserKnownHostsFile=~/.ssh/known_hosts -o StrictHostKeyChecking=no pi@192.168.1.85

ssh-keygen -R 192.168.1.85


sshpass -p raspberry ssh -o UserKnownHostsFile=~/.ssh/known_hosts -o StrictHostKeyChecking=no pi@192.168.1.85
sshpass -p raspberry ssh -o UserKnownHostsFile=~/.ssh/known_hosts -o StrictHostKeyChecking=no pi@192.168.1.85
"""
