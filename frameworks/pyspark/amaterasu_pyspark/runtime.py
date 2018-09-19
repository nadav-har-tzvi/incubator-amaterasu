from amaterasu import env, notifier, ImproperlyConfiguredError, BaseAmaContext
from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession, DataFrame


class AmaContext(BaseAmaContext):

    def __init__(self):
        super(AmaContext, self).__init__()
        try:
            master = env.master
        except AttributeError:
            raise ImproperlyConfiguredError("No SPARK_MASTER environment variable was defined!")
        else:
            conf = SparkConf().setAppName(env.name).setMaster(master)
            self.sc = SparkContext.getOrCreate(conf)
            self.spark = SparkSession(self.sc)

    def get_dataset(self, action_name, dataset_name, format="parquet"):
        return self.spark.read.format(format).load(str(
            env.workingDir) + "/" + env.name + "/" + action_name + "/" + dataset_name)

    def persist(self, action_name, dataset_name, dataset, format='parquet', overwrite=True):
        """
        Persists a dataset to the chosen storage backend.
        :param action_name: The name as described in the maki.yaml
        :param dataset_name: The requested export name
        :param dataset: The PySpark Dataset itself.
        :param format: JSON, Parquet, etc.
        :type action_name: str
        :type dataset_name: str
        :type dataset: DataFrame
        :type format: str
        :return:
        """
        if dataset_name in env.exports:
            format = env.exports[dataset_name]

        writer = dataset.write.format(format)
        if overwrite:
            writer = writer.mode('overwrite')
        writer.save(
            env.workingDir + "/" + env.jobId + "/" + action_name + "/" + dataset_name)


ama_context = AmaContext()