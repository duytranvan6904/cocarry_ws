from setuptools import find_packages, setup

package_name = 'kinect_tracker'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/models', ['models/pose_landmarker_full.task']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='duy',
    maintainer_email='tranvanduy6904@gmail.com',
    description='Kinect V2 Tracking Package',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'kinect_node = kinect_tracker.kinect_node:main'
        ],
    },
)
