# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 18:45:40 2018

@author: Image17


https://www.reddit.com/api/v1/authorize?client_id=kkxH8GHYYVYx5Q&response_type=code&
    state='henlo'&redirect_uri=http://127.0.0.1:65010/authorize_callback&duration=temporary&scope=read
"""

import sys
import praw
import csv
import glob

"""
Login to reddit through praw to provide a session for the scraper
"""
def login():
    session = praw.Reddit(username = 'dr_wormhat',
                password = '8@sACW2R7Sep4!u',
                client_id = 'kkxH8GHYYVYx5Q',
                client_secret =     'mRRC7fYfT0GJ_dlbPEFYEvJpo6k',
                user_agent = 'suh dud dr_wormhat')
    return session
    
"""
Scrape subreddit s of as money comments as possible and write to a specific file
"""
def scrape(s):
    comments=[]
    r = login()
    for comment in r.subreddit(s).comments(limit=10000):
        if comment and comment.author:
            cmmt = []
            # attain variables from prraw comment
            create_timestamp = str(comment.created_utc)
            author_name = comment.author.name
            # when accessing the comment body from the csv you must decode with utf8
            comment_body = str(comment.body)
            # clean each piece of data individually if necessary
            
            # add to list to be written to a file
            cmmt.append(create_timestamp)
            cmmt.append(s)
            cmmt.append(author_name)
            cmmt.append(comment_body)
            comments.append(cmmt)
    # write list to file
    with open('reddit/reddit-data-'+s+'.csv', mode='w+', newline='',encoding='utf-8') as reddit_data:
        csv_writer = csv.writer(reddit_data, delimiter='|')
        for c in comments:
            csv_writer.writerow(c)

"""
Due to the limitations of praw and the reddit api we are susceptible to having
duplicate comments in our data set.  It is important to remove comments that
may have been retrieved twice.  Adjust the scheduling of the scraping to limit
duplicates.
"""         
def clean_duplicates():
    print('cleaning...')
    files = glob.glob("reddit/*.*")
    for file in files:
        print('cleaning '+file)
        comments=[]
        with open(file, newline='', encoding='utf-8') as csvfile:
            spamreader = csv.reader(csvfile, delimiter='|')
            for row in spamreader:
                comment=[]
                if row not in comments:
                    for i in row:
                        comment.append(i)
                    comments.append(comment)
        print(len(comments))
        
        with open (file, 'w', newline='',encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter='|')
            csvfile.truncate()
            for c in comments:
                csv_writer.writerow(c)
    print('clean!')  


def merge_files():
    print('merging..')
    files = glob.glob("reddit/*.*")
    for file in files:
        print('handling',file)
        comments=[]
        with open(file, newline='',encoding='utf-8') as infile:
            reader = csv.reader(infile, delimiter='|')
            for row in reader:
                comment=[]
                if row not in comments:
                    for i in row:
                        comment.append(i)
                    comments.append(comment)
        with open ('reddit/merged.csv', 'a', newline='',encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter='|')
            csvfile.truncate()
            for c in comments:
                #c = c.append(file.split('-')[3].split('.')[0])
                csv_writer.writerow(c)
    print('merged!')


"""
Takes command line arguments of subreddit names, uses praw api to retrieve ~1000
comments and writes them to the local filesystem
"""
def main():
    print("scraping has begun")
    for subreddit in sys.argv[1:]:
        print('scraping ' + subreddit + '. . .')
        scrape(subreddit)
        print('scraping ' + subreddit + ' completed!')
    print('completed')

    merge_files()
    clean_duplicates()

if __name__ == '__main__':
    main()