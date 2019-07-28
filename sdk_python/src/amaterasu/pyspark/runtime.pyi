from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession, DataFrame

from amaterasu.base import runtime
from amaterasu.pyspark.datasets import DatasetManager


class AmaContextBuilder(runtime.BaseAmaContextBuilder):

    spark_conf = ... # type: SparkConf

    def setMaster(self, master_uri) -> "AmaContextBuilder": ...

    def set(self, key, value) -> "AmaContextBuilder": ...

    def prepare_user_dependencies(self): ...

    def build(self) -> "AmaContext": ...


class AmaContext(runtime.LoaderAmaContext):

    @classmethod
    def builder(cls) -> AmaContextBuilder: ...

    @property
    def dataset_manager(self) -> DatasetManager: ...

    @property
    def sc(self) -> SparkContext: ...

    @property
    def spark(self) -> SparkSession: ...

    def get_dataset(self, dataset_name: str) -> DataFrame: ...

    def persist(self, dataset_name: str, dataset: DataFrame, overwrite: bool = True): ...
