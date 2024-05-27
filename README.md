# Bachelor's Thesis Practice
Greetings to everyone! In this repository, you will find instructions and explanations on how to implement the projects that were presented in my bachelor's thesis 
## This repository will include such projects as: 
1. Smart Home
2. Smart Plant
3. Combined SmartPlant SmartHome + Website

# Introduction

* [Components and tools](#components-and-tools)
* [Installation](#installation)
* [Usage and MircoPython](#Usage-and-MircoPython)
* [Examples](#examples)
* [References](#references)

Here we will take a closer look at the Thonny IDE and all the necessary tools to start the implementation

## Components and tools
1. Microcontroller ESP32
2. Driver for ESP32
3. Tohnny IDE

Basically, these are all the necessary components for a successful implementation

## Installation
1. To begin with, we need to install the development environment for Python, where we can write all the basic functionality that will be in the code. To do this, we install the [*Thonny IDE*](https://thonny.org/).

2. After successful installation, we go to our microcontroller and see which driver it uses. To do this, we find the chip, as shown in the picture, and its name will correspond to the driver we need
![13507ffc05e5c59bd7a2d0dd8626b4abf05b1bb4](https://github.com/BohTsR/BachThesis/assets/160582711/fa039be4-7348-40a0-ac09-ddadd442537d)

3. Next, we connect ESP32 to the computer, log in to Thonny and go to the Run section, where we select the Configure Interpreter section 
<img width="893" alt="Screenshot 2024-03-22 at 08 22 37" src="https://github.com/BohTsR/BachThesis/assets/160582711/6acef568-250a-47c7-9073-338abfd36240">


4. Next, we select "Install or update MircroPython" tab and select what is shown in the photo below 
<img width="654" alt="Screenshot 2024-03-22 at 08 31 53" src="https://github.com/BohTsR/BachThesis/assets/160582711/b46bdceb-c29d-4e7d-8994-80b382e6a9be">

5. After successful installation, we should see this message in the terminal, which means that we are ready to work with ESP32
<img width="585" alt="Screenshot 2024-03-22 at 08 34 36" src="https://github.com/BohTsR/BachThesis/assets/160582711/78d92adc-1b22-43fe-8aa5-e029acea22a4">

## Usage and MircoPython
For a simple health check, diodes are usually used to turn on/off, or write "Hello World" to the microcontroller itself.  
```python 
from machine import Pin
print("Hello world! Check")
```
