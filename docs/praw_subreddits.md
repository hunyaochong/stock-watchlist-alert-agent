Subreddit
class praw.models.Subreddit(reddit: praw.Reddit, display_name: str | None = None, _data: Dict[str, Any] | None = None)
A class for Subreddits.

To obtain an instance of this class for r/test execute:

subreddit = reddit.subreddit("test")
While r/all is not a real subreddit, it can still be treated like one. The following outputs the titles of the 25 hottest submissions in r/all:

for submission in reddit.subreddit("all").hot(limit=25):
    print(submission.title)
Multiple subreddits can be combined with a + like so:

for submission in reddit.subreddit("redditdev+learnpython").top(time_filter="all"):
    print(submission)
Subreddits can be filtered from combined listings as follows.

Note

These filters are ignored by certain methods, including comments, gilded(), and SubredditStream.comments().

for submission in reddit.subreddit("all-redditdev").new():
    print(submission)
Typical Attributes

Note

This table describes attributes that typically belong to objects of this class. PRAW dynamically provides the attributes that Reddit returns via the API. Since those attributes are subject to change on Reddit’s end, PRAW makes no effort to document any new/removed/changed attributes, other than to instruct you on how to discover what is available. As a result, this table of attributes may not be complete. See Determine Available Attributes of an Object for detailed information.

If you would like to add an attribute to this table, feel free to open a pull request.

Attribute

Description

can_assign_link_flair

Whether users can assign their own link flair.

can_assign_user_flair

Whether users can assign their own user flair.

created_utc

Time the subreddit was created, represented in Unix Time.

description

Subreddit description, in Markdown.

description_html

Subreddit description, in HTML.

display_name

Name of the subreddit.

id

ID of the subreddit.

name

Fullname of the subreddit.

over18

Whether the subreddit is NSFW.

public_description

Description of the subreddit, shown in searches and on the “You must be invited to visit this community” page (if applicable).

spoilers_enabled

Whether the spoiler tag feature is enabled.

subscribers

Count of subscribers.

user_is_banned

Whether the authenticated user is banned.

user_is_moderator

Whether the authenticated user is a moderator.

user_is_subscriber

Whether the authenticated user is subscribed.

Note

Trying to retrieve attributes of quarantined or private subreddits will result in a 403 error. Trying to retrieve attributes of a banned subreddit will result in a 404 error.

__init__(reddit: praw.Reddit, display_name: str | None = None, _data: Dict[str, Any] | None = None)
Initialize a Subreddit instance.

Parameters:
reddit – An instance of Reddit.

display_name – The name of the subreddit.

Note

This class should not be initialized directly. Instead, obtain an instance via: reddit.subreddit("test")

banned() → praw.models.reddit.subreddit.SubredditRelationship
Provide an instance of SubredditRelationship.

For example, to ban a user try:

reddit.subreddit("test").banned.add("spez", ban_reason="...")
To list the banned users along with any notes, try:

for ban in reddit.subreddit("test").banned():
    print(f"{ban}: {ban.note}")
collections() → praw.models.reddit.collections.SubredditCollections
Provide an instance of SubredditCollections.

To see the permalinks of all Collections that belong to a subreddit, try:

for collection in reddit.subreddit("test").collections:
    print(collection.permalink)
To get a specific Collection by its UUID or permalink, use one of the following:

collection = reddit.subreddit("test").collections("some_uuid")
collection = reddit.subreddit("test").collections(
    permalink="https://reddit.com/r/SUBREDDIT/collection/some_uuid"
)
comments() → CommentHelper
Provide an instance of CommentHelper.

For example, to output the author of the 25 most recent comments of r/test execute:

for comment in reddit.subreddit("test").comments(limit=25):
    print(comment.author)
contributor() → praw.models.reddit.subreddit.ContributorRelationship
Provide an instance of ContributorRelationship.

Contributors are also known as approved submitters.

To add a contributor try:

