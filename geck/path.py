import os

from geck.builder import step
from geck.run import Status

@step
def cd(path):
    result = {'status': Status.ok}
    try:
        os.chdir(path)
    except Exception as e:
        result['status'] = Status.error
        result['error'] = e
    return result

