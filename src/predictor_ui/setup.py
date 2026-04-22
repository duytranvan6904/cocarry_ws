from setuptools import setup
package_name = 'predictor_ui'
setup(
    name=package_name, version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Duy', maintainer_email='duy@experiment.local',
    description='PyQt5 real-time dashboard for trajectory prediction',
    license='MIT',
    entry_points={
        'console_scripts': [
            'ui_node = predictor_ui.ui_node:main',
        ],
    },
)
