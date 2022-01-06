# tinnyHook
### API for Attiny85 payloads
<p align="left">
<img src="imgs/tinnyHook.png" width="240" height="180">
</p>

### _________________________________________________________________________
## Architecture
````
Web API in Golang to capture drops from Attiny85 payloads and display them on a page, also logging and obfuscating communications,
designed for mobile exploitation allowing a payload to drop data to the server and locking the server out so only password
authenticated users can read data or restart the server.
````
````
### Server
* POST / - send file of any format and up to size defined in source code (default=32<<20) 
* GET / - display grabz from latest drop, must be authenticated via ?passwd=$CH_PASSWD
* GET /start - start server and receive notification of time, must be authenticated 
* GET /stop - stop server and receive notification of time, must be authenticated 
````
````
### Dropper
* wifi_grabber - Windows powershell wifi crendentials grabber, logging data to server defined on payload source code
* templates - under development
````

### _________________________________________________________________________
## Disclaimer
* Attiny85 Payloads [from https://github.com/MTK911/Attiny85]
> See license in LICENSE [GPL3.0]