reddit.subreddit("test").contributor.add("spez")
controversial(*, time_filter: str = 'all', **generator_kwargs: str | int | Dict[str, str]) → Iterator[Any]
Return a ListingGenerator for controversial items.

Parameters:
time_filter – Can be one of: "all", "day", "hour", "month", "week", or "year" (default: "all").

Raises:
ValueError if time_filter is invalid.

Additional keyword arguments are passed in the initialization of ListingGenerator.

This method can be used like:

reddit.domain("imgur.com").controversial(time_filter="week")
reddit.multireddit(redditor="samuraisam", name="programming").controversial(
    time_filter="day"
)
reddit.redditor("spez").controversial(time_filter="month")
reddit.redditor("spez").comments.controversial(time_filter="year")
reddit.redditor("spez").submissions.controversial(time_filter="all")
reddit.subreddit("all").controversial(time_filter="hour")
emoji() → SubredditEmoji
Provide an instance of SubredditEmoji.

This attribute can be used to discover all emoji for a subreddit:

for emoji in reddit.subreddit("test").emoji:
    print(emoji)
A single emoji can be lazily retrieved via:

reddit.subreddit("test").emoji["emoji_name"]
Note

Attempting to access attributes of a nonexistent emoji will result in a ClientException.

filters() → praw.models.reddit.subreddit.SubredditFilters
Provide an instance of SubredditFilters.

For example, to add a filter, run:

reddit.subreddit("all").filters.add("test")
flair() → praw.models.reddit.subreddit.SubredditFlair
Provide an instance of SubredditFlair.

Use this attribute for interacting with a Subreddit’s flair. For example, to list all the flair for a subreddit which you have the flair moderator permission on try:

for flair in reddit.subreddit("test").flair():
    print(flair)
Flair templates can be interacted with through this attribute via:

for template in reddit.subreddit("test").flair.templates:
    print(template)
property fullname: str
Return the object’s fullname.

A fullname is an object’s kind mapping like t3 followed by an underscore and the object’s base36 ID, e.g., t1_c5s96e0.

gilded(**generator_kwargs: str | int | Dict[str, str]) → Iterator[Any]
Return a ListingGenerator for gilded items.

Additional keyword arguments are passed in the initialization of ListingGenerator.

For example, to get gilded items in r/test:

for item in reddit.subreddit("test").gilded():
    print(item.id)
hot(**generator_kwargs: str | int | Dict[str, str]) → Iterator[Any]
Return a ListingGenerator for hot items.

Additional keyword arguments are passed in the initialization of ListingGenerator.

This method can be used like:

reddit.domain("imgur.com").hot()
reddit.multireddit(redditor="samuraisam", name="programming").hot()
reddit.redditor("spez").hot()
reddit.redditor("spez").comments.hot()
reddit.redditor("spez").submissions.hot()
reddit.subreddit("all").hot()
message(*, from_subreddit: praw.models.Subreddit | str | None = None, message: str, subject: str)
Send a message to a Redditor or a Subreddit’s moderators (modmail).

Parameters:
from_subreddit –

A Subreddit instance or string to send the message from. When provided, messages are sent from the subreddit rather than from the authenticated user.

Note

The authenticated user must be a moderator of the subreddit and have the mail moderator permission.

message – The message content.

subject – The subject of the message.

For example, to send a private message to u/spez, try:

reddit.redditor("spez").message(subject="TEST", message="test message from PRAW")
To send a message to u/spez from the moderators of r/test try:

reddit.redditor("spez").message(
    subject="TEST", message="test message from r/test", from_subreddit="test"
)
To send a message to the moderators of r/test, try:

reddit.subreddit("test").message(subject="TEST", message="test PM from PRAW")
mod() → SubredditModeration
Provide an instance of SubredditModeration.

For example, to accept a moderation invite from r/test:

reddit.subreddit("test").mod.accept_invite()
moderator() → praw.models.reddit.subreddit.ModeratorRelationship
Provide an instance of ModeratorRelationship.

