# Reins (Account/Pipeline Auditor)

![Reins-Logo](reins-logo.png)

## Overview
- A framework for **AWS Lambda** function that's designed to be injected into stages of a **AWS CodePipeline** or as stand-alone libary:
- Example Reporters (Can Be Seen in `/unicon_pipeline_reporter/reporter_types`)
	- PolicyChecks
		-  Check for any overly permissive user/role accounts
			- Any user/role/group with `*` in it's resource or actions
		- If any non-auth user has write access to Pipeline resouces
	- CodeCommit:
		- Checks if the last commit was made by a valid user
	- MulitChecker:
		- Checks if any roots activities 
		- Checks for any unauthorised access to pipeline resouces
- It can also work as standalone lambda function (The user Params are just the request params)
- This also has a **CLI** usesed to run the project locally 
- This project was initially designed for Unicorn pipeline, but has been adapted to work for most AWS pipeline 

## Assumptions

 - The Reporter itself has been setup correctly 
	 - This includes proper security protections
 - It running under a role that has permissions outlined below 


## Required Permissions
The required role permissions for each reporter type


| Reporter Type|Required Permission |
|--------------|--------------------|
| All | codepipeline.put_job_success_result <br>codepipeline.put_job_failure_result <br> iam.get_user<br>iam.get_group<br>iam.get_role|
| Codecommit | cloudtrail.lookup_events |
| Policychecker | iam.get_policy<br>iam.get_policy_version<br>iam.list_attached_user_policies<br>iam.list_attached_group_policies<br>iam.list_attached_role_policies |
| Multicheck | cloudtrail.lookup_events
SNS Notification | sns.publish

## Installation (For Pipeline)

 1. Download the `funtion.zip` file from release
 2. Upload  the `funtion.zip` to lambda with the config `runtime:python3.6` `handler:index.handler` `ExecutionRole:a role with the required permssions` `timeout:10min`
 3. Add an invoke action to your pipeline which points to the new lambda with the User Param:

For **policychecker**
```json
{"reporterType":"policychecker","group":"Exclude from test group"}
```
For **codecommit**
```json
{"reporterType":"codecommit","branch":"The CodeCommit Branch","repo":"The CodeCommit Repo","group":"The Allowed Commit Group"}
```
For **multi-check**
```json
{"reporterType":"multichecker","group":"The Admin Group"}
```
For **To Add SNS Notifcation** (Don't need both)
```json
{"accept_sns_arn":"The ARN of sucessful Topic","fail_sns_arn":"The ARN of fail Topic"}
```

## Installation (For CLI)
### Requirements
- `python 3.6+`
- `AWS CLI`

### Steps
 1. Download the `funtion.zip` file from release
 2. Unzip `function.zip` into an empty folder
 3. Run `aws configure` and enter your `AWS Access Key ID`, `AWS Secret Access Key` and `Default region name`
 4. run `python3 cli.py TheNameOfTheReport(The reporter type from above) '{Same User params as above minus 'reporterType'}'`
 
 ### Example
 If your using the in built checkers you can run: (replace "ADMINGROUPNAME" with your group name)<br>
 ```python3 cli.py policychecker '{"group":"ADMINGROUPNAME"}'```
 
 
