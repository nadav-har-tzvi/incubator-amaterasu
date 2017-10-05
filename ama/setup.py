from setuptools import setup, find_packages
from setuptools.command.install import install
from distutils.errors import DistutilsSetupError
from ctypes.util import find_library
from distutils.sysconfig import get_python_lib
import os
import tarfile
import site


from amaterasu.cli import consts


class AmaterasuDistBuildCommand(install):
    """
    Runs the normal installation of setuptools and then downloads and installs Amaterasu and Anaconda distributables
    The Amaterasu distributable is the Scala application that does the heavy lifting.
    We use Anaconda to support PySpark jobs, or actually, any Python based jobs, PySpark is one type.
    """
    VERSION = '0.2.0-incubating'
    user_options = install.user_options + [
        ('skipdl=', None, "Skip downloading dependent files (Amaterasu distributable, Spark, Anaconda), FOR DEVELOPMENT PURPOSES ONLY!")
    ]

    def __init__(self, dist):
        super(AmaterasuDistBuildCommand, self).__init__(dist)
        self.dist_path = None


    def _download_and_extract(self, url, out=None):
        downloaded_dep_path = self._download_dependency(url, out)
        with tarfile.open(downloaded_dep_path) as tar:
            tar.extractall(self.dist_path + '/')

    def _download_dependency(self, url, out=None):
        import wget
        print("Downloading: {}".format(url))
        if not out:
            out = self.dist_path
        filename = wget.download(url, out=out)
        return filename

    def _download_amaterasu_dist(self):
        self._download_and_extract(consts.AMATERASU_URL, out=self.dist_path + '/amaterasu.tar.gz')


    def _download_anaconda_dist(self):
        self._download_dependency(consts.ANACONDA_URL, out=self.dist_path + '/apache-amaterasu-' + self.VERSION + '/dist/')

    def _download_spark(self):
        self._download_dependency(consts.SPARK_URL, out=self.dist_path + '/apache-amaterasu-' + self.VERSION + '/dist/')

    def _validate_os_dependencies(self):
        java_code = os.system('java -version')
        if java_code != 0:
            raise DistutilsSetupError("Java is not installed")

        libffi_exists = find_library('ffi')

        if not libffi_exists:
            raise DistutilsSetupError("libffi is required, please install it and try again")


    def initialize_options(self):
        self.skip_dl = False
        super(AmaterasuDistBuildCommand, self).initialize_options()


    def run(self):
        self._validate_os_dependencies()
        self.dist_path = get_python_lib() + '/amaterasu/process'
        print(self.dist_path)
        os.makedirs(self.dist_path, exist_ok=True)
        # if not self.skip_dl:
        #     self._download_amaterasu_dist()
        #     self._download_spark()
        #     self._download_anaconda_dist()
        super(AmaterasuDistBuildCommand, self).run()



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
    install_requires=['colorama', 'GitPython', 'six', 'PyYAML', 'netifaces', 'multipledispatch', 'docopt'],
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
    cmdclass={
        'install': AmaterasuDistBuildCommand
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