For example, to add a moderator try:

reddit.subreddit("test").moderator.add("spez")
To list the moderators along with their permissions try:

for moderator in reddit.subreddit("test").moderator():
    print(f"{moderator}: {moderator.mod_permissions}")
modmail() → praw.models.reddit.subreddit.Modmail
Provide an instance of Modmail.

For example, to send a new modmail from r/test to u/spez with the subject "test" along with a message body of "hello":

reddit.subreddit("test").modmail.create(subject="test", body="hello", recipient="spez")
muted() → praw.models.reddit.subreddit.SubredditRelationship
Provide an instance of SubredditRelationship.

For example, muted users can be iterated through like so:

for mute in reddit.subreddit("test").muted():
    print(f"{mute}: {mute.date}")
new(**generator_kwargs: str | int | Dict[str, str]) → Iterator[Any]
Return a ListingGenerator for new items.

Additional keyword arguments are passed in the initialization of ListingGenerator.

This method can be used like:

reddit.domain("imgur.com").new()
reddit.multireddit(redditor="samuraisam", name="programming").new()
reddit.redditor("spez").new()
reddit.redditor("spez").comments.new()
reddit.redditor("spez").submissions.new()
reddit.subreddit("all").new()
classmethod parse(data: Dict[str, Any], reddit: praw.Reddit) → Any
Return an instance of cls from data.

Parameters:
data – The structured data.

reddit – An instance of Reddit.

post_requirements() → Dict[str, str | int | bool]
Get the post requirements for a subreddit.

Returns:
A dict with the various requirements.

The returned dict contains the following keys:

domain_blacklist

body_restriction_policy

domain_whitelist

title_regexes

body_blacklisted_strings

body_required_strings

title_text_min_length

is_flair_required

title_text_max_length

body_regexes

link_repost_age

body_text_min_length

link_restriction_policy

body_text_max_length

title_required_strings

title_blacklisted_strings

guidelines_text

guidelines_display_policy

For example, to fetch the post requirements for r/test:

print(reddit.subreddit("test").post_requirements)
quaran() → praw.models.reddit.subreddit.SubredditQuarantine
Provide an instance of SubredditQuarantine.

This property is named quaran because quarantine is a subreddit attribute returned by Reddit to indicate whether or not a subreddit is quarantined.

To opt-in into a quarantined subreddit:

reddit.subreddit("test").quaran.opt_in()
random() → praw.models.Submission | None
Return a random Submission.

Returns None on subreddits that do not support the random feature. One example, at the time of writing, is r/wallpapers.

For example, to get a random submission off of r/AskReddit:

submission = reddit.subreddit("AskReddit").random()
print(submission.title)
random_rising(**generator_kwargs: str | int | Dict[str, str]) → Iterator[praw.models.Submission]
Return a ListingGenerator for random rising submissions.

Additional keyword arguments are passed in the initialization of ListingGenerator.

For example, to get random rising submissions for r/test:

for submission in reddit.subreddit("test").random_rising():
    print(submission.title)
rising(**generator_kwargs: str | int | Dict[str, str]) → Iterator[praw.models.Submission]
Return a ListingGenerator for rising submissions.

Additional keyword arguments are passed in the initialization of ListingGenerator.

For example, to get rising submissions for r/test:

for submission in reddit.subreddit("test").rising():
    print(submission.title)
rules() → SubredditRules
Provide an instance of SubredditRules.

Use this attribute for interacting with a Subreddit’s rules.

For example, to list all the rules for a subreddit:

for rule in reddit.subreddit("test").rules:
    print(rule)
Moderators can also add rules to the subreddit. For example, to make a rule called "No spam" in r/test:

reddit.subreddit("test").rules.mod.add(
    short_name="No spam", kind="all", description="Do not spam. Spam bad"
)
search(query: str, *, sort: str = 'relevance', syntax: str = 'lucene', time_filter: str = 'all', **generator_kwargs: Any) → Iterator[praw.models.Submission]
Return a ListingGenerator for items that match query.

