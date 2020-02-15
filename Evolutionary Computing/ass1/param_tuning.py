import numpy as np
import subprocess
import os

mutation_probs = np.linspace(0.1, 0.9, 9)
cross_over_probs = np.linspace(0.1, 0.9, 9)

new_env = os.environ.copy()
new_env['DISPLAY'] = ':0'

# For screen dont forget to
# sudo /etc/init.d/screen-cleanup start

# Set: 30 pop 10 gen and cxpb and mutpb are given via sys.args
for mup in mutation_probs:
    for crsp in cross_over_probs:
        proc = subprocess.Popen(["/usr/bin/screen", "-d", "-m", 'python3', 'alg_cx.py', str(mup), str(crsp)], env=new_env)

for mup in mutation_probs:
    proc = subprocess.Popen(["/usr/bin/screen", "-d", "-m", 'python3', 'alg_no_cx.py', str(mup)], env=new_env)
