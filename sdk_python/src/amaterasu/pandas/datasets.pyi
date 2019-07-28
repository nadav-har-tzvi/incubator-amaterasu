from typing import Type, Dict

from amaterasu.base import BaseDatasetLoader, BaseDatasetManager
from pandas import DataFrame


class HiveDatasetLoader(BaseDatasetLoader):

    def load_dataset(self) -> DataFrame: ...

    def persist_dataset(self, dataset: DataFrame, overwrite: bool = False, keep_index=False): ...


class _FileCSVDatasetLoader(BaseDatasetLoader):

    def load_dataset(self, *args, **kwargs) -> DataFrame: ...

    def persist_dataset(self, dataset: DataFrame, overwrite: bool): ...


class _FileJSONDatasetLoader(BaseDatasetLoader):

    def load_dataset(self, *args, **kwargs) -> DataFrame: ...

    def persist_dataset(self, dataset: DataFrame, overwrite: bool): ...


class _FileExcelDatasetLoader(BaseDatasetLoader):

    def load_dataset(self, *args, **kwargs) -> DataFrame: ...

    def persist_dataset(self, dataset: DataFrame, overwrite: bool): ...


class _FileParquetDatasetLoader(BaseDatasetLoader):

    def load_dataset(self, *args, **kwargs) -> DataFrame: ...

    def persist_dataset(self, dataset: DataFrame, overwrite: bool): ...


class _FilePickleDatasetLoader(BaseDatasetLoader):

    def load_dataset(self, *args, **kwargs) -> DataFrame: ...

    def persist_dataset(self, dataset: DataFrame, overwrite: bool): ...


class FileDatasetLoader(BaseDatasetLoader):

    def load_dataset(self) -> DataFrame: ...

    def persist_dataset(self, dataset: DataFrame, overwrite: bool): ...


class DatasetManager(BaseDatasetManager):

    def get_datastore(self, datastore_cls: Type[BaseDatasetLoader], dataset_conf: Dict): ...

