# PiVide
### Controlling an Anova Bluetooth Sous Vide with a Raspberry Pi Zero 

I have taken this projected from a forum post I found [here](https://community.mydevices.com/t/connecting-the-anova-precision-cooker-to-cayenne) which I found lacking a lot of detail which was also confirmed by confusion I saw on reddit.  I decided to expand on the instructions.  This tutorial assumes that you have successfully installed Raspbian on a Pi Zero W and have terminal access.  I have made a slight change in the included code to read in fahrenheit.  

1. Install python-pip and libglib2.0-dev
```
sudo apt-get install -y python-pip libglib2.0-dev
```

2. Using PIP install bluepy and chyenne-mqtt
```
sudo pip install bluepy cayenne-mqtt
```

3. Using pip install pycirculate --pre
```
sudo pip install pycirculate --pre
```

3. using hcitool scan for the MAC address of the Sous Vide.  It will display with the name Anova
```
sudo hcitool lescan
```
<img src="/images/ReadMe/hcitool.jpg">  

4. Create PiVide folder
```
sudo mkdir /opt/PiVide
```

5. Download the script to PiVide folder
```
sudo wget https://raw.githubusercontent.com/STLWaffles/PiVide/master/PiVide.py -P /opt/PiVide
```

6. Make the script executable
```
sudo chmod +x /opt/PiVide/PiVide.py
```

7. Create a free account at [mydevices](https://mydevices.com/)

8. Select Create App
<img src="/images/ReadMe/CreateApp.jpg">

9. Select Bring Your Own Thing
<img src="/images/ReadMe/BYO.jpg">

10. Note your MQTT Username and Password and Client ID.  Minimize the browser on this page
<img src="/images/ReadMe/MQTT.jpg">

11. using your favorite editor, update the below settings with the data from step 10(Yes I use nano)
```
sudo nano /opt/PiVide/PiVide.py
```
```
MQTT_USERNAME = "..."
MQTT_PASSWORD ="..."
MQTT_CLIENT_ID = "..."
ANOVA_MAC_ADDRESS = "..."
```

12. Start the Python Script
```
sudo python /opt/PiVide/PiVide.py
```

13. Open the browser from step 10.  It will now be a dashboard with 3 widgets on it.
<img src="/images/ReadMe/myDevices1.jpg">
  
14. Create a new project by clicking on the "Create New Proj..." button at the top and name it whatever you feel like.
<img src="/images/ReadMe/myDevices2.jpg">

15. Add a new widget by clicking on "Add New..." and then "Device/Widget"
<img src="/images/ReadMe/myDevices3.jpg">

16. Select "Custom Widget"
<img src="/images/ReadMe/myDevices4.jpg">

17. Create a "Value" Widget
<img src="/images/ReadMe/myDevices5.jpg">

18. Set the below parameters and click "Add Widget"
```
Name: Current Temp F
Channel: 1
Icon: Thermometer
```
<img src="/images/ReadMe/myDevices6.jpg">

19. Repeat steps 15-18 for channel 3 with the parameters below for the Temp the Sous Vide is set to
```
Name: Set Temp F
Channel: 3
Icon: Thermometer
```
<img src="/images/ReadMe/myDevices7.jpg">

20. Add a 3rd Custom Device/Widget with the type "Button"
<img src="/images/ReadMe/myDevices8.jpg">

21. Create the Widget with the below parameters 
```
Name: Run/Stop
Channel: 5
Icon: Fan
```
<img src="/images/ReadMe/myDevices9.jpg">

22. Add a 4th Custom Device/Widget with the type of "Value"  This is a binary on/off indicatator for the Sous Vide Fan)

23. Create the Widget with the below parameters
```
Name: Run Status
Channel: 2
Icon: Heart
```
<img src="/images/ReadMe/myDevices10.jpg">

24. Create a 5th custom Device/Widget with a type of "Slider"
<img src="/images/ReadMe/myDevices11.jpg">

25. Create the Widget with the below parameters
```
Name: Set Temp
Channel: 4
Slider Min Value: 32
Slider Max Value: 211
```
<img src="/images/ReadMe/myDevices12.jpg">

26. Select the project you created in step 14, and drag the new Widgets to the dashboard.  You can now control the Sous Vide from this dashboard.  This can also be controlled from your phone using the Cayenne app.
<img src="/images/ReadMe/myDevices13.jpg">

### Running PiVide at startup

1. Using your favorite editor create the service definition file and add the below content
```
sudo nano /lib/systemd/system/PiVide.service
```

```
[Unit]
Description=PiVide
After=multi-user.target

[Service]
Type=simple
ExecStart=/usr/bin/python /opt/PiVide/PiVide.py
Restart=on-abort

[Install]
WantedBy=multi-user.target
```

2. Reload systemctl daemon and start PiVide
```
sudo systemctl daemon-reload
sudo systemctl enable PiVide.service
sudo systemctl start PiVide.service
```

3. Check the service status
```
sudo systemctl status PiVide.service

```
<img src="/images/ReadMe/myDevices14.jpg">

4. Verify you are seeing data in your dashboard.  If it was not working you would see an offline message
<img src="/images/ReadMe/myDevices13.jpg">

5. Reboot the Raspberry Pi and verify the dashboard again.

















