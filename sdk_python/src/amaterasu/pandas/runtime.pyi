from amaterasu.base import BaseAmaContextBuilder, LoaderAmaContext, BaseDatasetManager


class AmaContextBuilder(BaseAmaContextBuilder):

    def build(self) -> "AmaContext": ...


class AmaContext(LoaderAmaContext):

    @property
    def dataset_manager(self) -> BaseDatasetManager: ...

    @classmethod
    def builder(cls) -> AmaContextBuilder: ...