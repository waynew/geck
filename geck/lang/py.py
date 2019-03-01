import geck.cmd

from pathlib import Path

from geck.builder import step
from geck.run import Status
# TODO: We want other useful bits like identity files & whatnot here -W. Werner, 2019-02-26
@step
def makevenv(python='python'):
    result = geck.cmd.run([python, '-m', 'venv', 'env']).run()
    if result['status'] is not Status.ok:
        print('ERROR', result['stdout'], result['stderr'])
    return result

@step
def build_wheel(python='python', setup='setup.py'):
    result = geck.cmd.run([python, setup, 'bdist_wheel']).run()
    if result['status'] is Status.ok:
        for row in result['stdout'].split('\n'):
            if row.startswith("creating 'dist/"):
                result['wheel'] = Path(row.split()[1].strip("'"))
