"""
Extend a Profile's CTD data to deeper depths
============================================

Use the TAMOC ambient module to open a Profile object, compute some buoyancy
frequencies and then artificially extend the profile to deeper depths while
maintaining a fixed buoyancy frequency.

Notes
-----
There are any number of ways that CTD data could be artificially extended to
deeper than the measured depths.  This script demonstrates one rational 
method coded in the `ambient.Profile` class and documented in the class 
method `ambient.Profile.extend_profile_deeper().

Requires
--------
This script reads data from a netCDF object already in the format of a 
TAMOC `ambient.Profile` object, stored in the file::

    ./Profiles/Profiles/BM54.nc

If this file is not yet present in your directory structure, it can be 
generated by the `profile_from_ctd` script.  To execute that file, change
directory at the command promt to the `./Profiles` root directory and at the 
IPython prompt execute::

    >>> run profile_from_ctd

Returns
-------
This script generates a new `ambient.Profile` object, whose netCDF file is
written to the file::

    ./Profiles/Profiles/BM54_deeper.nc

"""
# S. Socolofsky, July 2013, Texas A&M University <socolofs@tamu.edu>.

from tamoc import ambient
from tamoc import seawater

import numpy as np
import matplotlib.pyplot as plt
import os

if __name__ == '__main__':
    
    # Get the path to the input file
    __location__ = os.path.realpath(os.path.join(os.getcwd(),
                                    os.path.dirname(__file__), 
                                    '../../test/output'))
    dat_file = os.path.join(__location__,'test_BM54.nc')
    
    # Create a Profile object with this file.
    ctd = ambient.Profile(dat_file, chem_names=['oxygen'])
    
    # Print the buoyancy frequency at a few selected depths
    z = np.array([500., 1000., 1500.])
    N = ctd.buoyancy_frequency(z)
    print 'Buoyancy frequency is: '
    for i in range(len(z)):
        print '    N(%d m) = %g (1/s) ' % (z[i], N[i])
    
    # Plot the potential density profile and corresponding buoyancy frequency
    z_min = ctd.nc.variables['z'].valid_min
    z_max = ctd.nc.variables['z'].valid_max
    z = np.linspace(z_min, z_max, 500)
    ts = ctd.get_values(z, ['temperature', 'salinity'])
    rho = seawater.density(ts[:,0], ts[:,1], 101325.)
    N = ctd.buoyancy_frequency(z)
    fig = plt.figure(1)
    plt.clf()
    ax1 = plt.subplot(121)
    ax1.plot(rho, z)
    ax1.set_xlabel('Potential density, (kg/m^3)')
    ax1.set_ylabel('Depth, (m)')
    ax1.set_ylim([0., 2500.])
    ax1.invert_yaxis()
    ax2 = plt.subplot(122)
    ax2.plot(N, z)
    ax2.set_xlabel('N, (1/s)')
    ax2.set_ylim([0., 2500.])
    ax2.invert_yaxis()
    plt.show()
    
    # Extend the CTD profile to 2500 m
    dat_file = os.path.join(__location__,'BM54_deeper.nc')
    ctd.extend_profile_deeper(2500., dat_file)
    
    # Plot the new potential density and buoyancy frequency profiles
    z_min = ctd.nc.variables['z'].valid_min
    z_max = ctd.nc.variables['z'].valid_max
    z = np.linspace(z_min, z_max, 750)
    ts = ctd.get_values(z, ['temperature', 'salinity'])
    rho = seawater.density(ts[:,0], ts[:,1], 101325.)
    N = ctd.buoyancy_frequency(z)
    fig = plt.figure(2)
    plt.clf()
    ax1 = plt.subplot(121)
    ax1.plot(rho, z)
    ax1.set_xlabel('Potential density, (kg/m^3)')
    ax1.set_ylabel('Depth, (m)')
    ax1.invert_yaxis()
    ax2 = plt.subplot(122)
    ax2.plot(N, z)
    ax2.set_xlabel('N, (1/s)')
    ax2.invert_yaxis()
    plt.show()
    
    ctd.nc.close()

    