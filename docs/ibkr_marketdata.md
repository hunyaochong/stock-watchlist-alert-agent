Live Market Data Snapshot

get
/iserver/marketdata/snapshot


Get Market Data for the given conid(s). A pre-flight request must be made prior to ever receiving data. For some fields, it may take more than a few moments to receive information. See response fields for a list of available fields that can be request via fields argument. The endpoint /iserver/accounts must be called prior to /iserver/marketdata/snapshot. For derivative contracts the endpoint /iserver/secdef/search must be called first.

query Parameters
conids
required
string <int32>
Example: conids=265598
Contract identifier for the contract of interest. May provide a comma-separated series of contract identifiers.

fields	
any (mdFields)
Enum: "31" "55" "58" "70" "71" "73" "74" "75" "76" "77" "78" "79" "80" "82" "83" "84" "85" "86" "87" "88" "6004" "6008" "6070" "6072" "6073" "6119" "6457" "6508" "6509" "7051" "7057" "7058" "7059" "7068" "7084" "7085" "7086" "7087" "7088" "7089" "7094" "7184" "7219" "7220" "7221" "7280" "7281" "7282" "7283" "7284" "7285" "7286" "7287" "7288" "7289" "7290" "7291" "7292" "7293" "7294" "7295" "7296" "7308" "7309" "7310" "7311" "7607" "7633" "7635" "7636" "7637" "7638" "7639" "7644" "7655" "7671" "7672" "7674" "7675" "7676" "7677" "7678" "7679" "7724" "7681" "7682" "7683" "7684" "7685" "7686" "7687" "7688" "7689" "7690" "7694" "7695" "7696" "7697" "7698" "7699" "7700" "7702" "7703" "7704" "7705" "7706" "7707" "7708" "7714" "7715" "7718" "7720" "7741" "7762" "7768" "7920" "7921"
Many FYI endpoints reference a “typecode” value. The table below lists the available codes and what they correspond to.

