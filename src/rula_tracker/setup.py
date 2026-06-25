from setuptools import find_packages, setup

package_name = 'rula_tracker'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools', 'mediapipe', 'opencv-python', 'numpy'],
    zip_safe=True,
    maintainer='duy',
    maintainer_email='duy@todo.todo',
    description='RULA score tracking using RealSense and MediaPipe',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'rula_tracker_node = rula_tracker.rula_tracker_node:main',
        ],
    },
    package_data={
        'rula_tracker': ['model/*.task'],
    },
    include_package_data=True,
)
