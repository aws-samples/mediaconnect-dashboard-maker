#  a simple CW dashboard maker for AWS Elemental MediaConnect metrics
#  v7 02-2024
#  added FlowConnected metric to payload
#
import os
import json
from json import JSONEncoder
import code
import time
from time import gmtime, strftime
import datetime
from datetime import datetime
import subprocess 
import copy
##
myversion = "07"
# ------------------------------------------------------------------------------------
# Definition dictionaries of various metrics follow:
#
EMX_SourceBitRate_widget_d = {
            "type": "metric",
            "height": 6,
            "width": 18,
            "y": 6,
            "x": 0,
            "properties": {
                "metrics": [
                    [ "AWS/MediaConnect", "SourceBitRate", "FlowARN", "firstarn", { "label": "flow1name" } ],
                ],
                "view": "timeSeries",
                "stacked": "false",
                "region": "us-west-2",
                "title": "Source Bitrates",
                "period": 30,
                "stat": "Average"
            }
}
##-----------------------------------------------------------------------------
EMX_SourceConnected_widget_d = {
            "type": "metric",
            "height": 6,
            "width": 18,
            "y": 6,
            "x": 0,
            "properties": {
                "metrics": [
                    [ "AWS/MediaConnect", "SourceConnected", "FlowARN", "firstarn", { "label": "flow1name" } ],
                ],
                "view": "timeSeries",
                "stacked": "false",
                "region": "us-west-2",
                "period": 30,
                "stat": "Minimum",
                "title": "SourceConnected",
                "yAxis": {
                    "left": {
                        "min": 0
                    }
                }
            }
        }

##-------------------------------------------------------------------------------------------------------

EMX_SourceRecoveredPackets_widget_d = {
            "type": "metric",
            "height": 6,
            "width": 18,
            "y": 18,
            "x": 0,
            "properties": {
                "metrics": [
                    [ "AWS/MediaConnect", "SourceRecoveredPackets", "FlowARN", "firstarn", { "label": "flow1name" } ],
                ],
                "view": "timeSeries",
                "stacked": "false",
                "region": "us-west-2",
                "title": "Source Recovered Packets",
                "period": 30,
                "stat": "Maximum",
                "yAxis": {
                    "left": {
                        "min": 0
                    }
                }
            }
}
##-------------------------------------------------------------------------------------------------------
EMX_SourceNotRecoveredPackets_widget_d =  {
            "type": "metric",
            "height": 6,
            "width": 18,
            "y": 24,
            "x": 0,
            "properties": {
                "metrics": [
                    [ "AWS/MediaConnect", "SourceNotRecoveredPackets", "FlowARN", "firstarn", { "label": "flow1name" }  ],
                ],
                "view": "timeSeries",
                "stacked": "false",
                "region": "us-west-2",
                "title": "Source Not Recovered Packets",
                "period": 30,
                "stat": "Maximum"
            }
}
##---------------------------------------------------------------------------
EMX_SourceFECRecovered_widget_d = {
            "type": "metric",
            "height": 6,
            "width": 18,
            "y": 30,
            "x": 0,
            "properties": {
                "metrics": [
                    [ "AWS/MediaConnect", "SourceFECRecovered", "FlowARN", "firstarn", { "label": "flow1name" }  ],
                ],
                "view": "timeSeries",
                "stacked": "false",
                "region": "us-west-2",
                "title": "Source FEC Recovered Packets",
                "period": 30,
                "stat": "Average",
                "yAxis": {
                    "left": {
                        "min": 0
                    }
                }
            }
        }
#-------------------------------------------------------------------------------------------------------
EMX_SourceContinuityCounter_widget_d = {
            "type": "metric",
            "height": 6,
            "width": 18,
            "y": 12,
            "x": 0,            "properties": {
                "metrics": [
                    [ "AWS/MediaConnect", "SourceContinuityCounter", "FlowARN", "firstarn", { "label": "Label-flow1name" }  ],
                ],
                "view": "timeSeries",
                "stacked": "false",
                "region": "us-west-2",
                "title": "Source Continuity Counter Errors",
                "period": 30,
                "yAxis": {
                    "left": {
                        "label": "Incorrectly Ordered or Lost Pkts",
                        "min": 0
                    }
                },
                "stat": "Maximum"
            }
}
        

#-----------------------------------------------------------------------------------------------------
## Aggregate all the metrics dictionaries into a list of dictionaries
WidgetsList = [EMX_SourceConnected_widget_d,EMX_SourceBitRate_widget_d,EMX_SourceRecoveredPackets_widget_d,EMX_SourceNotRecoveredPackets_widget_d,EMX_SourceFECRecovered_widget_d,EMX_SourceContinuityCounter_widget_d]
#-----------------------------------------------------------------------------------------------------
def GetCLIResult(mycmd):
        try:
                result = subprocess.run(mycmd, stdout=subprocess.PIPE)
                DecodedReply = json.loads(result.stdout.decode('utf-8'))
                return(DecodedReply)
        except:
                print("Could not get valid CLI resonse to cmd: ",mycmd)
                #code.interact(local=globals())
                exit()
