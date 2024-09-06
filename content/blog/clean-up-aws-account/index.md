---
title: "Clean up your AWS account"
date: 2023-03-12T12:00:00+01:00
draft: false
tags: [DevOps, AWS]
---

Since I usually use Azure, I thought "let's try out Databricks on AWS for fun" and was surprised how many resources were created that I completely lost track of... In retrospective, terraform would have been a better choice so that I can destroy resources with one command. So: how would I clean up AWS and delete all resources? 

[AWS-nuke](https://github.com/rebuy-de/aws-nuke) is a helpful script to destroy all resources within an AWS account. Let's go through all the steps.

1. Install aws-nuke: on a mac simply with `brew install aws-nuke` (for other OS see the aws-nuke github page).
2. Setup the AWS CLI with `brew install awscli` and then `aws configure`. You will then have to enter AWS Access Key ID, AWS Secret Access Key, Default region name, Default output format (e.g. json). To get the keys, go to "IAM", "Users", choose the relevant user, then "Security credential", then down to "Access keys".
3. Now configure aws-nuke. Create a file, for example `nuke-config.yml`. Parameters are
   1. The list of regions to nuke, here I tried to select all.
   2. An account-blocklist. Here you should list the accounts that should not be nuked. In a usecase, where you have a production account and several development accounts that you want to clean up from time to time, list the production account here. In my case, I just have one development account, so I listed a dummy account here.
   3. The account to nuke (find out the account ID by clicking on your account drop-down menu in the upper right corner of the AWS console) and a list of filters. In my case I wanted to keep my admin account and the corresponding key as well as the Billing Alarm. But you can list any resource here.
    ```
    regions:
    - "global" # This is for all global resource types e.g. IAM
    - "us-east-2"
    - "us-east-1"
    - "us-west-1"
    - "us-west-2"
    - "af-south-1"
    - "ap-east-1"
    - "ap-south-1"
    - "ap-northeast-3"
    - "ap-northeast-2"
    - "ap-southeast-1"
    - "ap-southeast-2"
    - "ap-northeast-1"
    - "ca-central-1"
    - "cn-north-1"
    - "cn-northwest-1"
    - "eu-central-1"
    - "eu-west-1"
    - "eu-west-2"
    - "eu-south-1"
    - "eu-west-3"
    - "eu-north-1"
    - "me-south-1"
    - "sa-east-1"

    account-blocklist:
    - "999999999999" # production

    accounts:
    "6**********2":
        filters:
        IAMUser:
        - "gbusch"
        IAMUserPolicyAttachment:
        - "gbusch -> AdministratorAccess"
        IAMUserAccessKey:
        - "gbusch -> A*************H"
        CloudWatchAlarm:
        - "BillingAlarm"
    ```
4. A dry-run will show you all resources and what aws-nuke is planning to do with it: `aws-nuke -c nuke-config.yml --profile default`. 
5. To actually delete resources, run with the no-dry-run-flag: `aws-nuke -c nuke-config.yml --profile default --no-dry-run`.
