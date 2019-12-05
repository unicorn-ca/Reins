# Unicorn Reporter
## Overview
- A  **AWS Lambda** function that's designed to be injected into stages of a **AWS CodePipeline** , It will:
	-  Check for any overly permissive user/role accounts
		- Any user/role/group with `*` in it's resource or actions
	-  Checks if the last commit was made by a valid user 
	- Checks the integrity of the last commit
	- Checks if anything if the pipeline is running under root
- This project was initially designed for Unicorn pipeline, but has been adapted to work for most AWS pipeline 

## Assumptions

 - The Reporter itself has been setup correctly 
	 - This includes proper security protections
 - It running under a role that has permissions outlined below 


## Required Permissions
The required role permissions for each reporter type
| Reporter Type|Required Permission |
|--------------|--------------------|
| all | codepipeline.put_job_success_result <br>codepipeline.put_job_failure_result <br> iam.get_user<br>iam.get_group<br>iam.get_role|
| codecommit | cloudtrail.lookup_events |
| policychecker | iam.get_policy<br>iam.get_policy_version<br>iam.list_attached_user_policies<br>iam.list_attached_group_policies<br>iam.list_attached_role_policies |
SNS Notification | SNS.publish

## Installation

 1. Download the `funtion.zip` file from release
 2. Upload  the `funtion.zip` to lambda with the config `runtime:python3.6` `handler:index.handler` `ExecutionRole:a role with the required permssions` `timeout:4min`
 3. Add an invoke action to your pipeline which points to the new lambda with the User Param:

For **policychecker**
```json
{"reporterType":"policychecker","group":"Exclude from test group"}
```
For **codecommit**
```json
{"reporterType":"codecommit","branch":"The CodeCommit Branch","repo":"The CodeCommit Repo","group":"The Allowed Commit Group"}
```
For **To Add SNS Notifcation** (Don't need both)
```json
{"accept_sns_arn":"The ARN of sucessful Topic","fail_sns_arn":"The ARN of fail Topic"}
```
