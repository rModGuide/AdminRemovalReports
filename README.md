# Admin_Removal_Reports

A bot to post a summary of admin-level removals in your subreddit.

If you're new to scripting or need help with how to run a bot like this, see [this reddit post](https://www.reddit.com/r/modguide/comments/s3xwbu/how_to_run_a_basic_python_script_for_reddit_from/).

This bot is designed to run as a cronjob, once a week.  In windows this is done via the [Task Scheduler](https://active-directory-wp.com/docs/Usage/How_to_add_a_cron_job_on_Windows/Scheduled_tasks_and_cron_jobs_on_Windows/index.html).  

Cronjobs on MacOS and Linux are done via the [crontab](https://betterprogramming.pub/https-medium-com-ratik96-scheduling-jobs-with-crontab-on-macos-add5a8b26c30).

The bot account needs `manage wiki` and `manage users` perms.  The only reason it needs manage users is to check if user is banned. It is not currently set up to check if it has the perms it needs.  If it doesn't have the right perms the bot will crash.  Perm check will come in a future update. 

This bot was written for python 3.9 and the most recent versions of PRAW and PMAW. Install both of those modules via these links [PRAW](http://praw.readthedocs.io) and [PMAW](https://pypi.org/project/pmaw/).

There are three files in the repository.  A version for a single subreddit, a verison for multiple subreddits, and a multisub version that auto accepts mod invites.  This version is really just for if you want to add the bot to subreddits in the future and don't want to have to login to the bot account to accept the invites.  If you have the bot set up on a cronjob cycle it will accept and run the report when it runs next.

---
**Versions**

**All Versions**
- Add this bot with manage wiki and manage user perms. It will post a report in the subreddit/wiki/adminremovalreport page; if the wiki page doesn't exist, it will be created. It will then notify the sub via modmail that a new report has been posted.  If the bot HAS mail perms it will start a new mod discussion.  Those can't be archived and will clog up the folder making more importand discussions hard to find. The bot will never ban or action a user, the `manage users` perm is only for checking if the actioned user is already banned in your subreddit.

**admin_removals_single.py**
- Rename the script (if desired) once you have cloned or downloaded it.   
- Designed to run on a single subreddit via a cronjob or scheduled task.
- On lines 14-17, enter your bot's account credentials. **[See here for how to do that.](https://www.reddit.com/r/modguide/comments/s3xwbu/how_to_run_a_basic_python_script_for_reddit_from/)** 
- On line 29, define the subreddit to work on.

**admin_removals_multi.py**
- Rename the script (if desired) once you have cloned or downloaded it.
- Designed to run on the entire modlist of the bot account.  If you add this bot with manage wiki and manage user perms, it will post a report in the subreddit/wiki/adminremovalreport page for each sub on the list.  If the page doesn't exist, it will be created.  
- Processing reports in high volume subs can give the impression the bot is stalled.  It will notify when it has cycled for each subreddit. 
- On lines 15-19, enter the login credentials for the bot account.  **[See here for how to do that.](https://www.reddit.com/r/modguide/comments/s3xwbu/how_to_run_a_basic_python_script_for_reddit_from/)** 
- No need to define a subreddit to work on.  

**admin_removals_autoinvite.py**
- Rename the script (if desired) once you have cloned or downloaded it.
- When the bot starts up it will check its inbox for mod invites, then auto accept them. 
- Otherwise it is the same version as the multisub version.
- This version is handy if you plan to add the bot to more than one subreddit so that you don't have to login to the bot account to accept.  If you have this bot running on a schedule, once it starts up on its next run, it will add that sub to its list, mesage the sub that it has accepted and is preparing a report.  Then it will message when the report is posted. 


If you would like to add this bot to your subreddit instead of running your own instance of it, please message me.
