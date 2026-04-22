from setuptools import find_packages
from setuptools import setup

setup(
    name='human_hand_msgs',
    version='0.1.0',
    packages=find_packages(
        include=('human_hand_msgs', 'human_hand_msgs.*')),
)