Parameters:
query – The query string to search for.

sort – Can be one of: "relevance", "hot", "top", "new", or "comments". (default: "relevance").

syntax – Can be one of: "cloudsearch", "lucene", or "plain" (default: "lucene").

time_filter – Can be one of: "all", "day", "hour", "month", "week", or "year" (default: "all").

For more information on building a search query see: https://www.reddit.com/wiki/search

For example, to search all subreddits for "praw" try:

for submission in reddit.subreddit("all").search("praw"):
    print(submission.title)
sticky(*, number: int = 1) → praw.models.Submission
Return a Submission object for a sticky of the subreddit.

Parameters:
number – Specify which sticky to return. 1 appears at the top (default: 1).

Raises:
prawcore.NotFound if the sticky does not exist.

For example, to get the stickied post on r/test:

reddit.subreddit("test").sticky()
stream() → praw.models.reddit.subreddit.SubredditStream
Provide an instance of SubredditStream.

Streams can be used to indefinitely retrieve new comments made to a subreddit, like:

for comment in reddit.subreddit("test").stream.comments():
    print(comment)
Additionally, new submissions can be retrieved via the stream. In the following example all submissions are fetched via the special r/all:

for submission in reddit.subreddit("all").stream.submissions():
    print(submission)
stylesheet() → praw.models.reddit.subreddit.SubredditStylesheet
Provide an instance of SubredditStylesheet.

For example, to add the css data .test{color:blue} to the existing stylesheet:

subreddit = reddit.subreddit("test")
stylesheet = subreddit.stylesheet()
stylesheet.stylesheet += ".test{color:blue}"
subreddit.stylesheet.update(stylesheet.stylesheet)
submit(title: str, *, collection_id: str | None = None, discussion_type: str | None = None, draft_id: str | None = None, flair_id: str | None = None, flair_text: str | None = None, inline_media: Dict[str, praw.models.InlineMedia] | None = None, nsfw: bool = False, resubmit: bool = True, selftext: str | None = None, send_replies: bool = True, spoiler: bool = False, url: str | None = None) → praw.models.Submission
Add a submission to the Subreddit.

Parameters:
title – The title of the submission.

collection_id – The UUID of a Collection to add the newly-submitted post to.

discussion_type – Set to "CHAT" to enable live discussion instead of traditional comments (default: None).

draft_id – The ID of a draft to submit.

flair_id – The flair template to select (default: None).

flair_text – If the template’s flair_text_editable value is True, this value will set a custom text (default: None). flair_id is required when flair_text is provided.

inline_media – A dict of InlineMedia objects where the key is the placeholder name in selftext.

nsfw – Whether the submission should be marked NSFW (default: False).

resubmit – When False, an error will occur if the URL has already been submitted (default: True).

selftext – The Markdown formatted content for a text submission. Use an empty string, "", to make a title-only submission.

send_replies – When True, messages will be sent to the submission author when comments are made to the submission (default: True).

spoiler – Whether the submission should be marked as a spoiler (default: False).

url – The URL for a link submission.

Returns:
A Submission object for the newly created submission.

Either selftext or url can be provided, but not both.

For example, to submit a URL to r/test do:

title = "PRAW documentation"
url = "https://praw.readthedocs.io"
reddit.subreddit("test").submit(title, url=url)
For example, to submit a self post with inline media do:

from praw.models import InlineGif, InlineImage, InlineVideo

gif = InlineGif(path="path/to/image.gif", caption="optional caption")
image = InlineImage(path="path/to/image.jpg", caption="optional caption")
video = InlineVideo(path="path/to/video.mp4", caption="optional caption")
selftext = "Text with a gif {gif1} an image {image1} and a video {video1} inline"
media = {"gif1": gif, "image1": image, "video1": video}
reddit.subreddit("test").submit("title", inline_media=media, selftext=selftext)
Note

