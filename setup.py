from setuptools import setup

setup(
    name='nginx_log_stats',
    version='1.0.0',
    packages=['nginx_log_stats'],
    install_requires=[
        # List your script's dependencies here
    ],
    entry_points={
        'console_scripts': [
            'ngxav = nginx_log_stats.nginx_log_stats:main',
        ],
    },
)
