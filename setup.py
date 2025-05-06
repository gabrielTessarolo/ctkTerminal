from setuptools import setup, find_packages

setup(
    name='ctkTerminal',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'customtkinter>=5.2.0', 
    ],
    author='Gabriel Tessarolo',
    author_email='gabriel.tessarolo.h@gmail.com',
    url='https://github.com/gabrielTessarolo/ctkTerminal',
    description='Um terminal dinâmico e customizável para aplicações em Python com CustomTkinter.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)