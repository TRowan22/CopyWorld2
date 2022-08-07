from setuptools import setup

setup(
    name='copy-world',
    py_modules=['copyworld'],
    install_requires=[],
    entry_points='''
        [console_scripts]
        copyworld=copyworld2:main
    '''
)