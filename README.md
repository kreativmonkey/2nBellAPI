# Get API Anfrage

``"command":"db.get", "path":``

| Path | Response | Description |
| ---- | -------- | ----------- |
| WebServer.DeviceName | [{"status":"ok","value":"2N IP Uni","is_default":false}] | get the Device Name |
| WebServer.Language | [{"status":"ok","value":"17","is_default":true}] | |
| WebServer.MinTlsVersion | [{"status":"ok","value":"3","is_default":false}] | |
| WebServer.Password | [{"status":"ok","value":"********","is_default":true}] | |
| WebServer.Port | [{"status":"ok","value":"80","is_default":true}] | |
| WebServer.RemoteAccessEnabled | [{"status":"ok","value":"0","is_default":true}] | |
| WebServer.SecurePort | [{"status":"ok","value":"443","is_default":true}] | | 
| WebServer.UserCertPK | [{"status":"ok","value":"0","is_default":true}] | |
| Phone.Sip[0].User.Id | [{"status":"ok","value":"2nuniAnlage","is_default":false}] | get the ID of the SIP User from SIP Setup 1 (showen as number at the homescreen) |
| Phone.Sip[1].User.Id | [{"status":"ok","value":"111","is_default":true}] | get the ID of the SIP User from SIP Setup 2 |
| Camera.MotionDetection.Enabled | [{"status":"invalid path"}] | If path is invalide there is no Camera on this device! |

# State Requests

| Path | Response | Description |
| ---- | -------- | ----------- |
| State.Time.UpTime | [{"status":"ok","value":"116292","is_default":false}] | Uptime in Seconds |
| State.Directory.AComControl | [{"status":"ok","value":"0","is_default":true}] | |
| State.Directory.Counters.Users | [{"status":"ok","value":"2","is_default":false}] | Count the Users in the Dictionary |
| State.NetInfo.DhcpUsed | [{"status":"ok","value":"1","is_default":false}] | Returns 0 ore 1 for DHCP in use |
| State.Phone.Registration[0].State | [{"status":"ok","value":"2","is_default":false}] | If the Phone is registered (0=Not Registered, 1=Registering, 2=Registered)|
| State.Phone.Registration[1].State | [{"status":"ok","value":"0","is_default":true}] | |
| State.Phone.Registration[i].FailureReason | [{"status":"ok","value":"Registration failed","is_default":false}] | The reason of failure while registering |
| State.Phone.Registration[i].ExtNameDnsFailed | [{"status":"ok","value":"0","is_default":true}] | |
| State.Product.CompanyUri | [{"status":"ok","value":"http://www.2n.cz","is_default":false}] | The URI of the company |
| State.Product.Customer | [{"status":"ok","value":"0","is_default":true}] | |
| State.Product.ManualUri | [{"status":"ok","value":"https://wiki.2n.cz/is","is_default":false}] | The URI for the user manual |
| State.Product.ProductName | [{"status":"ok","value":"2N IP Uni","is_default":false}] | The name of the Product (model) |
| State.Product.SerialNumber | [{"status":"ok","value":"54-2336-1330","is_default":false}] | Serial Number of the Product |
| State.Product.SoftwareVersion | {"status":"ok","value":"2.29.1.38.8","is_default":false} | Current firmware version|
| State.WebServer.LanguageShort | [{"status":"ok","value":"","is_default":true}] | ? |
| State.AdaptiveVolume.CurrentGain | [{"status":"ok","value":"0","is_default":true}] | |
| State.AdaptiveVolume.NoiseLevel | [{"status":"ok","value":"-45","is_default":false}] | |
| State.Prdouct.Camera | [{"status":"ok","value":"0","is_default":true}] | this state is also ok if the camera isn't there!! | 

# Set API Requests

``"command":"db.set","path":``

| Request | value | Response |
| ---- | -------- | ----------- |
| Backlight.BkDayBrightness | "value":"50" | |
| Audio.NoiseDetection.Enabled | | [{"status":"invalid path"}] |
| Audio.AdaptiveVolume.Enabled | | [{"status":"ok","value":"1","is_default":false}] |
| Audio.AdaptiveVolume.MaxGain | | [{"status":"ok","value":"12","is_default":true}] |
| Audio.AdaptiveVolume.NoiseThreshold | [{"status":"ok","value":"-24","is_default":true}] | 
| Audio.CallProgressToneVolume | | [{"status":"ok","value":"2","is_default":false}] |
| Audio.KeyBeepVolume | | [{"status":"ok","value":"0","is_default":true}] |
| Audio.MasterVolume | | [{"status":"ok","value":"-6","is_default":false}] |
| Audio.RingingVolume | | [{"status":"ok","value":"4","is_default":false}] |
| Audio.SwitchSignalVolume | | [{"status":"ok","value":"0","is_default":true}] |
| Audio.WarnBeepVolume | | [{"status":"ok","value":"0","is_default":true}] |


# Button Press

Example for the door switch button:

```
https://192.168.178.5/api/log/pull?id=589609156&timeout=60&sid=2e8b3ea8-00d6-40aa-a690-274657ea85ee&_=1595154260370
```

| Button | ID |
| ------ | -------- |
| Switch | 589609156 | 
