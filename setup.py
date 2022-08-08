from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")


classifiers = ['Development Status :: 3 - Alpha',
               'Intended Audience :: Developers',
               'Programming Language :: Python',
               'Operating System :: OS Independent',
               'License :: OSI Approved :: MIT License',
               'Natural Language :: English',
               'Programming Language :: Python :: 3.10',
               'Programming Language :: Python :: 3 :: Only']

setup(
    name='Flappy-Bird',
    version='0.1.0',
    url='https://github.com/GreenMachine582/Flappy-Bird',
    description='Flappy Bird Environment',
    license='MIT',
    author='Matthew Johnson',
    author_email='greenchicken1902@gmail.com',
    classifiers=classifiers,
    keywords='flappy-bird-game, environment',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.10, <4',
    install_requires=['pygame >= 2.1.2, <3'],
    include_package_data=True,
)
