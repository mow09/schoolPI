"""Data for Raspberry Pi config."""
user = 'pi'
pw = 'raspberry'
keyoff = '-o UserKnownHostsFile=~/.ssh/known_hosts -o StrictHostKeyChecking=no'
keyon = ''
scripter = "'python -s' < environment_setup.py"
scripter_bash = "'bash -s' < bash_environment.sh"
# scripter = "'pwd'"  # -s' < test_file.py"

pyalias = "echo 'alias python=python3' > .bash_aliases"

file_name = "pi_data.py"


def run_script(run: bool = False):
    """Run a script if wished."""
    if run:
        return scripter
    else:
        return ''
