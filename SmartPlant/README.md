# Introduction

* [Components and tools](#components-and-tools)
* [Usage and MicroPython](#Usage-and-MircoPython)
* [Examples](#examples)
* [References](#references)

Here we will take a closer look at the Smart Plant project and all the necessary tools for its implementation.

## Components and tools
1. Microcontroller ESP32
2. Sensors, such us Soil Moisture
3. Driver for ESP32
4. Tohnny IDE

Basically, these are all the necessary components for a successful implementation.

## Usage and MicroPython
In this project, the most difficult part will be setting up the project itself, i.e. configuring the components so that they are fully autonomous.
In SmartPlant, you can see how the code works in general. At first, all the main components are initialized, such as relays, RGB LED Matrix, sensors for measuring soil moisture, and the current time. In the next part, you can see how 2 timers are used - one for sending data, and the other for the autonomous operation of the project.

