import numpy as np
import subprocess
import os

sims = np.arange(0, 10, 1)

new_env = os.environ.copy()
new_env['DISPLAY'] = ':0'

# For screen dont forget to
# sudo /etc/init.d/screen-cleanup start

for sim in sims:
    proc = subprocess.Popen(["/usr/bin/screen", "-d", "-m", 'python3', 'ea.py', str(sim)], env=new_env)
