---
title: "Superset Color Theme"
date: 2022-08-20T22:03:25+02:00
draft: true
tags: [Data Visualization, Apache Superset]
---

[Apache Superset](https://superset.apache.org) is a great open-source visualization and dashboarding tool that can be connected to a multitude of data sources.

In many situations it is required to adapt the layout, for example to match the corporate design.

You can add your own color scheme in the [superset-config](https://github.com/apache/superset/blob/a27f246effbc422d80fb2d6f7c5a7919749fd9e1/superset/config.py#L534). This will, however, only change the color scheme of the typescript-plugins.

There are three other files that have to be changed to adjust the colors in the remaining css-files:
* superset-frontend/src/assets/stylesheets/antd/index.less
* superset-frontend/src/assets/stylesheets/less/variables.less
* (superset-frontend/packages/superset-ui-core/src/style/index.tsx; this file will be overwritten by the data from the config-file)

Unfortunately, unlike the superset-configs, this requires us to rebuild the superset-frontend (automatically done when building a new Docker-image).

![Blue Superset](/blog/superset-color-theme/blue-superset.png)
