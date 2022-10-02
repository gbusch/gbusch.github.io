---
title: "Read parquet files from Azure Data Lake with Apache Spark"
date: 2022-10-02T20:28:57+02:00
draft: false
tags: [Apache Spark, Azure]
---

Azure Blob Storage - and especially the Datalake Gen 2 which is built on top and allows additional features like hierarchical namespace - is a great place to store data in all kinds of format: a data lake.

Here, I explain how to connect to this data lake with Apache Spark and read in parquet-files from the data lake.

1. Retrieve the access key from the Azure portal. Go to the storage account you want to connect to, choose "Access keys" under "Security + networking" and copy one of the keys.
2. When creating your Spark Session in your application or notebook, you need to add one package that will be automatically downloaded and included in the session:
    ```
    from pyspark.sql import SparkSession

    spark = SparkSession.builder \
        .master("local") \
        .config('spark.jars.packages', 'org.apache.hadoop:hadoop-azure:3.3.1')\
        .getOrCreate()
    ```
3. Hand over the key from (1) to the Spark config. Note that the key allows access to your data and is therefore a secret! You should handle it properly, for example with a local env-file that is not checked into version control, or better something like a key vault.
    ```
    spark.conf.set(
        "fs.azure.account.key.<storage account name>.dfs.core.windows.net",
        "<storage account key>"
    )
    ```
4. You can now read in parquet files:
    ```
    df = spark.read.format("parquet")\
        .load("abfss://<container name>@<storage account name>.dfs.core.windows.net/<file path>")
    ```
    Note that the container name comes before the "@"-sign but does not appear within the file path.
