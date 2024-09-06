---
title: "Autoloader in Databricks Delta Live Tables"
date: 2022-10-18T20:11:00+02:00
draft: false
tags: [Apache Spark, Databricks]
---

Recently, we had the following challenge:
* Data should be retrieved by REST-request in regular time intervals
* The data (simple json-response) should be ingested into the data lake
* The files should then be further processed.

Our solution was the following:
* Write a python script to perform the requests. The script should persist the response as separate json-files into the data lake.
* Schedule this script using Databricks jobs.
* As a second task of this multi-task job, trigger a Delta Live Tables pipeline.

The Delta Live Table pipeline should start using the Autoloader capability. Autoloader keeps track of which files are new within the data lake and only processes new files. Internally this is handled using Event Hubs but you don't need to care for details because this is all hidden from you.

Let's have a look at an Autoloader example:

```python
import dlt
from pyspark.sql import functions as F

@dlt.table(
    name="table_name",
    path="/mnt/datalake/02_silver/table.delta",
    partition_cols=["country", "city"],
)
def ingested_data():
    return (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "json")
        .option(
            "cloudFiles.schemaHints",
            "ratingAverage float, ratingsDistribution array<int>, votesTotal int, country string, city string",
        )
        .option("cloudFiles.schemaEvolutionMode", "rescue")
        .load(f"/mnt/datalake/01_bronze/raw-data/")
        .withColumn("file_name", F.input_file_name())
    )
```

This returns a Spark Streaming object that can then be used like other streaming objects, for example data coming from an Event Hub.

Let's have a look at the details:
* Within the `dlt.table-decorator`, you define the name of the table in the Hive-story, the path where the delta-table will be persisted and possibly partitioning columns.
* The format "cloudFiles" and the "cloudFiles.format"-option mark the Autoloader and define the input data format, here json.
* The "schemaHints"-option can be used to predefine the expected schema of the input data, using [DDL Schema String](../spark-ddl-schema).
* There are several options for schema evolution, i.e. how to handle cases where the schema changes over time. In the case of "rescue", additional fields are collected in an additional "_rescue"-column.
* In the last row, we add a column that contains the file name. In our case, this was done because the filename contained additional data that was extracted in the following steps.
