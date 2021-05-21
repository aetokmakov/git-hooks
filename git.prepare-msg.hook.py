#!/usr/bin/env python3

"""
Git hook for automatically assigning a task number to a commit message.
Branches should be named according to the standard ProjectName-TaskNumber.
"""

import re
import sys
import codecs
import subprocess 

# get current branch name
branch = (
    subprocess.check_output(["git", "symbolic-ref", "--short", "HEAD"]).decode("utf-8").strip()
)

# exists or not special parameter in local config?
is_branch_prefix = True
try:
	# get a branch prefix, parameter from local config, same as ProjectName in Jira
	branch_prefix = (
		subprocess.check_output(["git", "config", "core.branchPrefix"]).decode("utf-8").strip()
	)	
except subprocess.CalledProcessError as e:
	is_branch_prefix = False

if is_branch_prefix:
	# get a file path for file COMMIT_EDITMSG
	commit_msg_filepath = (
		subprocess.check_output(["git", "rev-parse", "--show-toplevel"]).decode("utf-8").strip()
	)
	commit_msg_filepath = commit_msg_filepath + "/.git/COMMIT_EDITMSG"

	# сheck the standard
	regex = r"%s\-?\d+" % branch_prefix
	if re.match(regex, branch, re.IGNORECASE):
		# if all is ok then we write JIRA task number in square brackets before commit message
		
		# if branch name without '-' then we add it between ProjectName and number
		if branch.find('-') != -1: 
			issue_number = branch.upper()
		else:
			issue_number = (branch[:len(branch_prefix)] + '-' + branch[len(branch_prefix):]).upper()
			
		with codecs.open(commit_msg_filepath, "r+", "utf-8") as f:
			commit_msg = f.read()
			# search JIRA num before git comments
			sharp = commit_msg.find("#")
			# maybe JIRA number already exists in commit message
			if commit_msg.upper().find('[' + issue_number + ']', 0, sharp) == -1:
				f.seek(0, 0)  # correctly positions issue_number when writing commit message
				f.write(f"[{issue_number}] {commit_msg}")