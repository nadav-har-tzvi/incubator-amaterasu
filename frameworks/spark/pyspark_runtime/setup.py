"""
 Licensed to the Apache Software Foundation (ASF) under one or more
 contributor license agreements.  See the NOTICE file distributed with
 this work for additional information regarding copyright ownership.
 The ASF licenses this file to You under the Apache License, Version 2.0
 (the "License"); you may not use this file except in compliance with
 the License.  You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""
import os

from setuptools import setup, find_packages

src_path = 'src'


def list_packages():
    for root, _, _ in os.walk(src_path):
        yield '.'.join(os.path.relpath(root, src_path).split(os.path.sep))


packages = list(find_packages()) + list(list_packages())


setup(
    name='amaterasu_pyspark',
    version='0.2.0-incubating-rc4',
    packages=packages,
    package_dir={'': src_path},
    url='https://github.com/apache/incubator-amaterasu',
    license='Apache License 2.0 ',
    author='Apache Amaterasu (incubating)',
    author_email="dev@amaterasu.incubator.apache.org",
    description='Apache Amaterasu (incubating) is an open source, configuration managment and deployment framework for big data pipelines',
    python_requires='>=3.4.*, <4',
    install_requires=['amaterasu-sdk==0.2.0-incubating-rc4', 'pyspark==2.2.1'],
    test_requires=['virtualenv'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Java',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Scientific/Engineering'
    ]
)