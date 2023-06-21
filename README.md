# dataset_indexer
This repo adapts code developed by [Devin Bayly](https://github.com/DevinBayly) for use in creating an index of the contents of tar archives stored on the CyVerse datastore.

To use this code:
1. Connect to an interactive node on the HPC.
2. Navigate to your xdisk location
3. Clone the repo and enter it
4. Change permissions on the files (chmod 755 *)
5. Run the transfer_dates.py script:
  `python3 transfer_dates.py -p <path containing post-processed scan directories> -s <ssh account to use for login> -i <path to sbatch_indexer.sh on user xdisk>`

The script will read in all scan dates present in the source path. For each of these, it will check whether a 'segmentation_pointclouds_index' archive is present, indicating that the indexing has already been performed. If not present, it will check whether a 'segmentation_pointclouds.tar' archive is present, and perform the indexing operation. The resulting index will then be uploaded to the same directory as the segmentation pointclouds.
