from setuptools import setup, find_packages


# def readme():
#     with open('README.md') as f:
#         return f.read()


setup(name='clientflexflow',
      version='1.4',
      description=' c.delete_wfmasterObj_by_name ',
      #long_description=readme(),
      url='https://gitlab.net.itc/tsp-billing/clientpaperhouse',
      author='Bhujay Kumar Bhatta',
      author_email='bhujay.bhatta@yahoo.com',
      license='Apache Software License',
      packages=find_packages(),
#       package_data={
#         # If any package contains *.     txt or *.rst files, include them:
#         '': ['*.txt', '*.rst', '*.yml'],
#         # And include any *.msg files found in the 'hello' package, too:
#         #'hello': ['*.msg'],
#     },
      include_package_data=True,
      install_requires=[
          'requests==2.20.1',
          'configparser==3.5.0',
          'PyJWT==1.7.0',
          'PyYAML==3.13',
          'cryptography==2.3.1',
             
      ],
#       entry_points = {
#         'console_scripts': ['micros2=micros2client.cli_parser:main',
#                             ],
#         },
      test_suite='nose.collector',
      tests_require=['nose'],

      zip_safe=False)
