# searchlist_lambda_distance

[![Build Status](https://travis-ci.org/fort-kickass/searchlist_lambda_distance.svg?branch=master)](https://travis-ci.org/fort-kickass/searchlist_lambda_distance)

This code runs on AWS Lambda and takes the following json via api gateway from the [searchlist_s3_frontend](https://github.com/fort-kickass/searchlist_s3_frontend) code and generates a list of cities within x distance of y CL city. Each result is then pushed via [Pusher](pusher.com) back to the frontend page.  It will also(when we get around to adding it) kick off a lambda job to generate a search and results for each CL site in the list.


```
{"city":"denver",
"distance":"100",
"query":"Oculus Rift",
"pusher_channel":"de81df41-5436-7be7-2666-d12ad1b8fdb2"}
```
