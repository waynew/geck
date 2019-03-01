import os
import subprocess

from geck.builder import step
from geck.run import Status

@step
def run(cmd):
    #print('Running command', cmd)
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = {
            'returncode': result.returncode,
            'stderr': result.stderr,
            'stdout': result.stdout,
            'status': Status.ok if result.returncode == 0 else Status.failed,
        }
    except FileNotFoundError as e:
        result = {
            'status': Status.error,
            'error': e,
            'curdir': os.path.abspath(os.path.curdir),
            'stdout': '',
            'stederr': '',
            'returncode': 1,
        }
        print(result)
    return result
