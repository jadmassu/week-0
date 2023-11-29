
from loader import SlackDataLoader 
slack_loader = SlackDataLoader('/home/user/Documents/10/Assignment/week-0/anonymized')

__all__ = ['SlackDataLoader']


# parse_slack_reaction = slack_loader.get_channel_messages('../anonymized/')
users = slack_loader.get_users()
channel = slack_loader.get_channels()
# avg_reply_users = slack_loader.draw_avg_reply_users_count()
print(channel)