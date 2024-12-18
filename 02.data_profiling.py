from ydata_profiling import ProfileReport
from pyspark.sql import SparkSession

spark = (
    SparkSession.builder().master("local[1]").appName("SparkProfiling").getOrCreate()
)


def profiling_spark_df(spark, filename):
    df = spark.read.csv(f"{filename}.csv")

    df.printSchema()

    a = ProfileReport(df, title=f"Profiling Report: {filename}")
    a.to_file(f"profiles/{filename}.html")


profiling_spark_df(spark, filename="user_metadata_sample")
profiling_spark_df(spark, filename="user_interactions_sample")
