from setuptools import setup, find_packages

setup(
      name='mcgtextension',
      version='1.0',
      packages=find_packages(),
      install_requires=['markdown>=3.0'],
      package_data={'mcgtable': ['*.lua']}
)
