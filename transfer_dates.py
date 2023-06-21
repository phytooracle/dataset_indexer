#!/usr/bin/env python3
"""
Author : Jeffrey Demieville, Devin Bayly
Date   : 2023-06-20
Purpose: Iterates over tar files within a directory, downloads them with iRODS, and runs sbatch_indexer.sh on each archive. This should be ran on the HPC filexfer node.
"""

import os
import sys
import argparse
import subprocess as sp


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='transfer_dates',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-p',
                        '--path',
                        help='path containing postprocessed data to index',
                        type=str,
                        required=True)
                        # Example: /iplant/home/shared/phytooracle/season_15_lettuce_yr_2022/level_2/scanner3DTop/lettuce/
      
    parser.add_argument('-s',
                        '--ssh',
                        help='ssh account to log in to hpc',
                        type=str,
                        required=True)
                        # Example: jdemieville@junonia.hpc.arizona.edu
        
    parser.add_argument('-i',
                        '--indexer',
                        help='path to sbatch_indexer.sh on user xdisk',
                        type=str,
                        required=True)
                        # Example: /xdisk/dukepauli/jdemieville/dataset_indexer/sbatch_indexer.sh
                        
    return parser.parse_args()
  
  
#-------------------------------------------------------------------------------
def get_file_list(data_path):
    '''
    List all files in path
    
    Input:
        - data_path: path to the input data on CyVerse data store
    Output: 
        - List of files contained within data_path
    '''
    result = sp.run(f'ils {data_path}', stdout=sp.PIPE, shell=True)
    files = result.stdout.decode('utf-8').split('\n')

    return files

  
#-------------------------------------------------------------------------------
def download_tar(path_to_archive):
    '''
    Download tar files
    
    Input:
        - path_to_archive: path to the tar data on CyVerse data store
    Output: 
        - Downloaded tar file
    '''
    result = sp.run(f'iget -PT {path_to_archive} ./', stdout=sp.PIPE, shell=True)
    
    return result

  
#-------------------------------------------------------------------------------
def run_indexer(path_to_archive, ssh_account, sbatch_indexer):
    '''
    Index tar files
    
    Input:
        - path_to_archive: path to the tar data on CyVerse data store
        - ssh_account: account to use for ssh to HPC
        - sbatch_indexer: path to sbatch indexer shell script
    Output: 
        - Tar file index
    '''
    #split path_to_archive to get last entry
    archive = path_to_archive.split('/')[-1]
    result = sp.run(f"ssh -t {ssh_account} '. /usr/local/bin/slurm-selector.sh elgato;sbatch {sbatch_indexer} {archive}'", stdout=sp.PIPE, shell=True)
    
    return result
    

#-------------------------------------------------------------------------------
def upload_index(index_file, path_to_archive):
    '''
    Uploads index files
    
    Input:
        - index_file: path to local index file
        - path_to_archive: path to the tar data on CyVerse data store
    Output: 
        - Uploaded index file
    '''
    archive_list = path_to_archive.split('/')[:-1]
    destination = ('/').join(archive_list)
    result = sp.run(f'iput -PT {index_file} {destination}', stdout=sp.PIPE, shell=True)
    
    return result


#-------------------------------------------------------------------------------
def main():
    print("get scan dates")
    dates = get_file_list(args.path)
    print("scan dates: ", dates)
    
    # Iterate through all dates within this season
    for scan in dates:
        print("get file list")
        filelist = get_file_list(scan + '/individual_plants_out/')
        print("filelist: ", filelist)
        for filename in filelist:
            print("check for index")
            #Create index if not present in /individual_plants_out/
            if filename.endswith("segmentation_pointclouds_index"):
                print("Index found. Continuing.")
                continue
            else:
                print("No index found.")
                if filename.endswith("_segmentation_pointclouds.tar"):
                    path_to_archive = (scan + '/individual_plants_out/' + filename.lstrip())[5:]
                    print("path to archive: ", path_to_archive)
                    print("downloading tar")
                    download_tar(path_to_archive)
                    print("Archive downloaded. Running indexer.")
                    index = run_indexer(path_to_archive, args.ssh, args.indexer)
                    print("Indexing complete. Uploading data.")
                    upload_index(index, path_to_archive)
                    print("Uploading data complete.")
                    #may need to use this one if the filename is not the output of run_indexer
                    #upload_index([(filename.lstrip()[5:]).split('segmentation_pointclouds')[0]+"segmentation_pointclouds_index"], path_to_archive)
                else:
                    print("No archive found. Continuing.")
                    continue
        print("Scan complete. Beginning next scan.")
    print("All dates complete.")    


# --------------------------------------------------
if __name__ == '__main__':

    main()
