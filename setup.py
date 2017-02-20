from setuptools import setup, find_packages


setup(
    name='geck',
    version='0.0.0',
    author='Wayne Werner',
    author_email='waynejwerner@gmail.com',
    url='https://github.com/waynew/geck',
    packages=find_packages(),
    entry_points='''
    [console_scripts]
    geck=geck.__main__:run
    ''',
)
