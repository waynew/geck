import pathlib

import geck.cmd

from geck.builder import step
from geck.run import Status
# TODO: We want other useful bits like identity files & whatnot here -W. Werner, 2019-02-26
@step
def clone(repo):
    if repo.startswith('~'):
        repo = str(pathlib.Path(repo).expanduser())
    result = geck.cmd.run(['git', 'clone', repo]).run()
    if result['status'] is not Status.ok:
        print('ERROR', result['stdout'], result['stderr'])
    return result
