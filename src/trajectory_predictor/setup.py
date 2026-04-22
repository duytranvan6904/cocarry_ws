from setuptools import setup
package_name = 'trajectory_predictor'
setup(
    name=package_name, version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/config', ['config/predictor_params.yaml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Duy', maintainer_email='duy@experiment.local',
    description='ML inference node for hand trajectory prediction',
    license='MIT',
    entry_points={
        'console_scripts': [
            'predictor_node = trajectory_predictor.predictor_node:main',
        ],
    },
)
