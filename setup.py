from setuptools import setup, find_packages
import sys
import unittest
import coverage.cmdline
import os.path
import glob
import xml.etree.ElementTree


def test_suite() -> unittest.TestSuite:
    """
    Builds a test suite with all tests.

    :return: the test suite with all tests.
    """
    test_loader = unittest.TestLoader()
    suite = test_loader.discover('tests', pattern='test_*.py')
    return suite


# Support for 'coverage' command: runs tests and outputs code coverage
if sys.argv[-1] == 'coverage':
    try:
        packages = ','.join(find_packages())
        work_dir = os.path.dirname(os.path.abspath(__file__))
        test_files = glob.glob(work_dir + '/tests/test_*')
        for file in test_files:
            argv = ['run',
                    '--append',
                    '--source=' + packages,
                    file,
                    ]
            coverage.cmdline.main(argv)
        coverage.cmdline.main(["xml", "-o", ".coverage.xml", "--ignore-errors"])
        root = xml.etree.ElementTree.parse('.coverage.xml').getroot()
        print('----------------------------------------------------------------------')
        print('COVERAGE')
        for package in root.iter('package'):
            cov = float(package.attrib['line-rate']) * 100
            pack_name = package.attrib['name']
            print('{:60s} {:8.2f}%'.format(pack_name, cov))
            for file in package.iter('class'):
                cov = float(file.attrib['line-rate']) * 100
                print('{:60s} {:8.2f}%'.format(pack_name + '.' + file.attrib['name'], cov))
        cov = float(root.attrib['line-rate']) * 100
        print('{:60s} {:8.2f}%'.format('GLOBAL', cov))
    finally:
        # Clean tmp file
        if os.path.exists('.coverage'):
            os.remove('.coverage')
        if os.path.exists('.coverage.xml'):
            os.remove('.coverage.xml')
    sys.exit(0)


setup(
    name='HostBlocker',
    version='1.1',
    description='Host file domain blocker builder',
    author='Rui Carlos Goncalves',
    author_email='rcgoncalves.pt@gmail.com',
    url='https://rcgoncalves.pt/project/hostblocker/',
    license='GPL v3',
    packages=find_packages(exclude=['tests']),
    entry_points={'console_scripts': ['hostblocker = hostblocker.main:main']},
    test_suite='setup.test_suite',
    install_requires=['PyYAML', 'coverage'],
)
