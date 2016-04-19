from __future__ import division
import argparse, json
import sys, subprocess, os.path
import numpy as np

# Set up Parser
parser = argparse.ArgumentParser(description="Run Default and Metropolis QWalk at various timesteps")
parser.add_argument('low', type=float, help='lower bound timestep')
parser.add_argument('high', type=float, help='upper bound timestep')
parser.add_argument('steps', type=int, help='number of steps')
parser.add_argument('nblocks', type=int, help='nblocks for each run')
args = parser.parse_args()

# Check files exist
checkFiles = os.path.exists('qw_0.threebody.opt.wfout')
checkNum = (args.low > 0) & (args.high > 0) & (args.steps > 2)
if checkFiles == 0 and checkNum == 1:
    print "qw_0.threebody.opt.wfout file do not exist, please refer to help"
# Create directory
if os.path.exists('./timestepRuns') != 1:
    subprocess.call("mkdir timestepRuns", shell=True)
if os.path.exists('./timestepRuns/Default') != 1:
    subprocess.call("mkdir timestepRuns/Default", shell=True)
if os.path.exists('./timestepRuns/Metro') != 1:
    subprocess.call("mkdir timestepRuns/Metro", shell=True)

# Get Variables
high = args.high
low = args.low
steps = args.steps
nblocks = args.nblocks
stepsize = (high - low)/(steps - 1)

defaultcmd = ''
metrocmd = ''
# Generate VMC files
for i in range(steps):
    timestep = low + i*(high-low)/(steps - 1)
    defaultVMC = open('qw_0DefaultTimestep%0.2f.vmc' % timestep, 'w')
    defaultVMC.write("method { VMC timestep %0.2f nblock %d }\ninclude qw_0.sys\ntrialfunc { include qw_0.threebody.opt.wfout }" % (timestep, nblocks))
    metroVMC = open('qw_0MetroTimestep%0.2f.vmc' % timestep, 'w')
    metroVMC.write("method { VMC dynamics { METRO } timestep %0.2f nblock %d }\ninclude qw_0.sys\ntrialfunc { include qw_0.threebody.opt.wfout }" % (timestep, nblocks))
    defaultVMC.close()
    metroVMC.close()
    defaultcmd += 'qwalk qw_0DefaultTimestep%0.2f.vmc; ' % timestep
    metrocmd += 'qwalk qw_0MetroTimestep%0.2f.vmc; ' % timestep

procDefault = subprocess.Popen(defaultcmd, shell=True, stdout=subprocess.PIPE)
procMetro = subprocess.Popen(metrocmd, shell=True, stdout=subprocess.PIPE)
procDefault.wait()
procMetro.wait()
subprocess.call('mv qw_0Default* ./timestepRuns/Default', shell=True)
subprocess.call('mv qw_0Metro* ./timestepRuns/Metro', shell=True)
