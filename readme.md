# IoT Smart Irrigation system

This is a short project created during 2018's UoE EaRS IoT challenge.

## Aims

The aim of this project was to create an open source, automatic irrigation system, to give anyone the ability to automate one more thing away using the magic of IoT.

The system uses low-power LoPy devices to collect local data about the user's environment (humidity, temperature, sunlight intensity), transmit that data to the cloud for processing, process the data with the computational power of a cloud-hosted solution (potentially incorporating historic data, weather forecasts, and presenting the data to the user in a web app / phone app format), and control any given irrigation valves automatically based on the need.


## Parts of the system 

LoPy parts: low-power components using LoRa for communication, to make power draw minimal and maximize reach - these can be placed pretty much anywhere around the propery the user decides (with the exception of the controller, which will draw more power thanks to the WiFi communication with the cloud, and should be somewhere inside the house, connected to an electric outlet.

Parts of the system (each in its own folder):

- LoPy controller: listens for data from sensors, transmits commands to actuators, communicates with the cloud
- LoPy sensor: uses various sensors (currently hooked up to an Arduino) to sense data about the environment; communicates over LoRa
- LoPy actuator: controls valves or other irrigation-relevant equipment. Receives data over LoRa.
- Cloud server: communicates with the LoPy controller, processes data and decides when and what actuators to turn on.
- Android app: tentative UI for the server - would show data, forecasts, allow manual override. 


## Current state

Currently, the server does a very rudimentaty calculation to decide when to turn the actuators on - it decides only based on the ground humidity. Ideally, it'd use weather forecasts and more different measures and sensors; we didn't have time to get that working during the hackathon. For the same reasons, the app does not yet connect to the server. All of the data flow and logic between the LoPy components and the cloud server work, though - it just uses LEDs instead of turning actual valves because we didn't have, well.. valves.

## Stretch goals

A stretch goal we have been considering is an automated defence system: this kind of low-power mesh of sensors and actuators could be extended with presence detection systems, maybe hooked up to the main home security system, and could remotely turn on hoses which would spray an intruder with gasoline, then produce a spark close to them. Somewhat gruesome, but could help in a zombie apocalypse scenario
