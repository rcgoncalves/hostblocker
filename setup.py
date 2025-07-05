from setuptools import setup, find_packages


setup(
    name='HostBlocker',
    version='2.1.1',
    description='Host file domain blocker builder',
    author='Rui Carlos Goncalves',
    author_email='rcgoncalves.pt@gmail.com',
    url='https://rcgoncalves.pt/project/hostblocker/',
    license='GPL v3',
    packages=find_packages(exclude=['tests']),
    entry_points={'console_scripts': ['hostblocker = hostblocker.main:main']},
    install_requires=['PyYAML', 'coverage'],
)
