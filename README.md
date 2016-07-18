# Simple Ad Server
REST api 

flask-restful
MongoDB

###Create Ad Campaign via HTTP POST###

 
A user should be able to create an ad campaign by sending a POST request to the ad server at http://<host>/ad.  The body of the POST request must be a JSON object containing the following data:

{
 "partner_id": "unique_string_representing_partner',
 "duration": "int_representing_campaign_duration_in_seconds_from_now"
 "ad_content": "string_of_content_to_display_as_ad"
}

The server should enforce the following invariant upon receiving a request to create a new campaign.

* Only one active campaign can exist for a given partner.

If an error is encountered, the ad server must return an appropriate response and indicate the problem to the user.  The response format is left up to the discretion of the implementer.

Storing campaign data in memory or a cookie is totally fine.
 
###Fetch Ad Campaign for a Partner###


A partner should be able to get their ad data by sending a GET request to the ad server at http://<host>/ad/<partner_id>.  Response can be delivered as a JSON object representing the active ad

If the current time is greater than a campaign's creation time + duration, then the server's response should be an error indicating that no active ad campaigns exist for the specified partner.



### Install requirements: ###
Install the requirements in a virtual environment.
```
pip install -r requirements.txt

```
### Testing api ##
```


