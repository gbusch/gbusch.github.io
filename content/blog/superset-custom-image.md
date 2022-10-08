---
title: "Superset Custom Docker Image"
date: 2022-10-08T15:00:00+02:00
draft: false
tags: [Data Visualization, Apache Superset]
---

[Apache Superset](https://superset.apache.org) is a great open-source visualization and dashboarding tool that can be connected to a multitude of data sources. For many of those data sources, additional drivers/packages need to be installed. 

But how to do that when using the default Docker-image? Also: how can we easily change superset-configurations. This is possible with a very simple custom Docker image.

1. Create a custom "Dockerfile":
    ```
    FROM apache/superset:2.0.0

    USER root

    RUN pip install duckdb-engine

    COPY ./start.sh /start.sh

    COPY superset_config.py /app/
    ENV SUPERSET_CONFIG_PATH /app/superset_config.py

    USER superset
    ENTRYPOINT [ "/start.sh" ]
    ```
    This Dockerfile builds on top of the default Superset-image. Using the root-account, we install additional packages, here duckdb-engine because I want to connect to DuckDB ([see here for other connections](https://superset.apache.org/docs/databases/installing-database-drivers)).

    Then we copy the start-script (see 2.) and the superset-config (see 3.) Finally, we switch back to the non-root user, as is best practice, and set the start-script as entrypoint.

2. Create a start-script `start.sh`. It is important that you make this file executable with `chmod +x start.sh`.
    ```
    #!/bin/bash

    superset fab create-admin --username admin --firstname Superset --lastname Admin --email admin@superset.com --password "admin"

    superset db upgrade

    superset init

    echo "Starting server"
    /bin/sh -c /usr/bin/run-server.sh
    ```
    This script creates an admin user "admin" with password "admin" (change accordingly and add other users with `superset fab create-user`). Then the database is upgraded and initialized. Finally the server is started.

    This script can also be used to create roles at start-up.

3. Create a superset-config-file `superset_config.py`. Find [here](https://github.com/apache/superset/blob/master/superset/config.py) the original config-file from where you can get an idea of which configs can be set and modified.
    ```
    FEATURE_FLAGS = {
        "ENABLE_TEMPLATE_PROCESSING": True,
    }

    def square(x):
        return x**2
    
    JINJA_CONTEXT_ADDONS = {
        'my_crazy_macro': square
    }
    ```
    This config is just an example. As you can see, this file can also be used to define functions that can be used as jinja-templates in the SQL-editor.

    Also, we can define custom auth here (article to follow).

4. Build the Docker-image with `docker build -f Dockerfile -t superset .` and run with `docker run -p 8088:8088 superset`.
   