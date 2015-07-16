import multiprocessing
from setuptools import setup, find_packages

setup(
    name='postman-mock-server',
    version='0.0.1',
    description='A simple utility to serve responses saved in a Postman Collection',
    url='https://github.com/czardoz/postman-mock-server',
    author='Aniket Panse',
    author_email='aniketpanse@gmail.com',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=open('requirements.txt').readlines(),
    test_suite='nose.collector',
    long_description=open('README.rst').read(),
    tests_require=['nose'],
    scripts=['bin/pmock']
)
