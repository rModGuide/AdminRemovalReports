# Admin_Removal_Reports

A bot to post a summary of admin-level removals in your subreddit. 

This bot is designed to run as a cronjob, once a week.  In windows this is done via the Task Scheduler.  

Cronjobs on MacOS and Linux are done via the [crontab](https://betterprogramming.pub/https-medium-com-ratik96-scheduling-jobs-with-crontab-on-macos-add5a8b26c30).

This bot was written for python 3.9 and the most recent version of PRAW and PMAW. 

Install bot of those via these links [PRAW](http://praw.readthedocs.io) and [PMAW](https://pypi.org/project/pmaw/).

There are three files in the repo.  A version for a single subreddit, a verison for multiple subreddits, and a multisub version that auto accepts mod invites.  This version is really just for if you want to add the bot to several subs at once and don't want to have to login to the bot account to accept the invites.  If you have the bot set up a cronjob cycle it will accept and run the report when it runs next.
