from setuptools import setup, find_packages

setup(
    name='newscollector',
    version='0.1',
    packages=find_packages(exclude=['tests*']),
    install_requires=['beautifulsoup4', 'requests', 'selenium', 'tabulate'],
    author='Tamir Shalit',
    author_email='shalit.tamir@gmail.com',
    description='Download, extraction and analysis of data from websites'
)
