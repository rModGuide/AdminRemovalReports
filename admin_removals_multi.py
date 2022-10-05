#  AdminRemovalReport bot v2.0 by u/BuckRowdy
#  Add this bot with wiki and manage user perms only

from pmaw import PushshiftAPI
from datetime import datetime as datetime
import praw
import traceback
import time


# Login to reddit
try:
	reddit = praw.Reddit(   
              	user_agent = 'AdminRemovalReportBot v2.0 by u/BuckRowdy to gather info from the mod log.',
		client_id = '',
		client_secret = '',
              	username = '',         
		password = '')

except Exception as e:
	print(f"\t### ERROR - Could not login.\n\t{e}")
	traceback.print_exc()
	
print(f'Logged in as: {reddit.user.me()}')

# Connect to the pushshift api via pmaw
api = PushshiftAPI()

def check_mod_log():
	'''This script runs on a weekly schedule on crontab, or can be run manually.  
	   It polls the mod log for admin-level removals in the past 7 days.
	   It will create three tables: comments, posts, and a catch-all for all other mod actions.
	   The bot updates a wiki page in your subreddit, with the data.
	   It will contact PushShift for the original text of comments and reproduce them if possible. 
	   This is a multi-sub version of the bot, a single sub version is also included in this repo.   
	'''
	print('Now processing your mod log...')
	# Set up a variable for finding the last 7 days worth of posts. 
	last_pass = (time.time() - 604800)
	
	# Bot will cycle through its entire mod list, updating wiki pages, and sending mail.  
	for subreddit in reddit.user.me().moderated():
		try:
			print(f'Gathering stats on r/{subreddit.display_name}.')
			# Set up some variables to count removals and create lists.
			comment_counter = 0
			posts_counter = 0
			other_counter = 0
			user_comments = []
			user_posts = []
			other_posts = []
			# Scan the mod log for admin-level comment removals within the past week and assign comment attributes as variables.
			for log in reddit.subreddit(subreddit.display_name).mod.log(mod='a', limit=None):		
				if log.action == 'removecomment':
					if log.created_utc >= last_pass:
						time_stamp = datetime.fromtimestamp(int(log.created_utc)).strftime('%m/%d/%Y at %H:%M')	
						log_action = log.action
						log_mod = log.mod
						target_author = log.target_author
						target_link = log.target_permalink
						# Extract the thread ID from the log item permalink.  The link is a string, so we split and grab the '5th section'.
						thread_id = target_link.split('/')
						thread_id = thread_id[4]
						# Process the comment id by stripping the object identifier, 't1_' from the item fullname.
						comment_id = log.target_fullname
						comment_id = comment_id[3:]
						# Once you have the comment id, search pushshift for the comment's body text.				
						comment_search = api.search_comments(ids=comment_id) 	
						comment_list = [comment for comment in comment_search]
						# Check if the target user is banned in that subreddit and return a simple Yes/No value. 
						ban_check = any(reddit.subreddit(subreddit.display_name).banned(redditor=f'{target_author}'))
						if ban_check:
							user_banned = 'Yes'
						else:
							user_banned = 'No'						
						# This block takes the original comment body (if archived) and condenses it, removing new lines.  
						for comment in comment_list:							
							if 'body' in comment:
								body_text = ''.join([comment_text for comment_text in comment["body"] if comment_text not in ['\n', '\n\n']])
							else:
								body_text = 'No comment body text found'	
						# Add each admin removal comment to a list set up for a reddit markdown table. 
						user_comments.append(f'{log_mod} | u/{target_author} | {user_banned} | {time_stamp} | {body_text} | [{thread_id}]({target_link})')
						# Count the number of admin removed comments.
						comment_counter = len(user_comments)
						
			# If comment removals exist, join each one of them for proper reddit table formatting.
			if comment_counter > 0: 
				new_comment_list = '\n'.join(user_comments)
			else:
				new_comment_list = 'None found'		
	
			# Scan the mod log for admin-level submission removals within the past week and assign attributes as variables.
			for log in reddit.subreddit(subreddit.display_name).mod.log(mod='a', limit = None):		
				if log.action == 'removelink':
					if log.created_utc >= last_pass:
						time_stamp = datetime.fromtimestamp(int(log.created_utc)).strftime('%m/%d/%Y at %H:%M')	
						log_action = log.action
						log_mod = log.mod
						target_author = log.target_author
						target_link = log.target_permalink
						target_title = log.target_title
						# Process the submission id by stripping the object identifier, 't3_' from the item fullname.
						submission_id = log.target_fullname
						submission_id = submission_id[3:]
						# Once you have the comment id, search pushshift for the comment's body text.
						posts = api.search_submissions(ids=submission_id)
						post_list = [post for post in posts]
						# Check if the target user is banned in the subreddit.
						ban_check = any(reddit.subreddit(subreddit.display_name).banned(redditor=f'{target_author}'))
						if ban_check:
							user_banned = 'Yes'
						else:
							user_banned = 'No'						
						# This block grabs the post title from pushshift if it was archived. 
						for post in post_list:
							if 'title' in post:
								target_title = post["title"]
							else:
								target_title = 'No title text found'
						# Add each admin removal comment to a list set up for a reddit markdown table.
						user_posts.append(f'{target_title} | {log_mod} | u/{target_author} | {user_banned} | {time_stamp} | [link]({target_link})')
						# Count the number of admin removed submissions.
						posts_counter = len(user_posts)

			# If submission removals exist, join each entry for proper reddit table formatting.			
			if posts_counter > 0:
				# for post in user_posts:
				new_post_list = '\n'.join(user_posts)
					# print(new_post_list)
			else:
				new_post_list = 'None found'
		
			# Scan the mod log for admin-level non-removal actions.
			for log in reddit.subreddit(subreddit.display_name).mod.log(mod='a'):		
				action_blacklist  = [ 		
									'removelink',
									'removecomment'
									]
				if log.action not in action_blacklist:
					if log.created_utc >= last_pass:
						time_stamp = datetime.fromtimestamp(int(log.created_utc)).strftime('%m/%d/%Y at %H:%M')	
						log_action = log.action
						log_mod = log.mod
						target_author = log.target_author
						target_link = log.target_permalink
						target_title = log.target_title
						# Add each admin removal comment to a list set up for a reddit markdown table.
						other_posts.append(f'{log_action} | {log_mod} | {time_stamp})')
						# Count the number of admin non-removal actions, which typically will be None.
						other_counter = len(other_posts)
			# If other actions exist, format each entry for a markdown table. 			
			if other_counter > 0:
				new_other_post_list = '\n'.join(other_posts)
			else:
				new_other_post_list = 'None found'

			# Reddit markdown table headers, modmail message subject and body.
			comment_table_header = f'**Comments Removed:** {comment_counter}\n\nMod | User | Banned | When | Body | Thread ID\n---|---|---|---|---|---\n'
			posts_table_header = f'**Submissions Removed:** {posts_counter}\n\nTitle | Mod | User | Banned | When | Thread ID\n---|---|---|---|---|---|---\n'
			other_table_header = f'**Other Actions:** {other_counter}\n\nAction | Mod | When\n---|---|---\n\n'
			message_body = '**Weekly admin action summary:**\n\n'+posts_table_header+new_post_list+'\n\n'+comment_table_header+new_comment_list+'\n\n'+other_table_header+new_other_post_list
			message_body_selftext = f'Your weekly admin action summary has been updated.\nPlease visit [this wiki page](http://reddit.com/r/{subreddit}/wiki/AdminRemovalReport) for your summary.'
			message_title = f'Your weekly Admin Removal Report is ready.'
			# reddit.subreddit(subreddit.display_name).message(
			# 	subject=message_title, message=message_body_selftext)		
			# Edit your wiki page to add the tables.
			reddit.subreddit(subreddit.display_name).wiki['AdminRemovalReport'].edit(content=f'{message_body}', reason='admin removal report update')             
			# Print to the terminal when this subreddit is finished processing.
			print(f'> Done with r/{subreddit.display_name}')
			# In case of rate limits on sending modmails. 
			time.sleep(10)

		except Exception as e:
			print(f'\t### ERROR - Could not login.\n\t{e}')
			traceback.print_exc()
				

# Run the bot's main (only) function.
check_mod_log()
