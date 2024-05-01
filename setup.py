from setuptools import setup

setup(
  name='riprint',
  packages=['riprint'],
  version='1.0.5',
  author='Hampus Hallman',
  author_email='me@hampushallman.com',
  url='https://github.com/Reddan/riprint',
  license='MIT',
  install_requires=[
    'numpy',
    'termcolor'
  ],
  python_requires='~=3.5',
)
