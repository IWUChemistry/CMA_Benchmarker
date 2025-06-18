from os import path
import glob
import os
import sys
import numpy as np
import re
import shutil
import subprocess
def parse_xyz_from_output(filepath='output.dat'):
    coordinates = []
    found_final_geometry_block = False
    capture = False
    waiting_for_coordinates = False

    with open(filepath, 'r') as file:
        coords_to_paste = ""
        for line in file:
            stripped = line.strip()

            if "Final optimized geometry and variables" in stripped:
                print("✅ Found geometry block header.")
                found_final_geometry_block = True
                continue

            if found_final_geometry_block and "Geometry (in Bohr)" in stripped:
                print(f"✅ Found geometry start line: {stripped}")
                waiting_for_coordinates = True
                continue

            # Skip empty lines between header and coordinates
            if waiting_for_coordinates and not stripped:
                continue

            if waiting_for_coordinates:
                print("▶️ Starting coordinate capture")
                capture = True
                waiting_for_coordinates = False  # Reset trigger

            if capture:
                print(f"📦 Capturing line: {repr(stripped)}")
                if not stripped or 'FINDIF' in stripped or re.match(r'^-+$', stripped):
                    print("⛔ End of coordinate block.")
                    break

                parts = stripped.split()
                if len(parts) == 4 and re.match(r'^[A-Z][a-z]?$', parts[0]):
                    try:
                        x, y, z = map(float, parts[1:])
                        coordinates.append((parts[0], x, y, z))
                        coords_to_paste += repr(stripped)
                        coords_to_paste += "\n"
                    except ValueError:
                        print(f"⚠️ Could not parse floats in: {stripped}")
                else:
                    print(f"⚠️ Skipped unexpected line: {stripped}")

    print(f"✅ Finished parsing: {len(coordinates)} atoms found.")
    #print("coords to paste")
    #print(coords_to_paste)
    return coordinates, coords_to_paste

def create_zmat_file(coordinates):
    #zmat_path = os.path.join(dir_path, "zmat")
    
    with open("zmat_red", 'w') as f:
        f.write("ZMAT begin\n")
        f.write("ZMAT end\n")
        f.write("\n")
        f.write("cart begin\n")
        for line in coordinates.strip().splitlines():
            f.write(line.strip().strip("'") + "\n")
        #f.write(coordinates.strip())
        f.write("cart end\n")
    with open("zmat", 'w') as f:
        f.write("ZMAT begin\n")
        f.write("ZMAT end\n")
        f.write("\n")
        f.write("cart begin\n")
        for line in coordinates.strip().splitlines():
            f.write(line.strip().strip("'") + "\n")
        #f.write(coordinates.strip())
        f.write("cart end\n")

raw_data_path = '/nfs/sisyphus/shared/amino_acid_coords'
#AA = '/Alanine'
AA = '/Asparagine'
#ts_name = '10_Alanine'
ts_name = '12_Asparagine'
#exclude_list = ["xaz"]
exclude_list = []
h_theory = "B3LYP_6-311G**"

#make job list for SINGLE amino acid
job_list = glob.glob(raw_data_path + AA + "/opt/*")
#filter job list for exclusions
if len(exclude_list):
    excludee_list = []
    for job in exclude_list:
        excludee_list += glob.glob(raw_data_path + AA + "/opt/" + job)
    for path in excludee_list:
        job_list.remove(path)

#process job list
#sort them alphabetically
job_list = sorted(job_list)
#iterate through the job list
os.chdir(ts_name)
print(os.getcwd())
for j , jobb in enumerate(job_list):
    j +=1
    print(f"the jobb {j} {jobb}")
    try:
        print(os.path.basename(jobb))
        #subdir
        AA_conformer = str(j) + '_' + os.path.basename(jobb)
        os.mkdir(AA_conformer)
        os.chdir(AA_conformer)
        #make Level A directory for zmat and fc.dat
        h_theory = h_theory.strip("'\"")
        os.mkdir(h_theory)
        os.chdir(h_theory)
        
        #create zmat file
        coords, coords_to_paste = parse_xyz_from_output(os.path.join(jobb, "output.dat"))
        create_zmat_file(coords_to_paste)

        #copy in level A force constants
        hessfile = glob.glob(jobb + "/*.hess")[0]
        print("hessfile")
        print(hessfile)
        #destination = os.getcwd() + "fc.dat" 
        destination = os.path.join(os.getcwd(), "fc.dat")
        print("destination")
        print(destination)
       
        shutil.copyfile(hessfile, destination)
        
    except Exception as e:
        print(f"⚠️ Skipping {subdir}: {e}")
    os.chdir("../../")
    #print(stop)

