#!/bin/bash
#SBATCH --output=indexer.out
#SBATCH --job-name=index_tar
#SBATCH --ntasks=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --nodes=1             
#SBATCH --time=00:15:00   
#SBATCH --partition=standard
#SBATCH --account=dukepauli   
cd /xdisk/dukepauli/jdemieville/dataset_indexer
tarfile=$1
python3 indexer.py $tarfile
rm $tarfile
