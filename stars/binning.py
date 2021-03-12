##!/usr/bin/python3

#bin_size = {
#    'x_size': [100],
#    'y_size': [100],
#    'z_size': [100],
#    'KE_size': [100], # This is actually going to be sqrt(KE)
#    }
# Top-level objects/locations only: A system or fleet is only one object for scanning.
# That means "false" KE/mass bins went away.

# bin locations are defined in reference to (0,0,0) not scanner's location
# bins are labeled by division floor so (-1,0,0,1) NOT (-100,0,0,50) 
# def _bin_search(location, penetrating, normal)

# Penetrating scanners have a defined range.  Anti-cloak scanners could be the same algorithm just other bins.
# Normal scanners always start their range at scanner location regardless of penetrating range
#"""bounding box"""
#if bin.x >= int((location.x - penetrating) / x_size) and bin.x <= int((location.x + penetrating) / x_size)
#and if bin.y >= int((location.y - penetrating) / y_size) and bin.y <= int((location.y + penetrating) / y_size)
#and if bin.z >= int((location.z - penetrating) / z_size) and bin.z <= int((location.z + penetrating) / z_size)



# First determine whether the player has the whole bin under penetrating scan, before doing any distance comparisons per object.
# Penetrating scanners only need to check the 0 KE bins.
#for scanner
#    my_binx = int(location.x / x_size)
#    my_biny = int(location.y / y_size)
#    my_binz = int(location.z / z_size)
#    __bins_penetrating(my_binx, my_biny, my_binz)

#"""take a penetrating scanner
#in what bin is it? does it fully cover that bin?  
#If no, next scanner"""
#bin.x == my_binx
#bin.y == my_biny
#bin.z == my_binz

#"""If the farthest corner of the bin is in range, I get the whole bin."""

# for each scanner of the player, what bins are fully covered?
#d_x = max(abs(location.x - (x_size * bin.x)), abs(location.x - (x_size * (1 + bin.x)))) 
#d_y = max(abs(location.y - (x_size * bin.y)), abs(location.y - (y_size * (1 + bin.y))))
#d_z = max(abs(location.z - (z_size * bin.z)), abs(location.z - (z_size * (1 + bin.z))))
#if penetrating >= sqrt((d_x)^2 + (d_y)^2 + (d_z)^2)
#and if bin.KE = 0
# then move the bin to "fully covered"
# take the next bin in that scanner's bounding-box that isn't already on the player's fully-scanned-bins list
# repeat for the next bin

#"""makes the KE-based scanner bounding box"""
#d_x = min(abs(location.x - (x_size * bin.x)), abs(location.x - (x_size * (1 + bin.x))))
#d_y = min(abs(location.y - (x_size * bin.y)), abs(location.y - (y_size * (1 + bin.y)))) 
#d_z = min(abs(location.z - (z_size * bin.z)), abs(location.z - (z_size * (1 + bin.z))))
#if bin.KE >= KE_size * sqrt((d.x)^2 + (d.y)^2 + (d.z)^2) / normal

#"""If the farthest corner of the bin is in range for its KE, I get the whole bin."""
#for each normal scanner of the player, what bins are fully covered?
#d_x = max(abs(location.x - (x_size * bin.x)), abs(location.x - (x_size * (1 + bin.x)))) 
#d_y = max(abs(location.y - (x_size * bin.y)), abs(location.y - (y_size * (1 + bin.y))))
#d_z = max(abs(location.z - (z_size * bin.z)), abs(location.z - (z_size * (1 + bin.z))))
#if bin.KE >= KE_size * sqrt((d_x)^2 + (d_y)^2 + (d_z)^2) / normal
#then the bin is fully covered

# then check objects in the non-fully-scanned bins for range
#    for target in bin
#        if target.KE >= 1000 * sqrt((location.x - target.location.x)^2 + (location.y - target.location.y)^2 + (location.z - target.location.z)^2) / normal
# then it's scanned

#"""OLD"""
#"""makes the box and trims it down"""
#for a penetrating scanner
#d_x = min(abs(location.x - (x_size * bin.x)), abs(location.x - (x_size * (1 + bin.x))))
#d_y = min(abs(location.y - (x_size * bin.y)), abs(location.y - (y_size * (1 + bin.y)))) 
#d_z = min(abs(location.z - (z_size * bin.z)), abs(location.z - (z_size * (1 + bin.z))))
#if penetrating >= d.x and penetrating >= d.y and penetrating >= d.z
#and if penetrating >= sqrt((d_x)^2 + (d_y)^2 + (d_z)^2)
#and if bin.mass = "false" or bin.mass = 0
# then check objects in the bin for range
#    for target in bin
#        if penetrating >= sqrt((location.x - target.location.x)^2 + (location.y - target.location.y)^2 + (location.z - target.location.z)^2)
# then it's scanned

