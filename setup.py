from setuptools import setup, find_packages
from codecs import open

import tortv_on_demand

with open('requirements.txt') as f:
    requirements = f.read().splitlines()


setup(
    name='tortv_on_demand',
    version=tortv_on_demand.version,
    description='tortv_on_demand.',
    url='https://github.com/louisoutin/tortv_on_demand',
    author='Outin',
    author_email='none@mail.com',
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=requirements,
    include_package_data=True,
    package_data={'': ['templates/*.png']},
    entry_points={
        'console_scripts': [
            'tortv=tortv_on_demand.cli:run_main',
        ],
    },
)