Inserted media will have a padding of \\n\\n automatically added. This is due to the weirdness with Reddit’s API. Using the example above, the result selftext body will look like so:

Text with a gif

![gif](u1rchuphryq51 "optional caption")

an image

![img](srnr8tshryq51 "optional caption")

and video

![video](gmc7rvthryq51 "optional caption")

inline
Note

To submit a post to a subreddit with the "news" flair, you can get the flair id like this:

choices = list(subreddit.flair.link_templates.user_selectable())
template_id = next(x for x in choices if x["flair_text"] == "news")["flair_template_id"]
subreddit.submit("title", flair_id=template_id, url="https://www.news.com/")
See also

submit_gallery() to submit more than one image in the same post

submit_image() to submit images

submit_poll() to submit polls

submit_video() to submit videos and videogifs

submit_gallery(title: str, images: List[Dict[str, str]], *, collection_id: str | None = None, discussion_type: str | None = None, flair_id: str | None = None, flair_text: str | None = None, nsfw: bool = False, send_replies: bool = True, spoiler: bool = False)
Add an image gallery submission to the subreddit.

Parameters:
title – The title of the submission.

images – The images to post in dict with the following structure: {"image_path": "path", "caption": "caption", "outbound_url": "url"}, only image_path is required.

collection_id – The UUID of a Collection to add the newly-submitted post to.

discussion_type – Set to "CHAT" to enable live discussion instead of traditional comments (default: None).

flair_id – The flair template to select (default: None).

flair_text – If the template’s flair_text_editable value is True, this value will set a custom text (default: None). flair_id is required when flair_text is provided.

nsfw – Whether the submission should be marked NSFW (default: False).

send_replies – When True, messages will be sent to the submission author when comments are made to the submission (default: True).

spoiler – Whether the submission should be marked asa spoiler (default: False).

Returns:
A Submission object for the newly created submission.

Raises:
ClientException if image_path in images refers to a file that is not an image.

For example, to submit an image gallery to r/test do:

title = "My favorite pictures"
image = "/path/to/image.png"
image2 = "/path/to/image2.png"
image3 = "/path/to/image3.png"
images = [
    {"image_path": image},
    {
        "image_path": image2,
        "caption": "Image caption 2",
    },
    {
        "image_path": image3,
        "caption": "Image caption 3",
        "outbound_url": "https://example.com/link3",
    },
]
reddit.subreddit("test").submit_gallery(title, images)
See also

submit() to submit url posts and selftexts

submit_image() to submit single images

submit_poll() to submit polls

submit_video() to submit videos and videogifs

submit_image(title: str, image_path: str, *, collection_id: str | None = None, discussion_type: str | None = None, flair_id: str | None = None, flair_text: str | None = None, nsfw: bool = False, resubmit: bool = True, send_replies: bool = True, spoiler: bool = False, timeout: int = 10, without_websockets: bool = False)
Add an image submission to the subreddit.

Parameters:
collection_id – The UUID of a Collection to add the newly-submitted post to.

discussion_type – Set to "CHAT" to enable live discussion instead of traditional comments (default: None).

flair_id – The flair template to select (default: None).

flair_text – If the template’s flair_text_editable value is True, this value will set a custom text (default: None). flair_id is required when flair_text is provided.

image_path – The path to an image, to upload and post.

nsfw – Whether the submission should be marked NSFW (default: False).

resubmit – When False, an error will occur if the URL has already been submitted (default: True).

send_replies – When True, messages will be sent to the submission author when comments are made to the submission (default: True).

spoiler – Whether the submission should be marked as a spoiler (default: False).

timeout – Specifies a particular timeout, in seconds. Use to avoid “Websocket error” exceptions (default: 10).

title – The title of the submission.

without_websockets – Set to True to disable use of WebSockets (see note below for an explanation). If True, this method doesn’t return anything (default: False).

