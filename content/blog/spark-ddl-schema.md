---
title: "Defining Spark Schemas with Strings in DDL"
date: 2022-07-25T20:28:57+02:00
draft: false
tags: [Apache Spark]
---

Defining a schema in Spark can sometimes be tedious and confusing. Also, there are some use cases (for example when writing tests, article TBD) where it is of advantage to define the schema in one string.

Schema definitions as a string follow the idea of the [Data Definition Language](https://en.wikipedia.org/wiki/Data_definition_language). DDL expressions are for example used to create tables in SQL databases:
```sql
CREATE TABLE employees (id INTEGER not null, name VARCHAR(50) not null);
```

Here the expression 
```sql
id INTEGER not null, name VARCHAR(50) not null
```
defines the schema of the table.

This notation can also be used to define schemas in Spark. For example, instead of defining:
```python
from pyspark.sql import types as T

schema = T.StructType(
    [
        T.StructField("id", T.IntegerType(), False),
        T.StructField("name", T.StringType(), True),
    ]             
)
```

you can simply write
```python
schema = "id int not null, name string"
```

To convert the string into an actual schema-object, you can use the following function: `from pyspark.sql.types import _parse_datatype_string`. However, when passing it to the `spark.createDataFrame`-method, this is not needed and you can directly pass the string.

Note that the notation also works for more complicated cases. However, when using nested schemas, you need to add colons between the column name and the data type. For example the following nested schema:
```python
from pyspark.sql import types as T

schema = T.StructType(
    [
        T.StructField("id", T.StringType(), False),
        T.StructField("person", T.ArrayType(
            T.StructType([
                T.StructField("name", T.StringType(), False),
                T.StructField("age", T.IntegerType(), True),
            ])), False),
    ]             
)
```
becomes:
```python
id: int not null, person: array<struct<name: string not null, age: int>>
```