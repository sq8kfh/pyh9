from setuptools import setup, find_packages
from codecs import open


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='h9',
    version='0.0.0',
    author='Kamil Palkowski',
    author_email='sq8kfh@gmail.com',
    description='h9 utils library',
    long_description=long_description,
    url='https://github.com/sq8kfh/pyh9',
    license='MIT',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        "Operating System :: OS Independent",
    ],
    keywords='h9',
    python_requires='>=3.5',
    install_requires=[
        'lxml',
    ],
    test_suite='tests',
)
