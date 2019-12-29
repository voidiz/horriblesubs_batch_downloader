from setuptools import setup

setup(
    name='horriblesubs_batch_downloader',
    version='1.1.0',
    description='A module that fetches magnet links from HorribleSubs and opens them.',
    author='voidiz',
    packages=['horriblesubs_batch_downloader'],
    install_requires=[
        'docopt',
        'requests',
        'beautifulsoup4',
        'lxml',
        'appdirs',
    ],
    entry_points={
        'console_scripts': [
            'hsbd=horriblesubs_batch_downloader.__main__:main'
        ]
    }
)
