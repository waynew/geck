'''
GECK self-build script.
'''
if __name__ == '__main__':
    import sys
    print(f'No - run this with GECK. geck builder {__file__} run', file=sys.stderr)
    sys.exit(1)


import geck

build = geck.builder.Build(root='~/build/metageck')
build.add_step(geck.git.clone('~/programming/geck'))
# TODO: I'd really like to make this a context manager, but I think that requires some refactoring of how things run -W. Werner, 2019-03-01
build.add_step(geck.py.makevenv())
build.add_step(geck.path.cd('geck'))
build.add_step(geck.cmd.run(['../env/bin/python', '-m', 'pip', 'install', '.[build,test]']))
build.add_step(geck.path.cd('..'))
build.add_step(geck.cmd.run(['env/bin/pytest', '--junit-xml', '../test-results.xml', 'geck/tests']))
build.add_step(geck.py.build_wheel(python='env/bin/python', setup='geck/setup.py'))
#build.add_step(geck.py.twine_upload())
