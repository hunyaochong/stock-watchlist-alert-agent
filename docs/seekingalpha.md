Version in use: free
- 500 requests per month
- 5 requests per second
- Program should be able to meet the above limits (program will be set to run once a day)

The Seeking Alpha API Endpoints
The Seeking Alpha API provides a lot of endpoints, including a default endpoint. These endpoints belong to 9 categories.

Market
Symbol
Analysis
Article
News
Press Release
Transcript
Author 
Comment
Default endpoint – GET /auto-complete
You can get suggested companies, authors, web pages, and queries for a particular search term from this endpoint. Therefore, you should include the search term in its mandatory ‘term’ parameter. The output consists of the following JSON object arrays.

symbols – Each company in the stock market has a symbol of recognizing it uniquely. For example,
AAPL – Apple Incorporation, FB – Facebook, NFLX – Netflix incorporation 

So if you include the search term as ‘apple,’ then this object would return’ companies whose name has that term

people – This object contains the list of suggested authors having the search term in their names.
pages – A list of URLs of web pages in the Seeking Alpha site having that search term. For example, if you search ‘portfolio,’ it will list both “investing-strategy/portfolio-strategy” and “account/portfolio” pages of the Seeking Alpha site.
query – Returns the query term.
Now, let’s take a look at the endpoints of each category.

Market
Market endpoints give you market information like market equities, real-time stock prices, dividend investing, etc. The following tables display all the endpoints and descriptions of their parameters. 

Endpoints
Endpoint	Usage	Parameters
Required

/market​/get-market-open	Get market open	–
/market/get-equity	Get different market equities	filterCategory
/market/get-day-watch	Get market day watch	–
/market/get-dividend-investing	Get dividend investing	–
/market/get-realtime-prices	Get real-time prices	symbols
Parameter definitions
Parameter	Description	Values
filterCategory	Type of market equity 	us-equity-markets        
us-equity-sectors            

us-equity-factors                 

global-equity                  

countries-equity

symbols	Symbols of the companies	Ex: AAPL, FB
Symbol
Symbol endpoints provide a list of essential data about the companies of your choice. For example, you can get information like company metadata, revenue estimations, data for stock charts, summary, fundamentals, momentum, company ratings, dividend histories, valuations, etc. Following is the summary of its endpoints and parameters.

Endpoints
Endpoint	Usage	Required parameters	Optional parameters
/symbols/get-meta-data	Get metadata of specific symbol	symbol	–
/symbols/get-estimates	Get estimated EPS/revenue of specific symbol by annual or quarterly	symbol	Data_type period_type
/symbols/get-chart	Get data to draw a chart for a specific symbol	symbol	period
/symbols/get-fundamentals	Get fundamentals for a specific symbol	symbol	Limit period_type
/symbols/get-key-data	Get key data of specific symbol	symbol	–
/symbols/get-ratings	Get ratings data for a specific symbol	symbol	–
/symbols/get-valuation	Get a valuation of a specific symbol	symbols	–
/symbols/get-momentum	Get momentum of the specific symbol	symbols	–
/symbols/get-peers	Get peers of a specific symbol	symbol	
/symbols/get-dividend-history	Get dividend history of the specific symbol	symbol	Years   group_by
/symbols/get-summary	Get summary information of specific symbol	symbols	–
/symbols/get-profile	Get profile information of specific symbol	symbols	–
 

Parameter definitions
Parameter	Description	Values
symbol	Symbol of the company, only one is allowed at a time.	Ex: AAPL
symbols	Symbols of the list of companies. Separating by comma to query multiple characters at once	Ex: AAPL, FB
data_type	Type pf estimations	eps|revenues
period	The period for stock charts	1D    
5D 

1M

6M

1Y

5Y

10Y

MAX

period_type	Period for which you need estimations 	quarterly         
annual

limit	How many records you want	Ex: 5
years	no of years	Ex: 6
group_by	group by year or month	year
month

Analysis
Seeking Alpha publishes analysis articles about various topics. You can use analysis endpoints to retrieve information about them. From its /analysis/list endpoint, you can get a list of analysis articles. The response contains an id for each piece. You can get more details about each article using that id using its /analysis/get-details endpoint. Refer to the following tables about the endpoints and parameters. 

