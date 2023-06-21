import subprocess as sp
from pathlib import Path
import argparse

p= argparse.ArgumentParser()
p.add_argument("tar")

args = p.parse_args()
tarfile = Path(args.tar)
sp.run(f'tar -vRtf "{tarfile}" > "{tarfile.stem}_index"',shell=True)