Returns:
A Submission object for the newly created submission, unless without_websockets is True.

Raises:
ClientException if image_path refers to a file that is not an image.

Note

Reddit’s API uses WebSockets to respond with the link of the newly created post. If this fails, the method will raise WebSocketException. Occasionally, the Reddit post will still be created. More often, there is an error with the image file. If you frequently get exceptions but successfully created posts, try setting the timeout parameter to a value above 10.

To disable the use of WebSockets, set without_websockets=True. This will make the method return None, though the post will still be created. You may wish to do this if you are running your program in a restricted network environment, or using a proxy that doesn’t support WebSockets connections.

For example, to submit an image to r/test do:

title = "My favorite picture"
image = "/path/to/image.png"
reddit.subreddit("test").submit_image(title, image)
See also

submit() to submit url posts and selftexts

submit_gallery() to submit more than one image in the same post

submit_poll() to submit polls

submit_video() to submit videos and videogifs

submit_poll(title: str, *, collection_id: str | None = None, discussion_type: str | None = None, duration: int, flair_id: str | None = None, flair_text: str | None = None, nsfw: bool = False, options: List[str], resubmit: bool = True, selftext: str, send_replies: bool = True, spoiler: bool = False)
Add a poll submission to the subreddit.

Parameters:
title – The title of the submission.

collection_id – The UUID of a Collection to add the newly-submitted post to.

discussion_type – Set to "CHAT" to enable live discussion instead of traditional comments (default: None).

duration – The number of days the poll should accept votes, as an int. Valid values are between 1 and 7, inclusive.

flair_id – The flair template to select (default: None).

flair_text – If the template’s flair_text_editable value is True, this value will set a custom text (default: None). flair_id is required when flair_text is provided.

nsfw – Whether the submission should be marked NSFW (default: False).

options – A list of two to six poll options as str.

resubmit – When False, an error will occur if the URL has already been submitted (default: True).

selftext – The Markdown formatted content for the submission. Use an empty string, "", to make a submission with no text contents.

send_replies – When True, messages will be sent to the submission author when comments are made to the submission (default: True).

spoiler – Whether the submission should be marked as a spoiler (default: False).

Returns:
A Submission object for the newly created submission.

For example, to submit a poll to r/test do:

title = "Do you like PRAW?"
reddit.subreddit("test").submit_poll(
    title, selftext="", options=["Yes", "No"], duration=3
)
See also

submit() to submit url posts and selftexts

submit_gallery() to submit more than one image in the same post

submit_image() to submit single images

submit_video() to submit videos and videogifs

submit_video(title: str, video_path: str, *, collection_id: str | None = None, discussion_type: str | None = None, flair_id: str | None = None, flair_text: str | None = None, nsfw: bool = False, resubmit: bool = True, send_replies: bool = True, spoiler: bool = False, thumbnail_path: str | None = None, timeout: int = 10, videogif: bool = False, without_websockets: bool = False)
Add a video or videogif submission to the subreddit.

Parameters:
title – The title of the submission.

video_path – The path to a video, to upload and post.

collection_id – The UUID of a Collection to add the newly-submitted post to.

discussion_type – Set to "CHAT" to enable live discussion instead of traditional comments (default: None).

flair_id – The flair template to select (default: None).

flair_text – If the template’s flair_text_editable value is True, this value will set a custom text (default: None). flair_id is required when flair_text is provided.

nsfw – Whether the submission should be marked NSFW (default: False).

resubmit – When False, an error will occur if the URL has already been submitted (default: True).

send_replies – When True, messages will be sent to the submission author when comments are made to the submission (default: True).

spoiler – Whether the submission should be marked as a spoiler (default: False).

thumbnail_path – The path to an image, to be uploaded and used as the thumbnail for this video. If not provided, the PRAW logo will be used as the thumbnail.

timeout – Specifies a particular timeout, in seconds. Use to avoid “Websocket error” exceptions (default: 10).

