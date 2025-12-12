---
title: "Databricks Workspace Migration: Seeding a New Streaming Pipeline from Old Bronze Data"
date: 2025-12-12T12:35:00+01:00
draft: false
tags: [Azure, Databricks, pyspark, Delta Lake]
---

## Problem: Retaining State During Workspace Migration

Recently, I was asked to move an Azure Databricks workspace to a new subscription. As direct migration is not supported, creating a new workspace is generally required. Since I had used *Infrastructure as Code (IaC)* to set up the Azure infrastructure and *Databricks Asset Bundles (DAB)* to set up the Databricks assets, this was relatively easy to do.

However, while DAB handles table creation, the new environment starts with an empty state. If the pipeline relies on processing historical messages from an Event Hub (persisted in an old Bronze Delta table), simply rerunning the new pipeline will cause it to miss all prior events unless the Event Hub retention is sufficient, which is often not the case. We need to initialize the new Bronze table with the historical data from the old workspace.


## Solution: Cross-Catalog Append for Stream Initialization

The solution leverages the ability to read tables across different Workspaces, assuming the executing user has `SELECT` permissions on both catalogs:

1. Initialize Tables: Deploy and run the new pipeline once. This action creates the empty Bronze, Silver, and Gold Delta tables in the new workspace's catalog schema.

2. Copy Bronze Data: Use a PySpark notebook on a cluster in the new workspace to read the entire historical Bronze table from the old catalog and append it to the newly created, empty Bronze table.

```python
# Assuming both the old and new catalogs are accessible and the user has SELECT permission.
# Replace 'old_catalog' and 'new_catalog' with your actual catalog names.
# Here it is assumed that the schema name is the same for old and new workspace,
# otherwise adjust accordingly

print("Reading data from old workspace/catalog...")
df = spark.read.table("old_catalog.raw_data.bronze_raw_events")

print(f"Read {df.count()} rows. Appending to new bronze table...")
df.write \
    .format("delta") \
    .mode("append") \
    .saveAsTable("new_catalog.raw_data.bronze_raw_events")

print("Append complete. Rerun the streaming pipeline.")
```

3. Final Pipeline Run: Rerun the streaming pipeline. The pipeline will read the appended data, stream it through the Silver layers, and materialize the Gold views, effectively synchronizing the data state.

*Note*: Order is important! I also tried to first copy the data into the new catalog and then run the pipeline. This does not work because the pipeline tries to create the table on its first run - but cannot as it already exists.