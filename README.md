# BGP Simulator

This project, named BGP-simulator, is developed as part of the DTEK8060 Protocol Processing and Security course. The objective of this project is to build a scalable and customizable simulator of inter-AS routing using the BGP protocol. The network must consist of a minimum of 10 routers, and the simulator is implemented in Python with some shell scripts to automate the setup.

## Project Overview

The BGP-simulator project aims to create a realistic simulation of inter-AS routing using BGP (Border Gateway Protocol). The system includes virtual interfaces representing routers (servers) and interfaces (clients) that establish TCP/IP connections. The project employs shell scripts for automation, especially in handling system-level configurations, to achieve a close approximation to real-world scenarios.

## Prerequisites

### Linux

- Install the following packages:
  - `uml-utilities`
  - `net-tools`
  - `iproute2`

### Windows

To run this project on Windows, you need to perform the following steps:

1. **Enable Virtualization in BIOS Settings**: Ensure that virtualization is enabled in your BIOS settings.

2. **Enable Hyper-V Feature**: Use one of the following methods:
   - Enable Hyper-V from the Windows features menu (optionalfeatures.exe).
   - Use the following command as an administrator and restart your PC:
     ```
     DISM.exe /Online /Enable-Feature /All /FeatureName:Microsoft-Hyper-V /NoRestart
     ```

3. **Configure Virtual Switch in Hyper-V Manager**:
   - Open Hyper-V Manager from the start menu or using the Run dialog box by typing `virtmgmt.msc`.
   - Go to Virtual Switch Manager, create a new Virtual Network Switch, and select the 'External' type. Click 'OK'. Ensure you select 'External' type for the virtual network switch.

4. **Creating Virtual Interfaces**:
   Unfortunately, there is no script provided for Windows. You will need to create the interfaces manually. To simulate around 40 interfaces for 10 routers, run the following command 40 times:
   ```
   Add-VMNetworkAdapter -Switch switch -ManagementOS
   ```
Ensure that you replace `switch` with the actual switch name you created earlier on step 3.
If you're confused, check this [StackEchange](https://superuser.com/questions/1299022/creating-a-virtual-nic-that-connects-to-the-same-network-as-physical-nic)

## Installation

To install the BGP-simulator, follow these steps:

1. Verify that `pip` is installed on your machine.

2. Open a command prompt and run the following setup script:
   ```
   bash scripts/setup.sh
   ```

## Running the Simulator

The simulator requires `sudo` privileges since it involves changing network configurations. To run the simulator, execute the following command:
   ```
    sudo python3 main.py
   ```

## Running in Docker

You can also run the BGP-simulator within a Docker container. Here are the steps:

1. Build the Docker image using the following command (replace `my-app` with your desired image name):

   ```
    docker build -t my-app .
   ```
2. Run the Docker container using the following command:
    ```
    docker run --rm -it --network host --privileged my-app
    ```

Please make sure you have Docker installed and properly configured on your system.

## Disclaimer

This project is intended for educational purposes and should be used responsibly and within the bounds of your institution's ethical guidelines and policies. Simulation of network protocols may have legal and ethical implications, so use this software responsibly and only for the intended purposes of your course.

For any issues or questions related to the BGP-simulator, feel free to contact the project maintainers.

**Note:** This readme assumes a basic understanding of networking concepts, Linux, and Windows operating systems.
