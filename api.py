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

class BellAPIWrapper():
  
  def __init__(
        self,
        password,
        host,
        username = DEFAULT_USERNAME,
        port=DEFAULT_PORT,
    ):
    self._session = None
    
    self._username = username
		self._password = password
		self._port = port
		self._host = host
    self._sessionID = ''
		# Setting the session URL to the default
		self._sessionUrl = 'https://' + host + '/ajax?sid='
    
		self._login()
    
    self._payload = []
	
  def _login(self):
    # TODO: Caching Session: https://stackoverflow.com/questions/12737740/python-requests-and-persistent-sessions
 
		self._session = requests.Session()
		# Workaround for self signed certificates, need a better solution!
    # TODO: support selfe signed certificate
		self._session.verify = False
				
    resp = self._send('[{"command":"system.login","user":"'+ self._username +'","password":"'+ self._password +'"}]', False)
    
		# Save the session ID
		self._sessionID = json.loads(resp.text)[0]["sid"]
    
		return resp
  
  def _logout(self):
		resp = self._send('[{"command":"system.logout"}]', False)
		
    # If logout is ok close the session, i need a better solution for error handling in this case.
		if json.loads(resp.text)[0]['status'] == 'ok':
      self._sessionID = ''
			self._session.close()
		
    return resp
  
  def _is_json(myjson):
    try:
      json_object = json.loads(myjson)
    except ValueError as e:
      return False
    return True
    
	def _send(self, p, checkSession = True):
    # TODO: Check if the session is already opened
    if checkSession:
      # First Workaround
      if self._sessionID == "":
        self._login()
         
    # check if payload is already a valid json
    if self._is_json(p):
      pyload = p
      
    # convert a list of dict into JSON
    if isinstance(p, list):
      payload = json.dumps(p)
      
    # return des the response
		return self._session.post(self._sessionUrl + self._sessionID, data=payload)

  def _payloadSet(self, path, value)
    # Check if path already in the payload
    #if any(p['path'] == path for p in self._payload):
    #  raise ValueError('Path already in the Payload')
    
    # Update if path already in the payload
    for p in self._payload:
      if p['path'] == path:
        p['value'] = value
        
        return 
    
    # TODO: Validate value for path
      
    payload["command"] = "db.set"
    payload["path"] = SET_TOPICS[path]
    payload["value"] = value
    
    return payload
    
  def _payloadGet(self, path)
    # Check if path already in the payload
    if any(p['path'] == path for p in self._payload):
      raise ValueError('Path already in the Payload')
    
    payload["command"] = "db.get"
    payload["path"] = STATE_TOPICS[path]
    
    return payload
    
  def addPayload(self, path, command="db.get", value = None):
    # Check if the command is supported
    if not command == "db.set" or not command == "db.get":
      raise ValueError("Command not be found")
    
    
    # Check if the path and command compares, not every path can be set ore get
    if command == "db.get":
      if path not in STATE_TOPICS:
        raise ValueError(path + ' is not supported ore has no set function')
        
      payload = self._payloadGet(path)
        
		elif command == "db.set":
      if path not in SET_TOPICS:
        raise ValueError(path + ' is not supported ore has no get function')
      # Check if the Value is set on command "db.set"
      # TODO: validate the value
      if value is None:
        raise ValueError('Value must be set')   
        
      payload = self._payloadSet(path, value)
  
    self._payload.append(payload)
      
  def sendPayloads(self):
    if not self._send(payload):
      return 1
  
    # after success delet saved payload
    del self._payload[:]
          
    return 0
    
  def setBrightness(self, value):
    # Check the correct value
		if not value >= 0 and not value <= 100:
      return
      
    payload = []
    payload.append(self._payloadSet("BacklightBrightness", value)) 
    if not self._send(payload):
      return 1
    
    return 0
      
  def getState(self):
    payload = []
    for state in STATE_TOPICS:
      payload.append(self._payloadGet(state))

    self._send(payload)
    				
		return 
    
    
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
