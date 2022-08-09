from setuptools import setup, find_packages
import subprocess
import os


def get_version():
    version = (
        subprocess.run(["git", "describe", "--tags"], stdout=subprocess.PIPE)
        .stdout.decode("utf-8")
        .strip()
    )

    # if len(version) > 0 and version[0] == 'v':
    #     version = version[1:]
    if "-" in version:
        x = version.split("-")
        v, i, s = x[0], x[1], x[-1]
        version = v + "+" + i + ".git." + s

    assert "-" not in version
    assert "." in version
    return version


flappy_bird_version = get_version()

assert os.path.isfile("src/version.py")
with open("src/VERSION", "w", encoding="utf-8") as fh:
    fh.write("%s\n" % flappy_bird_version)

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='Flappy-Bird',
    version=flappy_bird_version,
    author='Matthew Johnson',
    author_email='greenchicken1902@gmail.com',
    description='Flappy Bird Environment',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/GreenMachine582/Flappy-Bird',
    packages=find_packages(),
    package_data={'src': ['VERSION']},
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3 :: Only'
    ],
    keywords='flappy-bird-game, environment',
    python_requires='>=3.10, <4',
    entry_points={"gui_scripts": ["flappy_bird = src.flappy_bird:main"]},
    install_requires=['pygame >= 2.1.2, <3'],
)
