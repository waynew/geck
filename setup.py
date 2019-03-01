from setuptools import setup, find_packages


tests_require = [
    'pytest',
    'hypothesis',
]
setup(
    name='geck',
    version='0.0.0dev1',
    author='Wayne Werner',
    author_email='waynejwerner@gmail.com',
    url='https://github.com/waynew/geck',
    packages=find_packages(),
    entry_points='''
    [console_scripts]
    geck=geck.__main__:run
    ''',
    tests_require=tests_require,
    extras_require={
        'test': tests_require,
        'build': ['wheel'],
    },
)
