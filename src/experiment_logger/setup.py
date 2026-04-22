from setuptools import setup
package_name = 'experiment_logger'
setup(
    name=package_name, version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'], zip_safe=True,
    maintainer='Duy', maintainer_email='duy@experiment.local',
    description='CSV logger for experiment data', license='MIT',
    entry_points={
        'console_scripts': [
            'logger_node = experiment_logger.logger_node:main',
        ],
    },
)
