"""Inspect a LOCAL SSH profile without connecting, installing or making keys."""
import argparse
import subprocess
from pathlib import Path
parser=argparse.ArgumentParser()
parser.add_argument('config',type=Path)
args=parser.parse_args()
result=subprocess.run(['ssh','-G','-F',str(args.config.resolve()),'jetson'],check=True,capture_output=True,text=True)
wanted={'hostname','user','identityfile','identitiesonly','serveraliveinterval','serveralivecountmax'}
for line in result.stdout.splitlines():
    if line.split(' ',1)[0] in wanted: print(line)
print('Configuration only: no connection was attempted.')