videogif – If True, the video is uploaded as a videogif, which is essentially a silent video (default: False).

without_websockets – Set to True to disable use of WebSockets (see note below for an explanation). If True, this method doesn’t return anything (default: False).

Returns:
A Submission object for the newly created submission, unless without_websockets is True.

Raises:
ClientException if video_path refers to a file that is not a video.

Note

Reddit’s API uses WebSockets to respond with the link of the newly created post. If this fails, the method will raise WebSocketException. Occasionally, the Reddit post will still be created. More often, there is an error with the image file. If you frequently get exceptions but successfully created posts, try setting the timeout parameter to a value above 10.

To disable the use of WebSockets, set without_websockets=True. This will make the method return None, though the post will still be created. You may wish to do this if you are running your program in a restricted network environment, or using a proxy that doesn’t support WebSockets connections.

For example, to submit a video to r/test do:

title = "My favorite movie"
video = "/path/to/video.mp4"
reddit.subreddit("test").submit_video(title, video)
See also

submit() to submit url posts and selftexts

submit_image() to submit images

submit_gallery() to submit more than one image in the same post

submit_poll() to submit polls

subscribe(*, other_subreddits: List[praw.models.Subreddit] | None = None)
Subscribe to the subreddit.

Parameters:
other_subreddits – When provided, also subscribe to the provided list of subreddits.

For example, to subscribe to r/test:

reddit.subreddit("test").subscribe()
top(*, time_filter: str = 'all', **generator_kwargs: str | int | Dict[str, str]) → Iterator[Any]
Return a ListingGenerator for top items.

Parameters:
time_filter – Can be one of: "all", "day", "hour", "month", "week", or "year" (default: "all").

Raises:
ValueError if time_filter is invalid.

Additional keyword arguments are passed in the initialization of ListingGenerator.

This method can be used like:

reddit.domain("imgur.com").top(time_filter="week")
reddit.multireddit(redditor="samuraisam", name="programming").top(time_filter="day")
reddit.redditor("spez").top(time_filter="month")
reddit.redditor("spez").comments.top(time_filter="year")
reddit.redditor("spez").submissions.top(time_filter="all")
reddit.subreddit("all").top(time_filter="hour")
traffic() → Dict[str, List[List[int]]]
Return a dictionary of the Subreddit’s traffic statistics.

Raises:
prawcore.NotFound when the traffic stats aren’t available to the authenticated user, that is, they are not public and the authenticated user is not a moderator of the subreddit.

The traffic method returns a dict with three keys. The keys are day, hour and month. Each key contains a list of lists with 3 or 4 values. The first value is a timestamp indicating the start of the category (start of the day for the day key, start of the hour for the hour key, etc.). The second, third, and fourth values indicate the unique pageviews, total pageviews, and subscribers, respectively.

Note

The hour key does not contain subscribers, and therefore each sub-list contains three values.

For example, to get the traffic stats for r/test:

stats = reddit.subreddit("test").traffic()
unsubscribe(*, other_subreddits: List[praw.models.Subreddit] | None = None)
Unsubscribe from the subreddit.

Parameters:
other_subreddits – When provided, also unsubscribe from the provided list of subreddits.

To unsubscribe from r/test:

reddit.subreddit("test").unsubscribe()
widgets() → praw.models.SubredditWidgets
Provide an instance of SubredditWidgets.

Example usage

Get all sidebar widgets:

for widget in reddit.subreddit("test").widgets.sidebar:
    print(widget)
Get ID card widget:

print(reddit.subreddit("test").widgets.id_card)
wiki() → praw.models.reddit.subreddit.SubredditWiki
Provide an instance of SubredditWiki.

This attribute can be used to discover all wikipages for a subreddit:

for wikipage in reddit.subreddit("test").wiki:
    print(wikipage)
To fetch the content for a given wikipage try:

wikipage = reddit.subreddit("test").wiki["proof"]
print(wikipage.content_md)