Endpoints
Endpoint	Usage	Required Parameters	Optional Parameters
/analysis/get-details	Get analysis detail by id	id	–
/analysis/list	List analysis of the specific symbol	id	until         
size

 

Parameter definitions
Parameter	Description
id in /analysis/get-details	The value of id returned in …/analysis/list endpoint
id in /analysis/list	Symbol of the company, only one is allowed at a time.
until	The value of meta/page/minmaxPublishOn/min json object returned right in this endpoint to load next page
size	The number of items per response
Articles
Article endpoints provide various articles such as the latest articles, editor’s picks, dividends, investing strategies, etc. 

Endpoints
Endpoint	Usage	Required Parameters	Optional Parameters
/articles/list	List articles by category	category	until                 
size

/articles/get-details	Get analysis detail by id	id	–
/articles/list-wall-street-breakfast	List articles by category	–	–
/articles/list-trending	List trending articles	–	–
Parameter definitions
Parameter	Description	Values
id	The value of id returned in …/analysis/list endpoint.	–
category	Article category	Etfs-and-funds  
latest-articles

Stock-ideas

Editors-picks

Stock-ideas::editors-picks

Dividends

Investing-strategy

Dividends::reits

Podcast

market-outlook

 
News
These endpoints retrieve the latest and trending stock news and a list of news about a specific company.

Endpoints
Endpoint	Usage	Parameters
Required	Optional
/news/list-trending	List latest trending news	–	–
/news/list	List news of specific symbol	id	until,             
size

/news/get-details	Get analysis detail by id	id	–
Parameter definitions
Parameter	Description
Id in /news/list	Symbol to query for data, only one is allowed at a time
Id in /news/get-details	The value of id returned in …/news/list or …/news/list-trending endpoint
until	The value of meta/page/minmaxPublishOn/min json object returned right in this endpoint to load next page
size	The number of items per response
Pre-release
Press-release endpoints provide press releases of a specific company, and they allow you to search for details about any particular press release using its id. The below table gives you a description of each of its endpoints. Parameters are similar to ‘News’ endpoints.

Endpoints
Endpoint	Usage	Parameters
Required	Optional
/press-releases/get-details	Get press release detail by id	id	
/press-releases/list	List press releases of a specific symbol	id	until     
size

Transcript
You can get a list of transcripts of a specific company and get more details about a particular transcript using transcript endpoints. 

Endpoints
Endpoint	Usage	Parameters
Required	Optional
/transcripts/get-details	Get transcript detail by id	id	–
/transcripts/list	List transcripts of the specific symbol	id	until
size

Author – GET /authors/get-details
This endpoint is used to get details about a particular author. It requires you to specify the parameter ‘slug’, which identifies the author. You should use the value of the slug parameter in the ‘people’ JSON object returned from the GET /auto-complete endpoint.

Comment – GET /comments/list
This endpoint lists all comments relating to a post or article, or news. 

Parameter definitions
Parameter	Description
Id 	Mandatory Parameter. The value of the id returned in …/articles/list or …/articles/list-trending or …/articles/list-wall-street-breakfast endpoints
from_id  	Comment id
parent_count 	Maximum data for paging purpose
sort	Order by newest or oldest. For ordering by the latest comment, use the value ‘-top_parent_id.’ Otherwise, just leave it empty.
Integrating the Seeking Alpha API to an Application
This section will show you how to integrate the Seeking Alpha API  into Python, PHP, Ruby, and Javascript software applications with sample code snippets. For this instance, we will be using the “GET auto-complete” endpoint for all the languages. In each code, you need to include the ‘X-RapidAPI-key and X-RapidAPI-host parameters in the header, which you can obtain from the API page.

Python Code Snippet (requests)

First, you need to install the requests module on your computer. Then, specify all the parameters in the “querystring” variable. Finally, the request object’s request method sends the API call. 

import requests
 
url = "https://seeking-alpha.p.rapidapi.com/auto-complete"
querystring = {"term":"apple"}
headers = {
    'x-rapidapi-key': "cJvLRNK0GfdM9WSMbQe3inU7REn8JVy5",
    'x-rapidapi-host': "seeking-alpha.p.rapidapi.com"
    }
 
