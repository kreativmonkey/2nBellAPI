import ssl
import requests
import os
import json


DEFAULT_USERNAME = 'Admin'
DEFAULT_PORT = '443'
STATE_TOPICS = {
  'ProductName': 'State.Product.ProductName', 
  'DeviceName': 'WebServer.DeviceName',
  'UpTime': 'State.Time.UpTime', 
  'SerialNumber': 'State.Product.SerialNumber', 
  'SoftwareVersion': 'State.Product.SoftwareVersion', 
  'Phone0Registration': 'State.Phone.Registration[0].State' ,  # Sensor?
  'Phone1Registration': 'State.Phone.Registration[1].State' ,  # Sensor?
  'Phone0FailureReason' : 'State.Phone.Registration[0].FailureReason',
  'Phone1FailureReason' : 'State.Phone.Registration[1].FailureReason',
  'AdaptiveVolumeNoiseLevel': 'State.AdaptiveVolume.NoiseLevel', # Sensor
  'AdaptiveVolumeCurrentGain': 'State.AdaptiveVolume.CurrentGain' #Sensor
}

SET_TOPICS = {
  'BacklightBrightness': 'Backlight.BkDayBrightness'
}

class Wrapper(object):
    def __init__(self, obj):
        self._wrapped_obj = obj
        
    def __getattr__(self, attr):
        if attr in self.__dict__:
            return getattr(self, attr)
        return getattr(self._wrapped_obj, attr)



class BellAPIWrapper():
	
	def _send(self, payload):
        # dict in JSON umwandeln
        # dann der ganze http code
		return
		
	def _set(self, pathes):
		# Set path only for one value, it is much easier!
		payload = [self._getQuerry('db.set', path) for path in pathes]
		self._send(payload)

	def _get(self, pathes):
		payload = [self._getQuerry('db.get', path) for path in pathes]
		self._send(payload)

	def _getQuerry(self, command, path)
		payload = {}
		payload["command"] = command
		payload["path"] = path
		return payload
	
	
	def set_brightness(self, value):
		payload = {}
		payload["path"] = "Backlight.BkDayBrightness"
		payload["value"] = str(value)
		self._set(payload)
		


class TwoN():
	
	def __init__(
        self,
        password,
        host,
        username = DEFAULT_USERNAME,
        port=DEFAULT_PORT,
    ):
		self.s = None
		
		self.username = username
		self.password = password
		self.port = port
		self.host = host
		# Setting the session URL to the default
		self.sessionUrl = 'https://' + host + '/ajax?sid='
		
		self.login(username, password)
		
		self.State = self.TwoNState()
		
	def getState(self):
		return self.State
		
	def login(self, username, password):
		self.s = requests.Session()
		# Workaround for self signed certificates, need a better solution!
		self.s.verify = False
		
		# Payload for login
		login_payload = '[{"command":"system.login","user":"'+username+'","password":"'+password+'"}]'
		resp = self.sendRequest(login_payload)
		
		# Adding the session ID to the session URL
		self.sessionUrl += json.loads(resp.text)[0]["sid"]
		return resp
        
	def logout(self):
		resp = json.loads(self.s.post(self.sessionUrl, data='[{"command":"system.logout"}]').text)[0]['status']
		# If logout is ok close the session, i need a better solution for error handling in this case.
		if resp == 'ok':
			self.s.close()
		return resp
		
	def TwoNState(self):
		payload = self.createPayload('db.get', STATE_TOPICS)
		response = self.sendRequest(payload)
				
		return self.generateJsonFromRequest(STATE_TOPICS, response)
		
	def generateJsonFromRequest(self, request, response):
		states = {}
		for i, req in enumerate(request, start=0):
			states[req] = json.loads(response.text)[i]['value']
		
		return states
			
	def sendRequest(self, payload):
		return self.s.post(self.sessionUrl, data=payload)
	
	def createPayload(self, command, path):
		payload = '['
		for p in path.values():
			payload += '{"command":"'+ command +'", "path":"' + p + '"},'
		
		# Remove the last ',' from the Payload and add ]
		payload = payload.rstrip(',') + ']'
		
		return payload


host = '192.168.5.5'
port = '443'
username = 'Admin'
password = 'SavePassword'

two = TwoN(password = password, host = host, port = port, username = username)
states = json.dumps(two.getState())


print(json.loads(states)['DeviceName'])

print(states)
print(two.logout())  
