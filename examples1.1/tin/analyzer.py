import argparse, json
import sys, subprocess, os.path
import numpy as np

# Set up Parser
parser = argparse.ArgumentParser(description="Returns acceptance ratio of run")
parser.add_argument('default', type=str, help='default .vmc filename')
parser.add_argument('metropolis', type=str, help='metropolis .vmc filename')
args = parser.parse_args()

# Check files exist
checkFiles = os.path.exists(args.default + '.log') & os.path.exists(args.default + '.o') & os.path.exists(args.metropolis + '.log') & os.path.exists(args.metropolis + '.o')
if checkFiles == 0:
    print "log and output files do not exist, please refer to help"

# Run grep and gosling to find statistics
grepProcDefault = subprocess.Popen("grep 'accept' " + args.default + '.o', shell=True, stdout=subprocess.PIPE)
grepProcMetro = subprocess.Popen("grep 'accept' " + args.metropolis + '.o', shell=True, stdout=subprocess.PIPE)
goslingProcDefault = subprocess.Popen("gosling -json " + args.default + '.log', shell=True, stdout=subprocess.PIPE)
goslingProcMetro = subprocess.Popen("gosling -json " + args.metropolis + '.log', shell=True, stdout=subprocess.PIPE)
grepResultDefault = grepProcDefault.stdout.read()
grepResultMetro = grepProcMetro.stdout.read()
goslingResultDefault = goslingProcDefault.stdout.read()
goslingResultMetro = goslingProcMetro.stdout.read()
goslingJSONDefault = json.loads(goslingResultDefault)
goslingJSONMetro = json.loads(goslingResultMetro)

# Find average acceptance
def isFloat(string):
    try:
        float(string)
        return True
    except ValueError:
        return False
acceptValsAvg = np.average(np.array([float(s) for s in grepResultDefault.split() if isFloat(s) and float(s) <= 1]))
acceptValsMetroAvg = np.average(np.array([float(s) for s in grepResultMetro.split() if isFloat(s) and float(s) <= 1]))

#for key, val in goslingJSONMetro.iteritems():
#    print key, val
# Find difference and error
totalEnergyDiff = float(goslingJSONMetro['properties']['total_energy']['value'][0]) - float(goslingJSONDefault['properties']['total_energy']['value'][0])
totalEnergyDiffError = (float(goslingJSONMetro['properties']['total_energy']['error'][0])**2.0 + float(goslingJSONDefault['properties']['total_energy']['error'][0])**2.0)**(1/2.0)

# Print Gosling stats
print 'Gosling Stats for ' + args.default + ': independent points: ' + str(goslingJSONDefault['independent points']) + ' total blocks: ' + str(goslingJSONDefault['total blocks'])
print 'Gosling Stats for ' + args.metropolis + ': independent points: ' + str(goslingJSONMetro['independent points']) + ' total blocks: ' + str(goslingJSONMetro['total blocks'])

print 'Total_energy difference: ' + str(totalEnergyDiff) + ' +/- ' + str(totalEnergyDiffError)
print "Average Acceptance for " + args.default + ': ' + str(acceptValsAvg)
print "Average Acceptance for " + args.metropolis + ': ' + str(acceptValsMetroAvg)
