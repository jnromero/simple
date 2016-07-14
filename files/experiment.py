import os
from twisted.internet import reactor

class experimentClass():
   def __init__(self,config):
      "do init stuff"
      self.setParameters()
      self.config=config
      self.currentExperimentPath=self.config['webServerRoot']+self.config['currentExperiment']
      self.packageFolder=self.config['webServerRoot']+self.config['packageFolder']
      self.data['matchType']="regular"

   # - store data in self.data[subjectID] which is a Subject object (defined below)
   # - send messages like self.customMessage(subjectID,msg)
   # - list of all subjects at self.data['subjectIDs']

   def setParameters(self):
      self.data['exchangeRate']=.1
      self.data['experimentRunning']=0
      self.data['currentClicks']={}
      self.currentMatch=-1
 
   def sendParameters(self,sid):
      msg={}
      msg['payoffVariable']=2
      msg['type']="sendParameters"
      self.customMessage(sid,msg)

   def setMatchings(self):
      #This is run when you stop accecpting clients
      print self.data['subjectIDs']
   
   def reconnectingClient(self,client):
      sid=client.subjectID
      if self.data['experimentRunning']==1:#experimetn has started
         self.sendParameters(sid)
      self.updateStatus(sid)

   def startExperiment(self,message,client):
      #this is run when you click the "start Experiment" button on the server page.
      self.data['experimentRunning']=1
      self.taskDone(message)
      self.startMatch()
      print "Starting Experiment!"

   def startMatch(self):
      self.initializeTimer("all",20,self.endMatch)
      self.currentMatch=self.currentMatch+1
      self.data['currentClicks'][self.currentMatch]=0
      for sid in self.data['subjectIDs']:
         self.initializeTimer(sid,5,self.pleaseMakeChoice,sid)
         self.data[sid].status={"page":"game","numberClicks":0,"currentMatch":self.currentMatch}
         self.updateStatus(sid)

   def makeChoice(self,message,client):
      sid=client.subjectID
      self.initializeTimer(sid,10,self.pleaseMakeChoice,sid)
      self.data['currentClicks'][self.currentMatch]=self.data['currentClicks'][self.currentMatch]+1
      self.data[sid].choices.append([self.currentMatch,self.data['currentClicks'][self.currentMatch]])
      if self.data['currentClicks'][self.currentMatch]>10:
         self.endMatch()
      else:
         self.updateClicks()

   def pleaseMakeChoice(self,subjectID):
      msg={}
      msg['type']="pleaseMakeChoice"
      self.customMessage(subjectID,msg)

   def updateClicks(self):
      for sid in self.data['subjectIDs']:
         self.data[sid].status={"page":"game","numberClicks":self.data['currentClicks'][self.currentMatch],"currentMatch":self.currentMatch}
         self.updateStatus(sid)

   def endMatch(self):
      for sid in self.data['subjectIDs']:
         self.cancelTimerFunction(sid)
         self.data[sid].status={"page":"postMatch","stage":"noChoices"}
         self.updateStatus(sid)
      reactor.callLater(10,self.startMatch)


class Subject:
   def __init__(self):
      self.choices=[]
      self.guesses={}
      self.history={}
      self.correctGuesses={}
      self.myMatchPayoffs={}
      self.opponentMatchPayoffs={}
      self.bonusPay=0#In Dollars
      self.totalPayoffs=0#Me,You
      self.quizEarnings=0
      self.quizAnswers=[]
      self.name="default"
      self.desk="default"
      self.status={"page":"generic","message":["Please read, sign, and date your consent form. <br> You may read over the instructions as we wait to begin."]}

class serverClass():
   def __init__(self):
      "do init stuff"
      self.serverTasks()
   def getServerTable(self):
      table=[]
      titles=['#','subjectID',"Connection",'Name','Desk',"Status","Period","Choices","Total"]
      try:
         sortedSubs=[]
         for sid in self.data['subjectIDs']:
            sortedSubs.append([self.data[sid].desk,sid])
         sortedSubs.sort()
         for k in sortedSubs:
            subjectID=k[1]
            this=[]
            refreshLink="<a href='javascript:void(0)' onclick='refreshClient(\"%s\");'>%s</a>"%(subjectID,subjectID)
            this.append(refreshLink)
            this.append(self.data[subjectID].connectionStatus)
            this.append(self.data[subjectID].name)
            this.append(self.data[subjectID].desk)
            this.append("%s"%(self.data[subjectID].status['page']))
            if hasattr(self,'currentPeriods'):
               this.append("%s"%(self.currentPeriods[subjectID]))
            else:
               this.append("NA")
            this.append("%s"%(self.data[subjectID].totalPayoffs))
            totalPoints=self.data[subjectID].totalPayoffs
            totalPay=totalPoints*self.data['exchangeRate']+self.data[subjectID].quizEarnings
            this.append("$5+%.02f+%s=%.02f"%(totalPay,self.data[subjectID].bonusPay,totalPay+self.data[subjectID].bonusPay+5))
            table.append(this)
      except Exception as thisExept: 
         print "can't get table at this time because:"
         print thisExept
      return table,titles
   

   def serverTasks(self):
      taskList=[]

      thisPath=os.path.dirname(os.path.realpath(__file__))
      this=thisPath.find("/experiments/")
      thisPath=thisPath[this:]

      msg={}
      msg['type']='startQuiz'
      msg['title']='Start Quiz'
      msg['status']=''
      taskList.append(msg)

      msg={}
      msg['type']='startExperiment'
      msg['title']='Start Experiment'
      msg['status']=''
      taskList.append(msg)


      for k in range(len(taskList)):
         taskList[k]['index']=k

      self.data['serverTasks']=taskList


