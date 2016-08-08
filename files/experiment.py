#file: experiment.py
#this is where you will define the experimentClass class, subjectClass class, and monitorClass class
from __future__ import print_function
import os
from twisted.internet import reactor

class experimentClass():
   # - the dictionary self.data will be stored automatically every 10 seconds.
   # - store data in self.data[subjectID] which is a Subject class (defined below)
   # - send messages like self.customMessage(subjectID,msg)
   # - list of all subjects at self.data['subjectIDs']
   def __init__(self,config):
      # initialize the class
      self.config=config
      self.setParameters()

   def setParameters(self):
      self.data['exchangeRate']=.1
      self.data['currentClicks']={}
      self.currentMatch=-1
 
   def sendParameters(self,sid):
      msg={}
      msg['payoffVariable']=2
      msg['type']="sendParameters"
      self.customMessage(sid,msg)

   def setMatchings(self):
      #This function is needed, DO NOT DELETE
      #This is run when you stop accepting clients.  This is where you might want to do your random matching, or randomly determine parameters for the experiment.
      print(self.data['subjectIDs'])
   
   def reconnectingClient(self,client):
      #This function is needed, DO NOT DELETE
      sid=client.subjectID
      self.sendParameters(sid)
      self.updateStatus(sid)

   def startExperiment(self,message,client):
      #this is run when you click the "start Experiment" button on the monitor page.
      self.taskDone(message)
      self.startMatch()
      print("Starting Experiment!")

   def startMatch(self):
      #add 1 to self.currentMatch
      self.currentMatch=self.currentMatch+1
      #set current clicks for this match to 0
      self.data['currentClicks'][self.currentMatch]=0
      #update status of all clients
      for sid in self.data['subjectIDs']:
         self.data[sid].status={"page":"game","numberClicks":0,"currentMatch":self.currentMatch}
         self.updateStatus(sid)

   def makeChoice(self,message,client):
      #this function is run when the sever receives a message from a client such that message['type']="makeChoice"
      #get subjectID
      sid=client.subjectID
      #Add 1 to the number of currentClicks for self.currentMatch
      self.data['currentClicks'][self.currentMatch]=self.data['currentClicks'][self.currentMatch]+1
      #Record the data to self.data to be saved. This adds a list [currentMatch,#clicks] to self.data[sid].choices     
      self.data[sid].choices.append([self.currentMatch,self.data['currentClicks'][self.currentMatch]])
      #Check if there are more than 10 clicks, if so run self.endMatch, otherwise, run self.updateClicks      
      if self.data['currentClicks'][self.currentMatch]>10:
         self.endMatch()
      else:
         self.updateClicks()

   def updateClicks(self):
      #update status of all clients
      for sid in self.data['subjectIDs']:
         self.data[sid].status={"page":"game","numberClicks":self.data['currentClicks'][self.currentMatch],"currentMatch":self.currentMatch}
         self.updateStatus(sid)

   def endMatch(self):
      #update status of all clients
      for sid in self.data['subjectIDs']:
         self.data[sid].status={"page":"postMatch","stage":"noChoices"}
         self.updateStatus(sid)
      #wait 10 seconds, and then run self.startMatch to start the next match
      reactor.callLater(10,self.startMatch)


class subjectClass():
   def __init__(self):
      #the subjectID is automatically defined in server.py, and can be accessed with self.subjectID
      #every time the client clicks the button will be recorded here.
      self.choices=[]
      #the total payoffs are recorded here
      self.totalPayoffs=0
      #the subject status is initialized here.  Any time this is changed, you can update the client with self.updateStatus(subjectID)
      self.status={}
      self.status['page']="generic"
      self.status['message']=["Please read, sign, and date your consent form. <br> You may read over the instructions as we wait to begin."]

class monitorClass():
   def __init__(self):
      self.monitorTasks()

   def getMonitorTable(self):
      table=[]
      #define the titles for the table here
      titles=['#','subjectID',"Connection","Status","Total"]
      try:
         #add the entries for the monitor table for each subject.
         for subjectID in self.data['subjectIDs']:
            this=[]
            refreshLink="<a href='javascript:void(0)' onclick='refreshClient(\"%s\");'>%s</a>"%(subjectID,subjectID)
            this.append(refreshLink)
            this.append(self.data[subjectID].connectionStatus)
            this.append("%s"%(self.data[subjectID].status['page']))
            this.append("$%.02f"%(self.data[subjectID].totalPayoffs))
            table.append(this)
      except Exception as thisExept: 
         print("can't get table at this time because:")
         print(thisExept)
      return table,titles
   
   def monitorTasks(self):
      #define the monitor tasks here.
      taskList=[]

      #a task is defined like below (you can have as many as you want:
      #a button will appear on the monitor page that has this title msg['title']
      # when it is clicked, it will run the function msg['type'], (in this case self.startExperiment)
      msg={}
      msg['title']='Start Experiment'
      msg['type']='startExperiment'
      msg['status']=''
      taskList.append(msg)

      for k in range(len(taskList)):
         taskList[k]['index']=k

      self.data['monitorTasks']=taskList


