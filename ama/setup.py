from setuptools import setup, find_packages

setup(
    name='amaterasu',
    version='0.2.0',
    packages=find_packages(),
    url='https://github.com/shintoio/amaterasu',
    license='Apache License 2.0 ',
    author='Apache Amaterasu',
    author_email="dev@amaterasu.incubator.apache.org",
    setup_requires=['wget'],
    description='Apache Amaterasu (Incubating) is an open source, configuration managment and deployment framework for big data pipelines',
    install_requires=['colorama', 'GitPython', 'six', 'PyYAML', 'netifaces', 'multipledispatch', 'docopt', 'paramiko'],
    python_requires='!=3.0.*, !=3.1.*, !=3.2.*, <4',
    entry_points={
        'console_scripts': [
            'ama=amaterasu.__main__:main'
        ]
    },
    include_package_data=True,
    package_data={
        'amaterasu.cli.resources': ['*']
    },
    classifiers= [
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
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Scientific/Engineering'
    ]
)
