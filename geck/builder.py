import os
import runpy
import sys

from functools import wraps
from pathlib import Path

from .run import Status


def next_run_id(root):
    run_id_file = root / 'last-run-id'
    if not run_id_file.exists():
        run_id_file.parent.mkdir(parents=True, exist_ok=True)
        run_id_file.write_text('0')

    with run_id_file.open(mode='r+') as f:
        last_run = int(f.read())
        next_id = last_run+1
        f.seek(0)
        f.truncate()
        f.write(str(next_id))
        return(next_id)


def step(func):
    '''
    Wrap a function, deferring the actual call until later.
    '''
    print(f'Decorating this {func}')
    @wraps(func)
    def outer_wrapper(*args, **kwargs):
        #print(f'Outer {args} and {kwargs}')
        step = Step(func, *args, **kwargs)
        return step
#        @wraps(func)
#        def wrapper():
#            print(f'Calling wrapper now with {args} and {kwargs}')
#            return func(*args, **kwargs)
#        return wrapper

    return outer_wrapper


class Step:
    def __init__(self, func, *args, **kwargs):
        @wraps(func)
        def wrapper():
            #print(f'Calling wrapper now with {args} and {kwargs}')
            return func(*args, **kwargs)
        self.wrapper = wrapper

    def run(self):
        self.result = self.wrapper()
        return self.result

    @property
    def status(self):
        return self.result['status']


class Build:
    def __init__(self, root='.'):
        self.root = Path(root.format(self.__dict__)).expanduser().absolute()
        self.id = next_run_id(self.root)
        self.steps = []

    def run(self):
        self.status = Status.running
        pwd = Path().absolute()
        build_dir = self.root / f'build-{self.id}'
        print(f'ensuring {build_dir} exists')
        build_dir.mkdir(parents=True, exist_ok=True)
        print('changing to ', build_dir)
        os.chdir(build_dir)
        try:
            print(f'I can run in {self.root}!')
            for num, step in enumerate(self.steps):
                print(f'Running step {num}...', end=' ')
                sys.stdout.flush()
                step.run()
                print(step.status.value)
                if step.status.is_bad:
                    self.status = step.status
                    print(step.result)
                    break
            else:
                self.status = Status.ok
        finally:
            print('changing back to ', pwd)
            os.chdir(pwd)
            print(f'Status: {self.status.value}')

    def add_step(self, step):
        self.steps.append(step)


def run(filename):
    job = runpy.run_path(filename)
    job['build'].run()


def build(args):
    '''
    Take a ``Namespace``-like object and if `.action` is queue,
    queue up the build, or if it is 'run', run the build right now.
    '''
    if args.action == 'queue':
        raise NotImplemented('Pull requests welcome! This feature does not yet exist')
    elif args.action == 'run':
        run(args.script)
    else:
        raise NotImplemented(f'Unknown action {args.action}')
