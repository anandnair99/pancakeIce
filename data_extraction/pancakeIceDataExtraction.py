# Simulation data extraction ver 2+txt.export
import numpy as np
from pathlib import Path
import pandas as pd
import re

## Data extraction ##
# Open log file for reading
file = 'pancakeIceEllipse1.out'
with open(file, 'r') as logfile:
    lines = logfile.readlines()

# Initialize lists
time = []
deltaT = []

processing = False

# Iterate over log file to get list of time points
for line in lines:
    words = line.split()
    if "deltaT" in words:
        deltaT.append(float(words[-1]))
        processing = True
    elif processing:
        time.append(float(words[-1]))
        processing = False

# Initialize data lists
lin_velocity = []
ang_velocity = []

# Iterate over log file to get velocities
for line in lines:
    words = line.split()
    if "Linear" in words:
        lin_velocity.append(words)

    elif "Angular" in words:
        ang_velocity.append(words)
        continue

# Funtion to determine max PIMPLE iterations
# def maxIter(lines):
#     max_iter = 1
#     iter_pattern = re.compile(r"PIMPLE: iteration (\d+)")

#     for line in lines:
#         match = iter_pattern.search(line)
#         if match:
#             max_iter = max(max_iter, int(match.group(1)))

#     return max_iter

# nIter = maxIter(lines)

# Close log file
logfile.close()


## Data processing ##
# Cleaning up linear and angular velocity lists
ang = np.array(ang_velocity)
ang = np.delete(ang, [0,1], axis=1)
ang[:,0] = [x.lstrip('(') for x in ang[:,0].tolist()]
ang[:,2] = [x.rstrip(')') for x in ang[:,2].tolist()]
ang_velocity = ang.astype(float)

lin = np.array(lin_velocity)
lin = np.delete(lin, [0,1], axis=1)
lin[:,0] = [x.lstrip('(') for x in lin[:,0].tolist()]
lin[:,2] = [x.rstrip(')') for x in lin[:,2].tolist()]
lin_velocity = lin.astype(float)


# Integration function to determine displacements
def integrate(time,velocity):
    pos = 0
    t0 = 0
    v0 = 0
    out = [ ]
    for t,v in zip(time,velocity):
        deltaT = t - t0
        pos += deltaT * v0
        out.append(pos)
        t0 = t
        v0 = v
    return out


# Translations
v_x = lin_velocity[:,0]
v_y = lin_velocity[:,1]
v_z = lin_velocity[:,2]

# Remove extra PIMPLE iterations from list
# v_x = v_x[0::nIter]
# v_y = v_y[0::nIter]
# v_z = v_z[0::nIter]

x  = integrate(time,v_x)
y  = integrate(time,v_y)
z  = integrate(time,v_z)

# Rotations
omega_x = ang_velocity[:,0]
omega_y = ang_velocity[:,1]
omega_z = ang_velocity[:,2]

# Remove extra PIMPLE iterations from list
# omega_x = omega_x[0::nIter]
# omega_y = omega_y[0::nIter]
# omega_z = omega_z[0::nIter]

phi = integrate(time,omega_x)
theta = integrate(time,omega_y)
psi = integrate(time,omega_z)


## Data storage ##
#Save data into csv
SimData = pd.DataFrame(np.column_stack((time,x,y,z,v_x,v_y,v_z,phi,theta,psi,omega_x,omega_y,omega_z)), 
                      columns=['time','x','y','z','v_x','v_y','v_z','phi','theta','psi','omega_x','omega_y','omega_z'])

filename = Path(file).stem
SimData.to_csv(filename[10:]+'.txt')

# Prepend txt file with 0 to align columns
with open(filename[10:]+'.txt', 'r') as file:
    lines = file.readlines()
    lines[0] = "0" + lines[0]
with open(filename[10:]+'.txt', 'w') as file:
    file.writelines(lines)

print("//// Extraction Complete ////")