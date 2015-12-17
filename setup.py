from setuptools import setup, find_packages

# import sys

version = '0.0.1'

setup(
    name='wrflow',
    description='Applications workflow manager, scheduler',
    version=version,
    packages=find_packages(exclude=['tests/*']),
    include_package_data=True,
    zip_safe=False,
    # scripts=['scripts/bin/wrflow'],
    install_requires=[
        'cherrypy',
        'sqlalchemy',
        'pyhocon',
    ],
    entry_points={
        'console_scripts': [
            'wrctl = wrflow.scripts:main',
        ]
    },
    author='Andrey Proskurnev',
    author_email='andrey@proskurnev.ru',
    url='https://github.com/ariloulaleelay/wrflow',
    download_url=('https://github.com/ariloulaleelay/wrflow/tarball/' + version),
)