#-------------------------------------------------------------------------------------------------------
tnow = datetime.now()
tstamp = tnow.strftime("%m%d%y_%H%M%S")
#-------------------------------------------------------------------------------------------------------
quote='"'
print("\n","========== WELCOME TO THE EASY DASHBOARD MAKER v",myversion," ============")
print("   This script makes a Dash for: MediaConnect Input Monitoring","\n\n")
print("\n","\n",)
Answers = ['a','t','s']
RunMode = input("--> This script can include [a]ll Flows, [t]agged Flows, or a [s]ingle Flow. Please choose a,t,s ? (any other char quits) " )
if RunMode not in Answers:
	print("----> exiting.") 
	exit()
	
	##--------------------------------------------------------------------------------------
## Poll for all channels before we parse down the List
AllCannelsJSON_d = {'Flows': [{}]}  ## empty dictionaries for all channels and target flows
FLOWLIST= {'Flows': []}
##

cmd = ['/usr/local/bin/aws','--no-paginate','mediaconnect','list-flows']
try:
	AllCannelsJSON_d = GetCLIResult(cmd)
except:
	print("!! No valid reply from list-flows call. Sorry!!  --> Exiting .")
	exit()

ChCount = len(AllCannelsJSON_d['Flows'])
if (ChCount == 0 ):
	print("---> No Flows found for this Account in this region; exiting.")
	exit()	
		
##--------------------------------------------------------------------------------------
if RunMode == 't' :
	MyProjectName = input(" -> Please enter the value of the ProjectName to use when selecting Flows for this Dashboard: " )
	if (MyProjectName == ""):   ## default value = 'myproject'
		print("  --> This option requires a value for the Tag called ProjectName. Exiting.")
		exit()
	
	#code.interact(local=globals())
	for ChIndex in range (0, ChCount):  ## now we iterate all the chx matching tags
		flowarn = AllCannelsJSON_d['Flows'][ChIndex]['FlowArn']
		
		cmd = ['aws','mediaconnect','list-tags-for-resource', '--resource-arn',flowarn]
		flowtags = GetCLIResult(cmd)
		print("\n\n","-->Retrieved tags: ",flowtags, "from ",AllCannelsJSON_d['Flows'][ChIndex]['Name'])
		ChPointer = AllCannelsJSON_d['Flows'][ChIndex]
		if ('Tags' in flowtags) and ( 'ProjectName' in flowtags['Tags']) and (flowtags['Tags']['ProjectName'] == MyProjectName):
			print("----> Found matching Flow ",AllCannelsJSON_d['Flows'][ChIndex]['Name'])
			TLL = len(FLOWLIST['Flows'])
			#code.interact(local=globals())
			FLOWLIST['Flows'].append(ChPointer)
			
		else:
			print(" ...")
	
	#code.interact(local=globals())
##------------------------------------------------------------------------------------
if RunMode == 's' :
	# display all channels and prompt for desired channel ID
	
	print("\n\n","  This account has the following Flows defined:")	
	print("  ","NAME","                                ","ID")
	for ChIndex in range (0, ChCount):  ## now we list all the chx
		chName = (AllCannelsJSON_d['Flows'][ChIndex]['Name'])
		chName = chName.ljust(32, ' ')
		chanID = (AllCannelsJSON_d['Flows'][ChIndex]['Description'])
		print("  ",chName, "    ",chanID)
	
	print("\n")
	SingleCh = input("--> Specify (copy+paste) the Name of the Flow to use: ")
	
	for ChIndex in range (0, ChCount):  ## now we iterate all the chx matching by ID
		ChPointer = AllCannelsJSON_d['Flows'][ChIndex]
		if (SingleCh == ChPointer['Name'] ):
			print("----> Adding single flow",ChPointer['Name'])
			#code.interact(local=globals())
			FLOWLIST['Flows'].append(ChPointer)
			break
		else:
			print(" ...")
	
	#code.interact(local=globals())
##------------------------------------------------------------------------------------
if RunMode == 'a' :
	FLOWLIST = copy.deepcopy(AllCannelsJSON_d)
	#code.interact(local=globals())
##------------------------------------------------------------------------------------
print("\n\n","---> Processing", len(FLOWLIST['Flows'])," Channel(s) for new Dash...","\n")
##	
##===============================================================================================
## ===  WORK ON TARGET dict 'FLOWLIST' FROM THIS POINT FORWARD  ===========================
##===============================================================================================


