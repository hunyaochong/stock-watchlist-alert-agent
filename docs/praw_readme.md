PRAW: The Python Reddit API Wrapper

PRAW, an acronym for "Python Reddit API Wrapper", is a Python package that allows for simple access to Reddit's API. PRAW aims to be easy to use and internally follows all of Reddit's API rules. With PRAW there's no need to introduce sleep calls in your code. Give your client an appropriate user agent and you're set.

Installation
PRAW is supported on Python 3.9+. The recommended way to install PRAW is via pip.

pip install praw
To install the latest development version of PRAW run the following instead:

pip install --upgrade https://github.com/praw-dev/praw/archive/main.zip
For instructions on installing Python and pip see "The Hitchhiker's Guide to Python" Installation Guides.

Quickstart
Assuming you already have a credentials for a script-type OAuth application you can instantiate an instance of PRAW like so:

import praw

reddit = praw.Reddit(
    client_id="CLIENT_ID",
    client_secret="CLIENT_SECRET",
    password="PASSWORD",
    user_agent="USERAGENT",
    username="USERNAME",
)
With the reddit instance you can then interact with Reddit:

# Create a submission to r/test
reddit.subreddit("test").submit("Test Submission", url="https://reddit.com")

# Comment on a known submission
submission = reddit.submission(url="https://www.reddit.com/comments/5e1az9")
submission.reply("Super rad!")

# Reply to the first comment of a weekly top thread of a moderated community
submission = next(reddit.subreddit("mod").top(time_filter="week"))
submission.comments[0].reply("An automated reply")

# Output score for the first 256 items on the frontpage
for submission in reddit.front.hot(limit=256):
    print(submission.score)

# Obtain the moderator listing for r/test
for moderator in reddit.subreddit("test").moderator():
    print(moderator)
Please see PRAW's documentation for more examples of what you can do with PRAW.

Discord Bots and Asynchronous Environments
If you plan on using PRAW in an asynchronous environment, (e.g., discord.py, asyncio) it is strongly recommended to use Async PRAW. It is the official asynchronous version of PRAW and its usage is similar and has the same features as PRAW.

PRAW Discussion and Support
For those new to Python, or would otherwise consider themselves a Python beginner, please consider asking questions on the r/learnpython subreddit. There are wonderful people there who can help with general Python and simple PRAW related questions.

Otherwise, there are a few official places to ask questions about PRAW:

r/redditdev is the best place on Reddit to ask PRAW related questions. This subreddit is for all Reddit API related discussion so please tag submissions with [PRAW]. Please perform a search on the subreddit first to see if anyone has similar questions.

Real-time chat can be conducted via the PRAW Slack Organization (please create an issue if that invite link has expired).

Please do not directly message any of the contributors via Reddit, email, or Slack unless they have indicated otherwise. We strongly encourage everyone to help others with their questions.

Please file bugs and feature requests as issues on GitHub after first searching to ensure a similar issue was not already filed. If such an issue already exists please give it a thumbs up reaction. Comments to issues containing additional information are certainly welcome.

Note

This project is released with a Contributor Code of Conduct. By participating in this project you agree to abide by its terms.

Documentation
PRAW's documentation is located at https://praw.readthedocs.io/.

History
August 2010: Timothy Mellor created a github project called reddit_api.

March 2011: The Python package reddit was registered and uploaded to pypi.

December 2011: Bryce Boe took over as maintainer of the reddit package.

June 2012: Bryce renamed the project PRAW and the repository was relocated to the newly created praw-dev organization on GitHub.

February 2016: Bryce began work on PRAW4, a complete rewrite of PRAW.

License
PRAW's source (v4.0.0+) is provided under the Simplified BSD License.

Copyright ©, 2016, Bryce Boe
Earlier versions of PRAW were released under GPLv3.