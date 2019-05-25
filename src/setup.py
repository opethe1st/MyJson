from setuptools import (
    setup,
    find_packages,
)

setup(
    name='myjson',
    version='0.0.1',
    description="My Json library",
    url='http://github.com/opethe1st/myjson',
    author='Opemipo Ogunkola (Ope)',
    author_email='ogunks900@gmail.com',
    license='MIT',
    packages=find_packages(where=".", exclude=["tests"]),
    zip_safe=False
)