# ------------------------------------------------------------------------------------
# Set region and compare later
myregion = "us-east-1"
FlowCount = len(FLOWLIST['Flows'])
MetricTemplateLine = [ "...", "thisarn"]
# ------------------------------------------------------------------------------------
quote='"'
FlowRow = -1
print("\n","========== WELCOME TO THE DASHBOARD MAKER v",myversion," ============")
print("   This script makes a CloudWatch Dashboard for:  MediaConnect Flow Monitoring","\n\n")


# ------------------------------------------------------------------------------------
## Iterate through all the discovered flows add them to each widget 

for FlowIndex in range (0, FlowCount):
	FlowRow = (FlowRow + 1)
	FlowName = ""
	MetricTemplateLine = [ "...", "nextarn", { "label": "labelvalue" } ]
	thisFlowName = (FLOWLIST['Flows'][FlowIndex]['Name'])
	thisFlowArn = (FLOWLIST['Flows'][FlowIndex]['FlowArn'])
	thisFlowAZ = (FLOWLIST['Flows'][FlowIndex]['AvailabilityZone'])
	FlowDesc = (FLOWLIST['Flows'][FlowIndex]['Description'])
	FlowName = FlowName.ljust(32, ' ')
##
	print("\n","--> Scanning Flow ",thisFlowName)
	cmd = ['aws','--no-paginate','mediaconnect','describe-flow','--flow-arn',thisFlowArn]
	try:
		CLIReply = GetCLIResult(cmd)
        #print("DecodedReply has heys", CLIReply.keys())
	except:
		print("!! No flow info found on query: ",thisFlowName)
		print("!! Please report this to the author via AWS Support. ")
		print("!! Exiting.")
		exit()

	ThisFlowjson = CLIReply
	
	arnstring=str(thisFlowArn)
	arnlist=arnstring.split(":",9)
	thisSourcearn = (CLIReply['Flow']['Source']['SourceArn'])

	if (myregion != arnlist[3]) :
		myregion = arnlist[3]
		print("-----> Setting region to ",myregion," but you can change it later if needed.")

	
##----------------------------------------------------------------------------------
## check source of this flow 

	

	thislabel = thisFlowName
	if (FlowRow == 0) :
			# we are in the first line of each metric - special case due formatting needed
		
			for counter in range ( 0, len(WidgetsList) ) :
				try:
					WidgetsList[counter]['properties']['metrics'][0][3] = thisFlowArn
					WidgetsList[counter]['properties']['metrics'][0][4]['label'] = thislabel
					WidgetsList[counter]['properties']['region']= myregion
					print("------> Initializing Widget ")
				except:
					print("unable to add row 0 the widgets for Flow ",thisFlowName, "...continuing..." )
				
	
	else:
			## we are in rows 2-N, so add a line to each metric: 
			
			for counter in range (0,len(WidgetsList)) :
				WidgetsList[counter]['properties']['metrics'].append(MetricTemplateLine)
			## now set the values		
			try:
				for counter in range (0,len(WidgetsList)) :
					print("---------> Adding another row to widgets...")
					WidgetsList[counter]['properties']['metrics'][FlowRow][1] = thisFlowArn
					WidgetsList[counter]['properties']['metrics'][FlowRow][2]['label'] = thislabel
					#code.interact(local=globals())
			except:
				print("unable to add a row to the widgets for Flow ",thisFlowName, "...continuing..." )

	
	print(".")

# ------------------------------------------------------------------------------------

FileOpen = '{"widgets": ['
FileClose = ']}'
## 
##  Assemble full JSON as a list of strings 
WidgetStringsList=[]
#
FullJSON = FileOpen
for counter in range (0, len(WidgetsList)) :
	S = str(WidgetsList[counter])
	S = S.replace('(','')
	S = S.replace(')','')
	S = S.replace("'",'"')
	S = S.replace('"false"','false')
	S = S.replace('"true"','true')
	S+=","
	FullJSON+=S
##
##remove the comma after final widget and finish the JSON
FullJSON = FullJSON[:-1]
FullJSON+=FileClose
##
print("")
dashfile = "MediaConnect_dashjson_" + tstamp
f = open(dashfile, 'w')
f.write(FullJSON) 
f.close()
#
tyellow="\033[1;33;40m"
tnormal="\033[0;37;40m"
print(tnormal,"\n")


print("----> Dash JSON exported to local file '", dashfile, "' for future reference." )    
##
### now create the dashboard 
dashname = "MediaConnect_Flows_Dash_" + tstamp
dashcmd = "aws cloudwatch put-dashboard --dashboard-name "+ dashname +" --dashboard-body file://" + dashfile
print("\n","================================================")
print(" Attempting to create new dashboard ",dashname, "in your CW Console. You can rename the dash via the Console.")
dashresult = os.popen(dashcmd).read()
print("\n\n"," Cloudwatch upload result was: (empty [ ] means no errors) ","\n",dashresult)
print(" Remember to set the time range for your new Dashboard (upper right corner of CW Console).")

exit()
