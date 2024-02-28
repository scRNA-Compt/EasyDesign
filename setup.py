"""Setup script for the easyDesign distribution using Distutils.
"""

from setuptools import find_packages
from setuptools import setup

with open("README.md", "r", encoding="utf-8") as f:
  LONG_DESCRIPTION = f.read()

setup(name='easyDesign',
      description='Tools to design guides for diagnostics',
      long_description=LONG_DESCRIPTION,
      long_description_content_type='text/markdown',
      author='Tyvek Zhang',
      author_email='zhangwq@zhejianglab.com',
      maintainer='HeS',
      maintainer_email='hes@zhejianglab.com',
      url="https://github.com/scRNA-Compt/EasyDesign.git",
      version='1.0.0',
      packages=find_packages(),
      package_data={
        "easyDesign": ["models/*/*/*/assets.extra/*", "models/*/*/*/variables/*", "models/*/*/*/*", "models/*/*/*"],
      },
      install_requires=['numpy>=1.16.0,<1.19.0', 'scipy==1.4.1', 'tensorflow==2.3.0', 'fastapi>=0.78.0',
                        'uvicorn>=0.18.1', 'pandas>=1.0.0', 'protobuf<=3.20.3', 'python-multipart>=0.0.6'],
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache-2.0",
        "Operating System :: OS Independent",
      ],
      scripts=[
        'bin/design.py',
        'bin/design_naively.py',
        'bin/analyze_coverage.py',
        'bin/pick_test_targets.py'
      ])
