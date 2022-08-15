---
title: "Backup Azure Storage Accounts"
date: 2022-08-02T19:04:32+02:00
draft: true
---

While regular backups of data came a bit out of fashion in the modern cloud world, there might be situations where you have to generate a copy of your data from a storage account. In my case, the customer required me to enable infrastructure-encryption of storage accounts which forces a resource recreation. So the question was how to backup the data before and then migrate it back to the new resources.

The solution is a bit hacky but works quite well: Create a temporary backup storage account, copy your data there, recreate the actual storage account, and then copy the data back. Here, I will explain how to do that using azcopy.

1. Create a backup account. While the rest of my setup is handled with terraform as infrastructure as Code (IaC), I did this manually in the Azure UI, as it is just temporary. It makes sense to choose the same settings as for the storage account that you want to backup.

2. Download azcopy (https://docs.microsoft.com/en-us/azure/storage/common/storage-use-azcopy-v10) and unpack it.

3. Login to your Azure account in the command line. You can do that with `./azcopy login` which will lead you to a so-called device-login (meaning you should open a link in the browser, enter a alphanumeric code and then proceed with the normal Azure login). You might also need to choose the correct subscription in case you have several: `az account set --subscription <subscription_id>`.

