# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 18:45:40 2018

@author: Image17
"""

import sys
import praw
import config
import csv
import glob

"""
Login to reddit through praw to provide a session for the scraper
"""
def login():
    session = praw.Reddit(username = config.username,
                password = config.password,
                client_id = config.client_id,
                client_secret = config.client_secret,
                user_agent = config.user_agent)
    return session
    
"""
Scrape subreddit s of as money comments as possible and write to a specific file
"""
def scrape(s):
    comments=[]
    r = login()
    for comment in r.subreddit(s).comments(limit=10000):
        cmmt = []
        # attain variables from prraw comment
        create_timestamp = str(comment.created_utc)
        author_name = comment.author.name
        # when accessing the comment body from the csv you must decode with utf8
        comment_body = str(comment.body.encode('utf8'))
        # clean each piece of data individually if necessary
        
        # add to list to be written to a file
        cmmt.append(create_timestamp)
        cmmt.append(author_name)
        cmmt.append(comment_body)
        comments.append(cmmt)
    # write list to file
    with open('reddit/reddit-data-'+s+'.csv', mode='w', newline='') as reddit_data:
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
    files = glob.glob("reddit/*.*")
    for file in files:
        print('cleaning '+file)
        comments=[]
        with open(file, newline='', encoding='UTF-8-sig') as csvfile:
            spamreader = csv.reader(csvfile, delimiter='|')
            for row in spamreader:
                comment=[]
                if row not in comments:
                    for i in row:
                        comment.append(i)
                    comments.append(comment)
        print(len(comments))
        
        with open (file, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter='|')
            csvfile.truncate()
            for c in comments:
                csv_writer.writerow(c)

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

if __name__ == '__main__':
    main()