31 - Last Price. The last price at which the contract traded. May contain one of the following prefixes: C - Previous day's closing price. H - Trading has halted.
55 - Symbol.
58 - Text.
70 - High. Current day high price
71 - Low. Current day low price
73 - Market Value. The current market value of your position in the security. Market Value is calculated with real time market data (even when not subscribed to market data).
74 - Avg Price. The average price of the position.
75 - Unrealized PnL. Unrealized profit or loss. Unrealized PnL is calculated with real time market data (even when not subscribed to market data).
76 - Formatted position.
77 - Formatted Unrealized PnL.
78 - Daily PnL. Your profit or loss of the day since prior close. Daily PnL is calculated with real time market data (even when not subscribed to market data).
79 - Realized PnL. Realized profit or loss. Realized PnL is calculated with real time market data (even when not subscribed to market data).
80 - Unrealized PnL %. Unrealized profit or loss expressed in percentage.
82 - Change. The difference between the last price and the close on the previous trading day
83 - Change %. The difference between the last price and the close on the previous trading day in percentage.
84 - Bid Price. The highest-priced bid on the contract.
85 - Ask Size. The number of contracts or shares offered at the ask price. For US stocks
86 - Ask Price. The lowest-priced offer on the contract.
87 - Volume. Volume for the day
88 - Bid Size. The number of contracts or shares bid for at the bid price. For US stocks
6004 - Exchange.
6008 - Conid. Contract identifier from IBKR's database.
6070 - SecType. The asset class of the instrument.
6072 - Months.
6073 - Regular Expiry.
6119 - Marker for market data delivery method (similar to request id).
6457 - Underlying Conid. Use /trsrv/secdef to get more information about the security.
6508 - Service Params..
6509 - Market Data Availability. The field may contain three chars. First char defines: R = RealTime, D = Delayed, Z = Frozen, Y = Frozen Delayed, N = Not Subscribed, i - incomplete, v - VDR Exempt (Vendor Display Rule 603c). Second char defines: P = Snapshot, p = Consolidated. Third char defines: B = Book. RealTime Data is relayed back in real time without delay, market data subscription(s) are required. Delayed - Data is relayed back 15-20 min delayed. Frozen - Last recorded data at market close. relayed back in real time. Frozen Delayed - Last recorded data at market close, relayed back delayed. Not Subscribed - User does not have the required market data subscription(s) to relay back either real time or delayed data. Snapshot - Snapshot request is available for contract. Consolidated - Market data is aggregated across multiple exchanges or venues. Book - Top of the book data is available for contract.
7051 - Company name.
7057 - Ask Exch. Displays the exchange(s) offering the SMART price. A=AMEX, C=CBOE, I=ISE, X=PHLX, N=PSE, B=BOX, Q=NASDAQOM, Z=BATS, W=CBOE2, T=NASDAQBX, M=MIAX, H=GEMINI, E=EDGX, J=MERCURY
7058 - Last Exch. Displays the exchange(s) offering the SMART price. A=AMEX, C=CBOE, I=ISE, X=PHLX, N=PSE, B=BOX, Q=NASDAQOM, Z=BATS, W=CBOE2, T=NASDAQBX, M=MIAX, H=GEMINI, E=EDGX, J=MERCURY
7059 - Last Size. The number of unites traded at the last price
7068 - Bid Exch. Displays the exchange(s) offering the SMART price. A=AMEX, C=CBOE, I=ISE, X=PHLX, N=PSE, B=BOX, Q=NASDAQOM, Z=BATS, W=CBOE2, T=NASDAQBX, M=MIAX, H=GEMINI, E=EDGX, J=MERCURY
7084 - Implied Vol./Hist. Vol %. The ratio of the implied volatility over the historical volatility, expressed as a percentage.
7085 - Put/Call Interest. Put option open interest/call option open interest for the trading day.
7086 - Put/Call Volume. Put option volume/call option volume for the trading day.
7087 - Hist. Vol. %. 30-day real-time historical volatility.
7088 - Hist. Vol. Close %. Shows the historical volatility based on previous close price.
7089 - Opt. Volume. Option Volume
7094 - Conid + Exchange.
7184 - canBeTraded. If contract is a trade-able instrument. Returns 1(true) or 0(false).
7219 - Contract Description.
7220 - Contract Description.
7221 - Listing Exchange.
7280 - Industry. Displays the type of industry under which the underlying company can be categorized.
7281 - Category. Displays a more detailed level of description within the industry under which the underlying company can be categorized.
7282 - Average Volume. The average daily trading volume over 90 days.
7283 - Option Implied Vol. %. A prediction of how volatile an underlying will be in the future.At the market volatility estimated for a maturity thirty calendar days forward of the current trading day, and based on option prices from two consecutive expiration months. To query the Implied Vol. % of a specific strike refer to field 7633.
7284 - Historical volatility %. Deprecated
7285 - Put/Call Ratio.
7286 - Dividend Amount. Displays the amount of the next dividend.
7287 - Dividend Yield %. This value is the toal of the expected dividend payments over the next twelve months per share divided by the Current Price and is expressed as a percentage. For derivatives
7288 - Ex-date of the dividend.
7289 - Market Cap.
7290 - P/E.
7291 - EPS.
7292 - Cost Basis. Your current position in this security multiplied by the average price and multiplier.
7293 - 52 Week High. The highest price for the past 52 weeks.
7294 - 52 Week Low. The lowest price for the past 52 weeks.
7295 - Open. Today's opening price.
7296 - Close. Today's closing price.
7308 - Delta. The ratio of the change in the price of the option to the corresponding change in the price of the underlying.
7309 - Gamma. The rate of change for the delta with respect to the underlying asset's price.
7310 - Theta. A measure of the rate of decline the value of an option due to the passage of time.
7311 - Vega. The amount that the price of an option changes compared to a 1% change in the volatility.
7607 - Opt. Volume Change %. Today's option volume as a percentage of the average option volume.
7633 - Implied Vol. %. The implied volatility for the specific strike of the option in percentage. To query the Option Implied Vol. % from the underlying refer to field 7283.
7635 - Mark. The mark price is
7636 - Shortable Shares. Number of shares available for shorting.
7637 - Fee Rate. Interest rate charged on borrowed shares.
7638 - Option Open Interest.
7639 - % of Mark Value. Displays the market value of the contract as a percentage of the total market value of the account. Mark Value is calculated with real time market data (even when not subscribed to market data).
7644 - Shortable. Describes the level of difficulty with which the security can be sold short.
7655 - Morningstar Rating. Displays Morningstar Rating provided value. Requires Morningstar subscription.
7671 - Dividends. This value is the total of the expected dividend payments over the next twelve months per share.
7672 - Dividends TTM. This value is the total of the expected dividend payments over the last twelve months per share.
7674 - EMA(200). Exponential moving average (N=200).
7675 - EMA(100). Exponential moving average (N=100).
7676 - EMA(50). Exponential moving average (N=50).
7677 - EMA(20). Exponential moving average (N=20).
7678 - Price/EMA(200). Price to Exponential moving average (N=200) ratio -1
7679 - Price/EMA(100). Price to Exponential moving average (N=100) ratio -1
7724 - Price/EMA(50). Price to Exponential moving average (N=50) ratio -1
7681 - Price/EMA(20). Price to Exponential moving average (N=20) ratio -1
7682 - Change Since Open. The difference between the last price and the open price.
7683 - Upcoming Event. Shows the next major company event. Requires Wall Street Horizon subscription.
7684 - Upcoming Event Date. The date of the next major company event. Requires Wall Street Horizon subscription.
7685 - Upcoming Analyst Meeting. The date and time of the next scheduled analyst meeting. Requires Wall Street Horizon subscription.
7686 - Upcoming Earnings. The date and time of the next scheduled earnings/earnings call event. Requires Wall Street Horizon subscription.
7687 - Upcoming Misc Event. The date and time of the next shareholder meeting
7688 - Recent Analyst Meeting. The date and time of the most recent analyst meeting. Requires Wall Street Horizon subscription.
7689 - Recent Earnings. The date and time of the most recent earnings/earning call event. Requires Wall Street Horizon subscription.
7690 - Recent Misc Event. The date and time of the most recent shareholder meeting
7694 - Probability of Max Return. Customer implied probability of maximum potential gain.
7695 - Break Even. Break even points
7696 - SPX Delta. Beta Weighted Delta is calculated using the formula; Delta x dollar adjusted beta
7697 - Futures Open Interest. Total number of outstanding futures contracts
7698 - Last Yield. Implied yield of the bond if it is purchased at the current last price. Last yield is calculated using the Last price on all possible call dates. It is assumed that prepayment occurs if the bond has call or put provisions and the issuer can offer a lower coupon rate based on current market rates. The yield to worst will be the lowest of the yield to maturity or yield to call (if the bond has prepayment provisions). Yield to worse may be the same as yield to maturity but never higher.
7699 - Bid Yield. Implied yield of the bond if it is purchased at the current bid price. Bid yield is calculated using the Ask on all possible call dates. It is assumed that prepayment occurs if the bond has call or put provisions and the issuer can offer a lower coupon rate based on current market rates. The yield to worst will be the lowest of the yield to maturity or yield to call (if the bond has prepayment provisions). Yield to worse may be the same as yield to maturity but never higher.
7700 - Probability of Max Return. Customer implied probability of maximum potential gain.
7702 - Probability of Max Loss. Customer implied probability of maximum potential loss.
7703 - Profit Probability. Customer implied probability of any gain.
7704 - Organization Type.
7705 - Debt Class.
7706 - Ratings. Ratings issued for bond contract.
7707 - Bond State Code.
7708 - Bond Type.
7714 - Last Trading Date.
7715 - Issue Date.
7718 - Beta. Beta is against standard index.
7720 - Ask Yield. Implied yield of the bond if it is purchased at the current offer. Ask yield is calculated using the Bid on all possible call dates. It is assumed that prepayment occurs if the bond has call or put provisions and the issuer can offer a lower coupon rate based on current market rates. The yield to worst will be the lowest of the yield to maturity or yield to call (if the bond has prepayment provisions). Yield to worse may be the same as yield to maturity but never higher.
7741 - Prior Close. Yesterday's closing price
7762 - Volume Long. High precision volume for the day. For formatted volume refer to field 87.
7768 - hasTradingPermissions. if user has trading permissions for specified contract. Returns 1(true) or 0(false).
7920 - Daily PnL Raw. Your profit or loss of the day since prior close. Daily PnL is calculated with real-time market data (even when not subscribed to market data).
7921 - Cost Basis Raw. Your current position in this security multiplied by the average price and and multiplier.
Responses
200 Successfully enabled or disabled your email notifications.
400 bad request
401 access denied
500 internal server error, returned when incoming request cannot be processed. It can sometimes include subset of bad requests. For example, wrong accountId passed and it can only be detected later in handling request. Error contains reason of the problem.
503 service is unavailable. For example if request takes more than 10s due to some internal service unavailability, request aborted and this status returned