from setuptools import setup
import os
from glob import glob

package_name = 'coord_transform'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
        (os.path.join('share', package_name, 'scripts'), glob('scripts/*.py')),
    ],
    install_requires=['setuptools', 'numpy', 'scipy'],
    zip_safe=True,
    maintainer='Duy Tran',
    maintainer_email='duy@example.com',
    description='Coordinate transform for HRC co-carrying',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'transform_node = coord_transform.transform_node:main',
        ],
    },
)
