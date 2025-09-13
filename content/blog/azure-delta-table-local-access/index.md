---
title: "Securely Accessing Delta Tables on Azure from Local Machines"
date: 2024-08-18T16:00:00+03:00
draft: true
tags: [Azure, DevOps, Data Engineering, Data Science, Python]
---

[Delta Tables](https://docs.delta.io/latest/index.html) have emerged as a powerful tool for managing large datasets with ACID transactions on affordable cloud storage, which enables building a Lakehouse architecture on top of data lakes.

While initially developed by Databricks for Apache Spark, Delta Lake is now open-sourced and widely used across various platforms. The rust-based [delta-rs](https://delta-io.github.io/delta-rs/) engine further expands their usability as it enables interaction with Delta Tables using Python, without the overhead of Spark.

While Delta Tables offer impressive performance and scalability, managing secure access to these tables when located in cloud storage presents Data and DevOps Engineers with a challenge. While it is possible to access the tables with connection strings, this poses a significant security risk as they can easily be shared and exposed, leading to unauthorized data access. When using Azure Entra ID, access to resources can be controlled at one central location.

While using managed identities is quite common to grant other Azure resources access to storage accounts (see e.g. [this Microsoft tutorial](https://learn.microsoft.com/en-us/azure/azure-functions/functions-identity-based-connections-tutorial) which describes how to use managed identity in a Function App to access other Azure resources), I had issues to connect to the storage account from a Jupyter Notebook on my MacBook which is a common tool of a Data Scientist.

In the following article, I describe how we can use Azure Entra ID identification to access Delta Tables located in Azure Storage.


## Accessing Delta Tables with delta-rs



## IAM roles



## How to get a token

