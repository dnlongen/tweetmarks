Tweetmarks
=============

(Rough) proof of concept to extract URLs liked or favorited in Twitter, and add them to browser bookmarks.

* Written by David Longenecker
* Twitter: @dnlongen
* Email: david (at) securityforrealpeople.com

Twitter converts every url into a "t.co" shortlink. The same url tweeted again later will get a different shortlink. Tweetmarks handles this by examining the url entity, and replacing the t.co shortlink with the expanded url provided by the Twitter API.

The Twitter API is rate-limited, as described at https://dev.twitter.com/rest/public/rate-limiting. If you get a rate-limit error running tweetthief, try again with a smaller -n, or wait a few minutes.

PoC code so far extracts the liked URLs, but doesn't add them to bookmarks yet. Chrome bookmarks are stored in JSON format; theoretically it should be possible to parse the JSON file at $APPDATA\..\Local\Google\Chrome\User Data\Default\Bookmarks and add bookmark entries underneath roots-->bookmark_bar-->children-->(create a folder). Alternately, CLI bookmarks by TJ Holowaychuk (https://github.com/tj/bm) looks like a handy way to do browser-agnostic bookmarks.

Requirements:
=============

* Requires tweepy, the Twitter API module for Python, available from https://github.com/tweepy/tweepy
* Requires an application token for the Twitter API. Refer to documentation at https://dev.twitter.com/oauth/overview/application-owner-access-tokens, and set up your own app-specific tokens at https://apps.twitter.com
 
Change Log:
=============

* v0.1 Original release.

Errata:
=============

* TBD
