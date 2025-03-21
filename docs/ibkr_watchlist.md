Market DataCopy Location
In order to retrieve top-of-book, depth-of-book, or historical market data from the Web API, the following must be available:

Username with relevant live market data subscriptions and permission to trade the desired instruments
Authorized Web API session
Brokerage session (access to IServer endpoints)




Retrieve All Saved Watchlists Stored On IB Backend For The Username In Use In The Current Web API Session.

get
/iserver/watchlists


Retrieve all saved watchlists stored on IB backend for the username in use in the current Web API session.

query Parameters
SC	
string
Value: "USER_WATCHLIST"
Example: SC=USER_WATCHLIST
Can only be used with value USER_WATCHLIST, which returns only user-created watchlists and excludes those created by IB.

Responses
200 Historical data query successfully returned data.
Response Schema: application/json
data	
object
Contains the watchlist query results.

scanners_only	
boolean
Indicates if query results contain only market scanners.

show_scanners	
boolean
Indicates if market scanners are included in query results.

bulk_delete	
boolean
Indicates if username's watchlists can be bulk-deleted.

user_lists	
Array of objects
Array of objects detailing the watchlists saved for the username in use in the current Web API session.

Array 
is_open	
boolean
Internal use. Indicates if the watchlist is currently in use.

read_only	
boolean
Indicates if the watchlist can be edited.

name	
string
Display name of the watchlist.

modified	
integer <int32>
Unix timestamp in milliseconds of the last modification of the watchlist.

id	
string
Watchlist ID of the watchlist.

type	
string
Value: "watchlist"
Always has value 'watchlist'.

action	
string
Value: "content"
Internal use. Always has value 'content'.

MID	
string
Internal use. Number of times endpoint has been visited during session.

401 access denied
500 internal server error, returned when incoming request cannot be processed. It can sometimes include subset of bad requests. For example, wrong accountId passed and it can only be detected later in handling request. Error contains reason of the problem.
503 service is unavailable. For example if request takes more than 10s due to some internal service unavailability, request aborted and this status returned



Retrieve Details Of A Single Watchlist Stored In The Username's Settings.

get
/iserver/watchlist


Retrieve details of a single watchlist stored in the username's settings.

query Parameters
id
required
string
Example: id=1234
Watchlist ID of the requested watchlist.

Responses
200 Successful deletion of specified watchlist.
Response Schema: application/json
id	
string
Identifier of the watchlist.

hash	
string
Internal use. Unique hash of the watchlist.

name	
string
Human-readable display name of the watchlist.

readOnly	
boolean
Indicates whether the watchlist can be edited.

instruments	
Array of objects (singleWatchlistEntry)
Array of instruments contained in the watchlist.

Array 
ST	
string
Enum: "STK" "OPT" "FUT" "BOND" "FUND" "WAR" "CASH" "CRYPTO"
All-capital, shorthand security type identifier of the instrument.

C	
string
Instrument conid as a string.

conid	
integer <int32>
IB contract ID of the instrument.

name	
string
Complete display name of the instrument.

fullName	
string
Full display presentation of the instrument symbol.

assetClass	
string
Enum: "STK" "OPT" "FUT" "BOND" "FUND" "WAR" "CASH" "CRYPTO"
All-capital, shorthand security type identifier of the instrument.

ticker	
string
Symbol of the instrument.

chineseName	
string
Rendering of the instrument name in Chinese.

400 bad request
401 access denied
500 internal server error, returned when incoming request cannot be processed. It can sometimes include subset of bad requests. For example, wrong accountId passed and it can only be detected later in handling request. Error contains reason of the problem.
503 service is unavailable. For example if request takes more than 10s due to some internal service unavailability, request aborted and this status returned
