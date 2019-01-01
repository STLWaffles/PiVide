#
#Connect your Anova to MyDevices Cayenne.
#

#import time and date stuff
import datetime
import time

#import Anova lib
from pycirculate.anova import AnovaController
#get Cayenne
import cayenne.client

#MQTT Credentials
MQTT_USERNAME = "..."
MQTT_PASSWORD ="..."
MQTT_CLIENT_ID = "..."

# Your Anova Address goes here, run `sudo hcitool lescan` and record
ANOVA_MAC_ADDRESS = "..."

#Cayenne message callback
def on_message(message):
  print("message received: " + str(message))

  #set the temperature setpoint if we get a slider message
  if message.channel == 4:
    ctrl.set_temp(message.value)
    print("Setpoint set to " + message.value + " degrees")

  if message.channel == 5:
    if (message.value == '1'):
      ctrl.start_anova()
      print("Anova Started")
    else:
      ctrl.stop_anova()
      print("Anova Stopped")


#Initialize Cayenne
client = cayenne.client.CayenneMQTTClient()
#Set the Cayenne message callback
client.on_message = on_message
#begin a Cayenne session
client.begin(MQTT_USERNAME, MQTT_PASSWORD, MQTT_CLIENT_ID)

#grab your Anova
ctrl = AnovaController(ANOVA_MAC_ADDRESS)

def main():
    print datetime.datetime.now()
    #Canadians do Celcius
    print ctrl.set_unit('f')

    i=0
    timestamp = 0

    while True:
      #Cayenne kick
      client.loop()

      #Call every 10 seconds
      if(time.time() > timestamp + 10):

        #send the current temperature
        client.celsiusWrite(1,ctrl.read_temp())

        #send the set temperature
        client.celsiusWrite(3,ctrl.send_command_async("read set temp"))

        #send the run status
        if (ctrl.anova_status() == 'stopped'): a_stat = 0
        else: a_stat = 1
        client.virtualWrite(2,a_stat)

        #save last timestamp
        timestamp = time.time()



#    print ctrl.read_temp(), ctrl.read_unit()
#    print ctrl.set_temp(TEMP)
#    print ctrl.start_anova()
#    print ctrl.anova_status()


if __name__ == "__main__":
    main()