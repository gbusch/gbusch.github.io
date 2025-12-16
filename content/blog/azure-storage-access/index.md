---
title: "Let third-party access your Azure Storage Account"
date: 2025-12-16T20:34:12+01:00
draft: false
tags: [Azure, RBAC, storage]
---

## Problem

A third-party needs to ingest data into a specific Azure Storage container but must be restricted from accessing any other containers or resources within the subscription. They still require enough visibility to locate the Storage Account and the container in the Azure Portal to confirm file uploads.

## Solution: Control and data plane RBAC

To solve this, roles must be assigned at two different scopes: the Storage Container (for data access) and the Storage Account (for portal visibility).

1. Data Plane Access (Read/Write Data)

Assign the `Storage Blob Data Contributor` role.

- Scope: The specific container only.

- Purpose: Allows reading, writing, and deleting blobs (data operations). This is all that is strictly required for programmatic file transfer.

2. Control Plane Access (Portal View)

Assign the `Reader` role.

- Scope: The Storage Account resource.

- Purpose: This control-plane permission is required for the user to view the Storage Account resource itself within the Azure Portal. Without it, the resource cannot be found or navigated to.

- Result: The user will see the Storage Account and a list of all containers, but they will only be able to view the contents and perform data operations on the container where they were granted the more restrictive Data Contributor role.

## Verification via Azure CLI

To verify that the permissions work with the user's Microsoft Entra ID (Azure AD) identity:

```bash
# Ensure a file named test-upload.txt exists locally before running this command.
az storage blob upload \
  --account-name <storage-account-name> \
  --container-name <container-name> \
  --name test-upload.txt \
  --file test-upload.txt \
  --auth-mode login
```

## Automation Best Practices

For automated ingestion processes (where a user is not logging in interactively):

- Service Principals: Use these for external applications or scripts running outside of Azure.

- Managed Identities: If the ingestion job runs on an Azure resource (e.g., Azure VM, Azure Function, Azure Container App), assign the Storage Blob Data Contributor role directly to that resource's Managed Identity.
