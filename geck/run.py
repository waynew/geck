from enum import Enum


class Status(Enum):
    ok = 'ok'
    queued = 'queued'
    paused = 'paused'
    running = 'running'
    failed = 'failed'
    aborted = 'aborted'
    error = 'error'

    @property
    def is_bad(self):
        return self in (Status.failed, Status.aborted, Status.error)
