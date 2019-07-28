from abc import ABC
from typing import Dict, Type
from pyspark.sql import SparkSession, DataFrame
from amaterasu.base import datasets


class BaseSparkDatasetLoader(datasets.BaseDatasetLoader, ABC):

    spark = ... # type: SparkSession


class HiveDatasetLoader(BaseSparkDatasetLoader):

    def load_dataset(self) -> DataFrame: ...
    def persist_dataset(self, dataset: DataFrame, overwrite: bool = False): ...


class FileDatasetLoader(BaseSparkDatasetLoader):

    def load_dataset(self) -> DataFrame: ...
    def persist_dataset(self, dataset: DataFrame, overwrite: bool = False): ...


class DatasetManager(datasets.BaseDatasetManager):

    spark = ... # type: SparkSession
    def get_datastore(self, datastore_cls: Type[BaseSparkDatasetLoader], dataset_conf: Dict): ...
