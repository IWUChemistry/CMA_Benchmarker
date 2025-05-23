from os import path
import glob
import os
import sys
import numpy as np
import re
import shutil
import subprocess

paths = ['/1*','/2*']
#levelA = "CCSD_T_TZ"
levelA = "B3LYP_6-31G_2df,p_"

levelB = "GFN"

make_all = True #False if testing code
#job_list = ["1.59"]

hq = os.getcwd()
jobb_list = []
path_ind = []

def insert_templates(jobb_list):
    for j, job in enumerate(jobb_list):
        dir_to_insert_temp = os.path.join(job, "/Disps_", levelB)
        levelB_direc = "/Disps_" + levelB
        destination = job + levelA +  levelB_direc + "/templateInit.dat" 
        shutil.copyfile(os.getcwd() + "/templateInit.dat", destination)
        print(f"Has the template file been copied in? {os.path.exists(destination)}")

def delete_Disps_dir(jobb_list):
    for j, job in enumerate(jobb_list):
        levelB_direc = "/Disps_" + levelB
        dir_to_delete = job + levelA +  levelB_direc
        if os.path.exists(dir_to_delete):
            print(f"The path exists to delete")
            shutil.rmtree(dir_to_delete)
        else:
            print("the path doesn't exist... can't delete it")
        print(f"Does the directory exist now? {os.path.exists(dir_to_delete)}")
def make_Disps_dir(jobb_list):
    for j, job in enumerate(jobb_list):
        print(f"the job {job}")
        levelB_direc = "/Disps_" + levelB
        dir_to_make = job + levelA +  levelB_direc
        print(f"the dir to make {dir_to_make}")
        os.mkdir(dir_to_make)
        print(f"Does the directory exist now? {os.path.exists(dir_to_make)}")
        #os.chdir(dir_to_make)
        #print(os.getcwd())




if make_all:
    for path in paths:
        path_ind.append(len(jobb_list))
        tmp_list = glob.glob(hq + path + "/[1-9]*_*/")
        ind = np.argsort(np.array([int(re.search(r"/\d_.*/(\d*)_.*", name).group(1)) for name in tmp_list]))
        tmp_list = [tmp_list[i] for i in ind]
        jobb_list += tmp_list
    make_Disps_dir(jobb_list)
    insert_templates(jobb_list)
    #delete_Disps_dir(jobb_list)
else:
    for job in job_list:
        id1, id2 = job.split(".")
        jobb_list += glob.glob(hq + f"/{id1}_*" + f"/{id2}_*/")
    make_Disps_dir(jobb_list)
    insert_templates(jobb_list)
    #delete_Disps_dir(jobb_list)
