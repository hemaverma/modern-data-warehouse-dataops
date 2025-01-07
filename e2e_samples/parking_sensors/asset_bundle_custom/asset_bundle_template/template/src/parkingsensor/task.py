import pyspark
from pyspark.sql import SparkSession

spark = SparkSession.builder.master('local[*]').appName('example').getOrCreate()

print(f'Spark version{spark.version}')