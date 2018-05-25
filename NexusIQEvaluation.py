import sublime, sublime_plugin
import json
from pprint import pprint
from urllib import request, parse

import base64
import os

import subprocess
import uuid
import time


def generateShrinkWrap(strPath, strPackageJson):
	#I have to use the older syntax as Sublime uses Python 3.3
    print ("generateShrinkWrap")
    #thisFile = __file__
    #print ("thisFile", thisFile)
    #strPath = "/Users/camerontownshend/Documents/Cameron/dev/learnNPM/simpletest/"
    shrinkFileName = "npm-shrinkwrap.json"
    os.chdir(strPath)
    #strCommand = "npm shrinkwrap"

    proc=subprocess.call(('npm', 'shrinkwrap'))
    #strOutput = proc.stdout
    #strErr = proc.stderr
    intReturncode = proc
    #print (strErr)
    strFullFileName = os.path.join(strPath, shrinkFileName)
    return strFullFileName


def loadShrinkWrap(strFileName):
	print ("loadhrinkWrap")
	file = open(strFileName, "r")
	fileContents = file.read() 
	return fileContents

def generateShrinkWrapMock(strPath, strPackageJson):
	print ("generateShrinkWrapMock")
	strPath = "/Users/camerontownshend/Documents/Cameron/dev/learnNPM/simpletest/"
	shrinkFileName = "npm-shrinkwrap.json"
	strFullFileName = os.path.join(strPath, shrinkFileName)
	return strFullFileName

def testnexusFormat():
	componentlist={
		"components" : 
		[
			{"hash": None, 
			"componentIdentifier": 
				{ "format":"maven", "coordinates" : 
					{
						"artifactId":"tomcat-util",
						"extension":"jar", 
						"groupId":"tomcat", 
						"version" : "5.5.23"
					}
				}
			},			
			{"hash": None, 
			"componentIdentifier": 
				{ "format":"npm", "coordinates" : 
					{
						"packageId":"lodash", 
						"version" : "4.17.4"
					}
				}
			}
		]
	}
	return componentlist

def parseShrinkWrapMock(fileContents):
	print ("parseShrinkWrapMock")
	#sourece file looks like this
	#it should return a dictionary of dependencies
	shrinkWrapFileBody = {
	  "name": "simpletest",
	  "version": "1.0.0",
	  "lockfileVersion": 1,
	  "requires": True,
	  "dependencies": {
	    "lodash": {
	      "version": "4.17.4",
	      "resolved": "http://localhost:8083/repository/npm-all/lodash/-/lodash-4.17.4.tgz",
	      "integrity": "sha1-eCA6TRwyiuHYbcpkYONptX9AVa4="
	    }
	  }
	}
	return shrinkWrapFileBody["dependencies"]


def nexusFormat(dependencies):
	print ("nexusFormat")
	#return a dictionary in Nexus Format
	#return dictionary of components
	componentlist=[]
	for key, dependency in dependencies.items():
		#key = dependency
		#print (key)
		#print (dependency["version"])
		packageId=key
		version=dependency["version"]
		component = {
			"hash": None, 
			"componentIdentifier": 
				{
				"format":"npm",
				"coordinates" : 
					{
						"packageId": key, 
						"version" : version
					}
				}
			}
		#hash=("%s_%s") % (packageId, version) 
		componentlist.append(component) 
	componentDict = {}
	componentDict = {"components":componentlist}
	#print (componentDict)
	return componentDict


def parseShrinkWrap(fileContents):
	print ("parseShrinkWrap")
	#sourece file looks like this
	#it should return a dictionary of dependencies
	d = json.loads(fileContents)
	#print(d["dependencies"])
	return (d["dependencies"])


def serverURL():
	print ("ServerURL")
	scheme=view.settings().get("scheme")
	uri=view.settings().get("uri")
	port=view.settings().get("port")
	username=view.settings().get("username")
	password=view.settings().get("password")
	rest="api/v2/components/details"
	theurl="%s://%s:%s/%s" % (scheme, uri, port, rest)
	print (theurl)
	return (theurl)

def evaluateComponent(componentlist):
	print ("EvaluateComponent")
	#receive a dictionary of components
	#return the Json object
	uri="localhost"    
	port=str(8070)
	username="admin"
	password="admin123"
	theurl="http://%s:%s/api/v2/components/details" % (uri,port)



	#json_data = json.dumps(d).encode('utf8')
	json_data = json.dumps(componentlist).encode('utf8')

    #data = parse.urlencode(<your data dict>).encode()
    #req =  request.Request(<your url>, data=data) # this will make the method "POST"
    #resp = request.urlopen(req)
    # create a password manager
	password_mgr = request.HTTPPasswordMgrWithDefaultRealm()
	theTopLevelurl="http://%s:%s" % (uri, port)
	password_mgr.add_password(None, theTopLevelurl, username, password)
	handler = request.HTTPBasicAuthHandler(password_mgr)
    # create "opener" (OpenerDirector instance)
	opener = request.build_opener(handler)
    # use the opener to fetch a URL
	#opener.open(theurl)
	enableProxyDebug=False
	if (enableProxyDebug):
		proxy=request.ProxyHandler({"http" : "http://localhost:8080"})
		opener = request.build_opener(proxy)

    # Install the opener.
    # Now all calls to urllib.request.urlopen use our opener.
	request.install_opener(opener)

	usrPass = "%s:%s" % (username, password)
	b64Val = base64.b64encode(bytes(usrPass, 'utf-8'))
	auth='Basic %s' % b64Val.decode("utf-8")
	#print (auth)

	#print (theurl)
	#return
	req= request.Request(theurl, data=json_data, method='POST', headers={'Content-Type': 'application/json', 'Authorization': auth})
	resp = request.urlopen(req)	
	#text = str(resp.status)
	string = resp.read().decode('utf-8')
	json_obj = json.loads(string)
	#text=string
	return (json_obj)

