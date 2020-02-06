# Saved Archiver for Reddit
## Introduction
Only 1000 combined saved comments and posts may be saved at one time per Reddit account. As new content is saved, old content is lost. This script allows you to archive all of your current saved posts and comments into a single file, as well as download all images and gifs hosted on Imgur.
## Setup
In 'archiver.py', the following fields must be edited to allow the script access to your saved posts:
```python
reddit = praw.Reddit(client_id='<client_id>', \
                     client_secret='<client_secret>', \
                     user_agent='<script_name>', \
                     username='<username>', \
                     password='<password>')
```
To start, login to Reddit and navigate to https://www.reddit.com/prefs/apps/
Next, click 'Create App'. You should see the following screen:
![alt text](https://i.imgur.com/P5Ff2qv.png "Reddit application creation screen")
Now, name your application 'Saved Archiver for Reddit', select 'script', and list the about url
to whatever you'd like (feel free to use this github page). We don't need a redirect url, but
Reddit makes us provide one anyway. An easy one to use is http://localhost:8080
When you've finished filling out the form, click 'Create App'.

Now, you should see your app at the top of the page:
![alt text](https://i.imgur.com/JV14cBM.png "Our app")
Fill in the fields in archiver.py with the values shown here. 

We now need to register for API use. Navigate to https://www.reddit.com/wiki/api
and click the link at the bottom 'Read the full API terms and sign up for usage'.
You will be redirected to a Google form. Fill out the fields as directed. Make
sure to fill in the following field with your **client_id value** from the previous screen:
![alt text](https://i.imgur.com/tHe6rCT.png "Your client_id can be found in https://www.reddit.com/prefs/apps/")

We're almost done! The last step is to change the username and password fields in
'archiver.py' to match those of the account you used to setup API access.

*Note: Saved Archiver does not save or transmit this information to anyone other than
Reddit.com. Even so, you should always be cautious when using scripts obtained from the internet,
and ensure that you understand exactly how your credentials are being used. For more information
visit https://praw.readthedocs.io/en/latest/getting_started/authentication.html*

Now that we've finished setup, open a Powershell window in the directory containing
'archive.py' and 'imgurdownloader.py'. Run the script with the command:
```
python archiver.py
```
When the script has completed execution, you should see a file named 'saved.txt' that contains
all saved comments and posts with urls, and a folder named 'images' that has grouped saved imgur/reddit
links by reddit username. 

## Known Issues
todo
