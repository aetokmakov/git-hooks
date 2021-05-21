# git-hooks
 Hooks for using with git

1. prepare-msg hook. 

Add JIRA task number to your commit message. Your branch must be named same as JIRA task. And you must perform the following command in cmd:

git config --local core.branchPrefix <JIRA Project Name (i.e. task is PROJECT-123, then use PROJECT)>
