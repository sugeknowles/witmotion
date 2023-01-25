from setuptools import setup

setup(name='witble',
      version='0.1',
      description='Wit-Motion BLE Sensor Library',
      url='http://github.com/sugeknowles/witble',
      author='Chris Knowles',
      author_email='chris@alexanderaiden.com',
      license='closed',
      packages=['witble'],
      install_requires=['bleak'],
      zip_safe=False)