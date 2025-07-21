# interface-advantech-WISE-REST
code to interface the REST endpoint of advantech's WISE IO module(s)  
preface: i'm used to industrial electronics doing things weirdly and having subpar documentation. so the situation i encountered is not at all surprising. hopefully this will save someone some headache.  

**THIS IS WORK IN PROGRESS I'M STILL TESTING THIS**

## motivation  
the documentation i found at  
https://advdownload.advantech.com/productfile/Downloadfile2/1-14JNLJL/UM-WISE-4000-Ed.4-EN.pdf  
for advatech's WISE-4000 series IO modules does not do a great job at describing their REST interface. the biggest downside is that there is absolutely no mention of the fact that one needs to log into the device and then use the provided cookie for setting digital outputs and querying IO state.  
i tested this with a WISE-4050/LAN module with four digital inputs and four digital outputs. i assume that other modules will work similarly.  

## logging in  
when requesting the login page, the returned index.html contains an eight digit hexadecimal seed (seeddata in code). from this, a string can be constructed in the form of  
seed:username:password  
this string is then hashed with md5 into authdata. then, this information is packaged into a payload in the form  
seeddata=seed&authdata=authdata  
send this with a POST request to the login endpoint. the only header that matters seems to be Content-Length, which is the length of the above string. if you receive a 200 response, it will containg a cookie with an adamsessionid variable. i _believe_ that this variable holds the first 11 digits of the hash for the seed:username:password string, so probably it can also be constructed.  
the way this process works lets me believe that the username and password are stored in plain text on the module. there are more than enough standardized ways to do authentication via REST. it's beyond me why advantech chose their own convoluted, undocumented and probably unsafe way to do this.  

## query state of digital IO  
send a GET request to  
/do_value/slot_0 for outputs or  
/di_value/slot_0 for inputs  
port :80 is not required here.  you get back a string that can be converted into json.  

## set digital output  
this was the biggest headache.  
sending PUT to /do_value/slot_0/ch_X (X = 0..3) did not work at all. the server required a Content-Length, however setting it to 0 crashed the server. other numbers didn't work either.  
by investigating network traffic, it became obvious that the web interface actually sends a json to /do_value/slot_0. BUT: it sends it as a string à la  
"{\"DOVal\":[{\"Ch\":0,\"Val\":1}]}"  
Content-Length is the length of the string.  
altogether, this concept feels strange.  

## other info / final thoughts  
the default cycle time on the IO module is 1 s. beware of that and adjust the timing of your application accordingly. the cycle time can be changed in the configuration, but i did not dare trying it. god knows what kind of side effects this will have.  
the REST API is not available on all firmware versions. i updated my module to whatever seems to have been the latest version in july 2025.  

## TODO  
- check if modularized code actually works  
- add test and/or example scripts  