def handleError(self, edit, txtResponse):
	print("handleError:", txtResponse)
	
	self.panel = self.view.window().create_output_panel('sf_st3_output')
	self.view.window().run_command('show_panel', { 'panel': 'output.sf_st3_output' })
	#self.panel.run_command('sfprint');
	#self.panel.insert(edit, self.view.size(), txtResponse)
	#panels["output.sf_st3_output"].insert(edit, self.view.size(), txtResponse)
	#createdPopupPanel.insert(edit, 0, txtResponse)
	#createdView.insert(edit, 0, txtResponse)
	#window.create_output_panel("errorWindow")	
	#, "Please select a package.json before continuing"

def hasSecurityIssues(response):
	print ("hasSecurityIssues")
	numFound = 0
	#return (6)
	#len(json_obj["componentDetails"][0]["securityData"]["securityIssues"])
	for component in response["componentDetails"]:
		if len(component["securityData"]["securityIssues"])>0:
			numFound+=1
	return (numFound)

def saveOutput(self, edit, json_obj, strPath):
	#for component in e["components"]:
	#	txtResponse += ", " + component["componentIdentifier"]["format"]
	txtResponse = json.dumps(json_obj, indent=4, sort_keys=True)
	createdView = self.view.window().new_file() # New view in group		
	#currentPosition = self.view.sel()[0].begin()
	createdView.insert(edit, 0, txtResponse)
	version_format  = "%Y-%m-%d-%H-%M-%S"
	guid=str(uuid.uuid4())
	unique_filename = ("details-%s-%s" % (time.strftime(version_format), guid))
	fullSavePath = os.path.join(strPath, unique_filename)
	os.chdir(strPath)
	print("fullSavePath: %s" % fullSavePath)
	#createdView.run_command("save", args={"filename": fullSavePath})

	createdView.retarget(fullSavePath)
	createdView.run_command("save")
	#createdView.save(fullSavePath)
	#self.window.run_command("save")
	#createdView.run_command("save")
	return fullSavePath

class NexusEvaluationCommand(sublime_plugin.TextCommand):
	def run(self, edit):	
		print ("NexusEvaluationCommand_run")
		#print("ExampleCommand")
		#txtResponse="Hello World!"
		#/Users/camerontownshend/Documents/Cameron/dev/learnNPM/simpletest/package.json
		#print (self.view.file_name())
		strFullFileName=self.view.file_name()		
		#strPath='\\'.join(strFileName.split('\\')[0:-1])
		strPath, strFileName = os.path.split(os.path.abspath(strFullFileName))
		print("strFullFileName: %r, strPath: %r, strFileName: %r" % (strFullFileName, strPath, strFileName))
		txtMessage="Please select a package.json before continuing"
		isPackageJason=(strFileName==None or strFileName.find("package.json") == -1)
		if (isPackageJason):
			handleError(self, edit, txtMessage + str(test))		
			return (txtMessage)

		# intFind=strFileName.find("package.json")
		# if (intFind==-1):
		# 	handleError(self, edit, txtMessage)
		# 	return ("not found")

		#strFileName = "/Users/camerontownshend/Documents/Cameron/dev/learnNPM/simpletest/package.json"
		strJsonFile = generateShrinkWrap(strPath, strFileName)
		txtMessage="Could not generate ShrinkWrap"
		if (strJsonFile==None):
			handleError(self, edit, txtMessage)		
			return (txtMessage)

		#strJsonFile = generateShrinkWrapMock(strFileName)

		fileContents = loadShrinkWrap(strJsonFile)
		txtMessage="Could not load ShrinkWrap"
		if (fileContents==None):
			handleError(self, edit, txtMessage)		
			return (txtMessage)

		dependencies = parseShrinkWrap(fileContents)
		txtMessage="Could not parse ShrinkWrap"
		if (dependencies==None):
			handleError(self, edit, txtMessage )		
			return (txtMessage)

		componentlist = nexusFormat(dependencies)
		txtMessage="Could not parse Convert to Nexus Format"
		if (componentlist==None):
			handleError(self, edit, txtMessage)		
			return (txtMessage)

		#now the rubber hits the road
		json_obj = evaluateComponent(componentlist)

		print ("json_obj")
		print(json_obj)
		txtMessage="Could not evaluate Components"
		if (json_obj==None):
			handleError(self, edit, txtMessage)
			return (txtMessage)
		
		txtMessage="Could not evaluate Components"
		fullSavePath = saveOutput(self, edit, json_obj, strPath)		
		if (fullSavePath==None):
			handleError(self, edit, txtMessage)
			return (txtMessage)

		numFound=hasSecurityIssues(json_obj)
		if numFound>0:
			txtMessage = "%d Security issues found" % numFound
			handleError(self, edit, txtMessage)
