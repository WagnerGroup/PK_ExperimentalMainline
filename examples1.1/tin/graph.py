from __future__ import division
import argparse, json
import sys, subprocess, os.path
import numpy as np

# Set up Parser
parser = argparse.ArgumentParser(description="Returns acceptance ratio of run")
parser.add_argument('runsDir', type=str, help='path to directory of runs')
args = parser.parse_args()

# Check directory and files exist
if not os.path.exists(args.runsDir) or not os.path.exists(args.runsDir + '/runInformation.json'):
    print "directory or runInformation.json is not present"
    exit()
# Change directory
os.chdir(args.runsDir)

# Extract JSON
infoJSONFile = open('runInformation.json', 'r')
infoJSON = infoJSONFile.read()
infoJSONFile.close()
info = json.loads(infoJSON)

# Plot Data
timestepDefault = []
timestepMetro = []
energyDefault = []
energyMetro = []
energyErrorDefault = []
energyErrorMetro = []
acceptanceDefault = []
acceptanceMetro = []
indPointsDefault = []
indPointsMetro = []
nblockDefault = []
nblockMetro = []

# Extract Data
for algo, runs in info.iteritems():
    for i, runInfo in runs.iteritems():
        grepAcceptProc = subprocess.Popen("grep -oP '(?<=acceptance )[0-9].[0-9]+' " + runInfo['filename'] + '.o', shell=True, stdout=subprocess.PIPE)
        goslingProc = subprocess.Popen("gosling -json " + runInfo['filename'] + '.log', shell=True, stdout=subprocess.PIPE)
        avgAccept = np.average(np.array([float(a) for a in grepAcceptProc.stdout.read().split('\n')[:-1]]))
        gosling = json.loads(goslingProc.stdout.read())
        grepAcceptProc.wait()
        goslingProc.wait()
        if algo == 'default':
            timestepDefault.append(runInfo['timestep'])
            nblockDefault.append(runInfo['nblock'])
            acceptanceDefault.append(avgAccept)
            indPointsDefault.append(gosling['independent points'])
            energyDefault.append(float(gosling['properties']['total_energy']['value'][0]))
            energyErrorDefault.append(gosling['properties']['total_energy']['error'][0])
        elif algo == 'metro':
            timestepMetro.append(runInfo['timestep'])
            nblockMetro.append(runInfo['nblock'])
            acceptanceMetro.append(avgAccept)
            indPointsMetro.append(gosling['independent points'])
            energyMetro.append(float(gosling['properties']['total_energy']['value'][0]))
            energyErrorMetro.append(gosling['properties']['total_energy']['error'][0])

import matplotlib.pyplot as plt
# Plot Energy Diff
energyDiff = np.array(energyMetro) - np.array(energyDefault)
energyDiffStd = np.sqrt(np.array(energyErrorMetro)**2.0 + np.array(energyErrorDefault)**2.0)
fig = plt.figure()
d = fig.add_subplot(1, 1, 1)
d.errorbar(timestepDefault, energyDiff, yerr=energyDiffStd, label='Total Energy Difference', fmt='o')
d.plot([0, 1.1], [0, 0], color='black')
d.plot([0, 1.1], [0.001, 0.001], color='red', label='one millihartree')
d.plot([0, 1.1], [-0.001, -0.001], color='red')
plt.xlabel('timestep')
plt.ylabel('Energy Difference (Ha)')
plt.xlim((0,1.1))
plt.title("Energy Difference vs. timestep")
# Add legend
legend = d.legend(loc='upper right', shadow=True)
# Add frame
frame = legend.get_frame()
frame.set_facecolor('0.90')

# Plot Acceptance
fig = plt.figure()
d = fig.add_subplot(1, 1, 1)
d.plot(timestepDefault, acceptanceDefault, 'ro', label='Default VMC')
d.plot(timestepMetro, acceptanceMetro, 'bo', label='Metropolis VMC')
plt.xlabel('timestep')
plt.ylabel('Acceptance Ratio')
plt.xlim((0,1.1))
plt.title("Acceptance vs. timestep")
# Add legend
legend = d.legend(loc='upper right', shadow=True)
# Add frame
frame = legend.get_frame()
frame.set_facecolor('0.90')

# Plot Acceptance
indPointsPerStepDefault = np.array(indPointsDefault) / (100*np.array(nblockDefault))
indPointsPerStepMetro = np.array(indPointsMetro) / (100*np.array(nblockMetro))
fig = plt.figure()
d = fig.add_subplot(1, 1, 1)
d.plot(timestepDefault, indPointsPerStepDefault, 'ro', label='Default VMC')
d.plot(timestepMetro, indPointsPerStepMetro, 'bo', label='Metropolis VMC')
plt.xlabel('timestep')
plt.ylabel('Independent Points per step')
plt.xlim((0,1.1))
plt.title("Independent Points per step vs. timestep")
# Add legend
legend = d.legend(loc='upper right', shadow=True)
# Add frame
frame = legend.get_frame()
frame.set_facecolor('0.90')
plt.show()
