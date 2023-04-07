# DecentraliDrone: A Decentralized, Fully Autonomous Drone Delivery System

Welcome to DecentraliDrone, a reliable and efficient drone delivery system for transporting goods. Our system is fully autonomous and decentralized, meaning that it operates without the need for human intervention and relies on a distributed network of drones and devices to function.

# Features

1. Fully autonomous operation: DecentraliDrone drones are equipped with advanced sensors and navigation systems that allow them to fly to their destinations and make deliveries without the need for human intervention.

2. Decentralized network: Our system relies on a decentralized network of drones and devices to function, which helps to ensure that deliveries can be made even if individual drones or devices fail.

3. Reliable delivery: DecentraliDrone drones are designed to be reliable and efficient, with advanced algorithms that help them navigate to their destinations quickly and safely.

4. Wide coverage area: Our drones are capable of flying long distances and can make deliveries to a wide range of locations.

# Figma Design

Here's the link to our Figma design for the application UI: [https://www.figma.com/file/uUzRa5nWk5w5iCr6rFJvrs/Drone-Delivery-App-Prototype?node-id=33%3A444&t=NZsoGaZYzjknIV5f-1] 

# Instructions to run the project

1. Clone the repository

2. Download Unreal Engine 4.27 from the Epic Games Store

3. A strong internet connection is recommended while downloading the engine and the binaries.

4. Download the precompiled binaries for AirSimNH from [here](https://github.com/Microsoft/AirSim/releases) and place them in the AirSimNH folder.

5. Copy the settings file for AirSim from `settings/set2.json` and paste it on your AirSim's `settings.json` file.

6. Open the folder containing the precompiled binary, find AirSimNH executable and run it.

7. Open VSCode and open the folder containing the project, navigate to dbg.py and run it.

The drones should now carry out a fixed delvery route and make deliveries to the specified locations. The drone's camera feed can be viewed in the Unreal Engine window. This uses the `td3_per` algorithm to make decisions for autonomously avoiding obstacles and making deliveries.

# Hardware Requirements

 - A computer with a minimum of 8GB RAM and a 2.5GHz processor.
    - A graphics card with at least 4GB of VRAM.
    - A minimum of 100GB of free disk space.

# Software Requirements
 - Python 3.10.0 
 - Unreal Engine 4.27 
 - AirSim 1.5.0
    - OpenCV 4.5.3
    - Numpy 1.21.2
    - Scipy 1.7.1
    - Matplotlib 3.4.3
    - Pytorch 1.9.0
 - Tensorflow 2.5.0
 - Keras 2.5.0

