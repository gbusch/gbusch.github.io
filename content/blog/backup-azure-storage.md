---
title: "Backup Azure Storage Accounts"
date: 2022-08-20T13:00:00+02:00
draft: false
tags: [DevOps, Azure]
---

While regular backups of data came a bit out of fashion in the modern cloud world, there might be situations where you have to generate a copy of your data from a storage account. In my case, the customer required me to enable infrastructure-encryption of storage accounts which forces a resource recreation. So the question was how to backup the data before and then migrate it back to the new resources.

The solution is a bit hacky but works quite well: Create a temporary backup storage account, copy your data there, recreate the actual storage account, and then copy the data back. Here, I will explain how to do that using azcopy.

1. Create a backup account. While the rest of my setup is handled with terraform as infrastructure as Code (IaC), I did this manually in the Azure UI, as it is just temporary. It makes sense to choose the same settings as for the storage account that you want to backup.

2. Download azcopy (https://docs.microsoft.com/en-us/azure/storage/common/storage-use-azcopy-v10) and unpack it.

3. Login to your Azure account in the command line. You can do that with `./azcopy login` which will lead you to a so-called device-login (meaning you should open a link in the browser, enter a alphanumeric code and then proceed with the normal Azure login). You might also need to choose the correct subscription in case you have several: `az account set --subscription <subscription_id>`. Also in some cases it can be necessary to add the tenantId: `./azcopy login --tenant-id <tenantId` (you can get your tenant-id for example on the overview page of your "Azure Active Directory" resource in the Azure portal).

4. Now create a Shared access signature for accessing the data with azcopy. Copy the resulting "Blob service SAS URL".
![Generate SAS](/blog/backup-azure-storage/generate-sas.png)

5. You can now list the files inside the storage account by typing `./azcopy list <SAS URL>` (no additional parentheses).

6. To copy all data from one storage account to another (empty) storage account, you first need to get the SAS for the target account as well (see 4.) and then copy with the command: `./azcopy cp <SAS URL origin> <SAS URL destination> --recursive`.

7. Note that you can also copy on a per-container basis. In this case, choose the container, go to "Shared access tokens", generate a SAS and proceed as above. Note that the default permissions for the SAS in this case is "Read" and you might have to add more.

In my case, I would now recreate the original storage account and copy all data back the same way. This might be a niche use case, but copying data of storage accounts with `azcopy` is certainly a useful skill also in other situations.