response = requests.request("GET", url, headers=headers, params=querystring)
print(response.text)


My details:
import http.client

conn = http.client.HTTPSConnection("seeking-alpha.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "60750c6adcmshec76effe66ba54cp110f68jsna2fa440ab8f4",
    'x-rapidapi-host': "seeking-alpha.p.rapidapi.com"
}

conn.request("GET", "/analysis/v2/list?id=aapl&size=20&number=1", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))

Example Responses
{
  "data": [
    {
      "id": "4486743",
      "type": "article",
      "attributes": {
        "publishOn": "2022-02-14T05:59:46-05:00",
        "isLockedPro": false,
        "commentCount": 154,
        "gettyImageUrl": "https://static.seekingalpha.com/cdn/s3/uploads/getty_images/1321772866/image_1321772866.jpg",
        "themes": {},
        "title": "Apple: Not Facing Reality"
      },
      "relationships": {
        "author": {
          "data": {
            "id": "22148",
            "type": "author"
          }
        },
        "sentiments": {
          "data": [
            {
              "id": "361162",
              "type": "sentiment"
            }
          ]
        },
        "primaryTickers": {
          "data": [
            {
              "id": "146",
              "type": "tag"
            }
          ]
        },
        "secondaryTickers": {
          "data": []
        },
        "otherTags": {
          "data": []
        }
      },
      "links": {
        "self": "/article/4486743-apple-not-facing-reality"
      }
    },
  ],
  "included": [
    {
      "id": "22148",
      "type": "author",
      "attributes": {
        "company": null,
        "slug": "stone-fox-capital",
        "userId": 234751,
        "tagId": 12011,
        "image": {
          "small": "https://static3.seekingalpha.com/images/users_profile/000/234/751/small_pic.png",
          "medium": "https://static3.seekingalpha.com/images/users_profile/000/234/751/medium_pic.png",
          "big": "https://static3.seekingalpha.com/images/users_profile/000/234/751/big_pic.png",
          "extra_large": "https://static3.seekingalpha.com/images/users_profile/000/234/751/extra_large_pic.png"
        },
        "nick": "Stone Fox Capital",
        "bio": "Stone Fox Capital Advisors, LLC is a registered investment advisor founded in 2010. Mark Holder graduated from the University of Tulsa with a double major in accounting & finance. Mark has his Series 65 and is also a CPA.<br><p><br></p><p>Stone Fox Capital launched the <a href=\"https://seekingalpha.com/checkout?service_id=mp_1361\">Out Fox The Street</a> MarketPlace service in August 2020. </p><br>Invest with Stone Fox Capital's model Net Payout Yields portfolio on Interactive Advisors as he makes real time trades. The site allows followers to duplicate the model portfolio in their own brokerage accounts. You can find the portfolio and more details here:<br><br><a href=\"https://interactiveadvisors.com/stone-fox-capital?portfolio=net-payout-yield\" target=\"_blank\">Net Payout Yields model</a><br><p><br></p>Follow Mark on twitter: @stonefoxcapital",
        "memberSince": 2008,
        "contributorSince": 2008,
        "followersCount": 36734
      },
      "relationships": {
        "user": {
          "data": {
            "id": "234751",
            "type": "user"
          }
        }
      },
      "links": {
        "self": "/author/stone-fox-capital",
        "profileUrl": "/author/stone-fox-capital",
        "site": null,
        "linkedinUrl": null,
        "twitterUrl": null
      }
    },
  ],
  "meta": {
    "page": {
      "title": "Apple Inc. (AAPL) Latest Stock Analysis",
      "description": "Find the latest Apple Inc. AAPL stock analysis from Seeking Alpha’s top analysts: exclusive research and insights from bulls and bears",
      "listTitle": "Analysis",
      "listDescription": null,
      "proStatus": 0,
      "size": 20,
      "totalPages": 2,
      "total": 30,
      "minmaxPublishOn": {
        "min": 1643286600,
        "max": 1644836386
      }
    },
    "ads": {
      "zone": "quotes/stocks/analysis/dashboard"
    },
    "mone": {
      "params": {
        "pu": ""
      }
    }
  }
}