import json
import argparse
import os
import io
import shutil
import copy
import glob

from datetime import datetime
# from pick import pick
from time import sleep
import pandas as pd
from matplotlib import pyplot as plt


# Create wrapper classes for using slack_sdk in place of slacker
class SlackDataLoader:
    '''
    Slack exported data IO class.

    When you open slack exported ZIP file, each channel or direct message 
    will have its own folder. Each folder will contain messages from the 
    conversation, organised by date in separate JSON files.

    You'll see reference files for different kinds of conversations: 
    users.json files for all types of users that exist in the slack workspace
    channels.json files for public channels, 
    
    These files contain metadata about the conversations, including their names and IDs.

    For secruity reason, we have annonymized names - the names you will see are generated using faker library.
    
    '''
    def __init__(self, path):
        '''
        path: path to the slack exported data folder
        '''
        self.path = path
        self.channels = self.get_channels()
        self.users = self.get_users()
    

    def get_users(self):
        '''
        write a function to get all the users from the json file
        '''
        with open(os.path.join(self.path, 'users.json'), 'r') as f:
            users = json.load(f)

        return users
    
    def get_channels(self):
        '''
        write a function to get all the channels from the json file
        '''
        with open(os.path.join(self.path, 'channels.json'), 'r') as f:
            channels = json.load(f)

        return channels

    def get_channel_messages(self, channel_name):
        '''
        write a function to get all the messages from a channel
        
        '''
    
        """ parse slack data to extract useful informations from the json file
            step of execution
            1. Import the required modules
            2. read all json file from the provided path
            3. combine all json files in the provided path
            4. extract all required informations from the slack data
            5. convert to dataframe and merge all
            6. reset the index and return dataframe
        """

    # specify path to get json files
        combined = []
        for json_file in glob.glob(f"{channel_name}*.json"):
            with open(json_file, 'r', encoding="utf8") as slack_data:
                combined.append(slack_data)

        # loop through all json files and extract required informations
        dflist = []
        for slack_data in combined:

            msg_type, msg_content, sender_id, time_msg, msg_dist, time_thread_st, reply_users, \
            reply_count, reply_users_count, tm_thread_end = [],[],[],[],[],[],[],[],[],[]

            for row in slack_data:
                if 'bot_id' in row.keys():
                    continue
                else:
                    msg_type.append(row['type'])
                    msg_content.append(row['text'])
                    if 'user_profile' in row.keys(): sender_id.append(row['user_profile']['real_name'])
                    else: sender_id.append('Not provided')
                    time_msg.append(row['ts'])
                    if 'blocks' in row.keys() and len(row['blocks'][0]['elements'][0]['elements']) != 0 :
                        msg_dist.append(row['blocks'][0]['elements'][0]['elements'][0]['type'])
                    else: msg_dist.append('reshared')
                    if 'thread_ts' in row.keys():
                        time_thread_st.append(row['thread_ts'])
                    else:
                        time_thread_st.append(0)
                    if 'reply_users' in row.keys(): reply_users.append(",".join(row['reply_users'])) 
                    else:    reply_users.append(0)
                    if 'reply_count' in row.keys():
                        reply_count.append(row['reply_count'])
                        reply_users_count.append(row['reply_users_count'])
                        tm_thread_end.append(row['latest_reply'])
                    else:
                        reply_count.append(0)
                        reply_users_count.append(0)
                        tm_thread_end.append(0)
            data = zip(msg_type, msg_content, sender_id, time_msg, msg_dist, time_thread_st,
            reply_count, reply_users_count, reply_users, tm_thread_end)
            columns = ['msg_type', 'msg_content', 'sender_name', 'msg_sent_time', 'msg_dist_type',
            'time_thread_start', 'reply_count', 'reply_users_count', 'reply_users', 'tm_thread_end']

            df = pd.DataFrame(data=data, columns=columns)
            df = df[df['sender_name'] != 'Not provided']
            dflist.append(df)

        dfall = pd.concat(dflist, ignore_index=True)
        dfall['channel'] = path_channel.split('/')[-1].split('.')[0]        
        dfall = dfall.reset_index(drop=True)
        
        return dfall


    def slack_parser(self,path_channel):
        """ parse slack data to extract useful informations from the json file
            step of execution
            1. Import the required modules
            2. read all json file from the provided path
            3. combine all json files in the provided path
            4. extract all required informations from the slack data
            5. convert to dataframe and merge all
            6. reset the index and return dataframe
        """

    # specify path to get json files
        combined = []
       
        for json_file in glob.glob(f"{path_channel}*.json"):
         
            with open(json_file, 'r', encoding="utf8") as file:
                slack_data = file.read()
                combined.append(slack_data)
        
        # loop through all json files and extract required informations
        dflist = []
        for slack_data in combined:
            json_data = json.loads(slack_data)

            msg_type,user, msg_content, sender_id, time_msg, msg_dist, time_thread_st, reply_users, \
            reply_count, reply_users_count, tm_thread_end = [],[],[],[],[],[],[],[],[],[],[]

            for row in json_data:
                if 'bot_id' in row.keys():
                    continue
                else:
                    msg_type.append(row['type'])
                    user.append(row['user'])
                    
                    msg_content.append(row['text'])
                    
                    if 'user_profile' in row.keys(): sender_id.append(row['user_profile']['real_name'])
                    else: sender_id.append('Not provided')
                    time_msg.append(row['ts'])
                    if 'blocks' in row.keys() and len(row['blocks'][0]['elements'][0]['elements']) != 0 :
                        msg_dist.append(row['blocks'][0]['elements'][0]['elements'][0]['type'])
                    else: msg_dist.append('reshared')
                    if 'thread_ts' in row.keys():
                        time_thread_st.append(row['thread_ts'])
                    else:
                        time_thread_st.append(0)
                    if 'reply_users' in row.keys(): reply_users.append(",".join(row['reply_users'])) 
                    else:    reply_users.append(0)
                    if 'reply_count' in row.keys():
                        reply_count.append(row['reply_count'])
                        reply_users_count.append(row['reply_users_count'])
                        tm_thread_end.append(row['latest_reply'])
                    else:
                        reply_count.append(0)
                        reply_users_count.append(0)
                        tm_thread_end.append(0)
            data = zip(msg_type, user,msg_content, sender_id, time_msg, msg_dist, time_thread_st,
            reply_count, reply_users_count, reply_users, tm_thread_end)
            columns = ['msg_type', 'user','msg_content', 'sender_name', 'msg_sent_time', 'msg_dist_type',
            'time_thread_start', 'reply_count', 'reply_users_count', 'reply_users', 'tm_thread_end']

            df = pd.DataFrame(data=data, columns=columns)
            df = df[df['sender_name'] != 'Not provided']
            dflist.append(df)
            
        # for item in dflist:
        #     if isinstance(item, pd.DataFrame):
        #         print("DataFrame found!")
        #     else:
        #         print("Not a DataFrame.")
            
        # print(dflist)
        dfall = pd.concat(dflist, ignore_index=True)
        dfall['channel'] = path_channel.split('/')[-1].split('.')[0]        
        dfall = dfall.reset_index(drop=True)
        
        return dfall

    def draw_avg_reply_count(self, data, channel='Random'):#which user has the highest number of reply counts?
        """who commands many reply?"""
        df = pd.DataFrame(data)
        df.groupby('sender_name')['reply_count'].mean().sort_values(ascending=False)[:20]\
            .plot(kind='bar', figsize=(15,7.5));
        plt.title(f'Average Number of reply count per Sender in #{channel}', size=20, fontweight='bold')
        plt.xlabel("Sender Name", size=18); plt.ylabel("Frequency", size=18);
        plt.xticks(size=14); plt.yticks(size=14);
        plt.show()

    def parse_slack_reaction(self, path, channel):
            """get reactions"""
            dfall_reaction = pd.DataFrame()
            combined = []
            for json_file in glob.glob(f"{path}*.json"):
                with open(json_file, 'r') as slack_data:
                    combined.append(slack_data)

            reaction_name, reaction_count, reaction_users, msg, user_id = [], [], [], [], []

            for k in combined:
                slack_data = json.load(open(k.name, 'r', encoding="utf-8"))
                
                for i_count, i in enumerate(slack_data):
                    if 'reactions' in i.keys():
                        for j in range(len(i['reactions'])):
                            msg.append(i['text'])
                            user_id.append(i['user'])
                            reaction_name.append(i['reactions'][j]['name'])
                            reaction_count.append(i['reactions'][j]['count'])
                            reaction_users.append(",".join(i['reactions'][j]['users']))
                    
            data_reaction = zip(reaction_name, reaction_count, reaction_users, msg, user_id)
            columns_reaction = ['reaction_name', 'reaction_count', 'reaction_users_count', 'message', 'user_id']
            df_reaction = pd.DataFrame(data=data_reaction, columns=columns_reaction)
            df_reaction['channel'] = channel
            return df_reaction
    # 
    def visualize_reply_counts(self, data, channel='Random'):
        """Visualize reply counts per user per channel"""
        df = pd.DataFrame(data)
        grouped = df.groupby(['user', 'channel'])['reply_count'].sum().unstack()

        grouped.plot(kind='bar', figsize=(15, 7.5))
        plt.title(f'Reply Counts per User in #{channel}', size=20, fontweight='bold')
        plt.xlabel("User", size=18)
        plt.ylabel("Reply Count", size=18)
        plt.xticks(size=14)
        plt.yticks(size=14)
        plt.legend(title="Channel", title_fontsize=14, fontsize=12)

        plt.show()
    def get_user_map(self):
        '''
        write a function to get a map between user id and user name
        '''
        userNamesById = {}
        userIdsByName = {}
        for user in self.users:
            userNamesById[user['id']] = user['name']
            userIdsByName[user['name']] = user['id']
        return userNamesById, userIdsByName        


    def draw_user_reaction(self,data, channel='General'):
        data.groupby('sender_name')[['reply_count', 'reply_users_count']].sum()\
            .sort_values(by='reply_count',ascending=False)[:10].plot(kind='bar', figsize=(15, 7.5))
        plt.title(f'User with the most reaction in #{channel}', size=25);
        plt.xlabel("Sender Name", size=18); plt.ylabel("Frequency", size=18);
        plt.xticks(size=14); plt.yticks(size=14);
        plt.show()

    def get_top_20_user(self, data, channel='Random'):
        """get user with the highest number of message sent to any channel"""

        data['sender_name'].value_counts()[:10].plot.bar(figsize=(15, 7.5))
        plt.title(f'Top 20 Message Senders in #{channel} channels', size=15, fontweight='bold')
        plt.xlabel("Sender Name", size=18); plt.ylabel("Frequency", size=14);
        plt.xticks(size=12); plt.yticks(size=12);
        plt.show()

        data['sender_name'].value_counts()[-10:].plot.bar(figsize=(15, 7.5))
        plt.title(f'Bottom 10 Message Senders in #{channel} channels', size=15, fontweight='bold')
        plt.xlabel("Sender Name", size=18); plt.ylabel("Frequency", size=14);
        plt.xticks(size=12); plt.yticks(size=12);
        plt.show()
        
    def draw_avg_reply_users_count(self,data, channel='Random'):
        """who commands many user reply?"""

        data.groupby('sender_name')['reply_users_count'].mean().sort_values(ascending=False)[:10].plot(kind='bar',
        figsize=(15,7.5));
        plt.title(f'Average Number of reply user count per Sender in #{channel}', size=20, fontweight='bold')
        plt.xlabel("Sender Name", size=18); plt.ylabel("Frequency", size=18);
        plt.xticks(size=14); plt.yticks(size=14);
        plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Export Slack history')

    
    parser.add_argument('--zip', help="Name of a zip file to import")
    args = parser.parse_args()
