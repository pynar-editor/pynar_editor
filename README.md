# Turkish Python Code Editor: PyNar

![pynar](https://user-images.githubusercontent.com/854154/194779188-b7c93de3-52e3-4e49-8e1c-9dd8e8d1e987.png)

This project developed an open-source coding environment with a fully Turkish interface for the Python language. The system is designed with three layers: the User Interface Layer, the Middle Layer, and the Python Interpreter Layer. Components in the User Interface Layer include the Python Code Editor and the Chatbot's user interface units. The Middle Layer contains the “Code Structural Control,” “Code Error Manager,” and “Intelligent Agent Subsystem.” The “Code Structural Control Module” detects syntax errors in the user's code. This is achieved through static code checking libraries without running the code. The “Code Error Manager” analyzes the error notifications obtained when the Python interpreter runs the user's code. The Chatbot Agent uses these insights to identify the cause of the student's error and suggests a solution using a machine learning subsystem. The best possible solution is determined and communicated to the user through the chatbot, and the error in the code is corrected if the user approves.

The proposed system is named "PyNar." PyNar is designed according to usability principles to ensure that beginners in coding can easily adapt to its ergonomics. The PyNar editor can be used as a standalone desktop software and has the capability to store written codes in the cloud. It can receive assignments assigned to the user by the instructor/teacher in the cloud and allow students to send their solutions back to the instructor. Furthermore, it enables error analysis for each user, reports the extent of learning, and performs plagiarism analyses of the solutions.

The coding editor is developed as a platform-independent desktop application that works on all operating systems. All project codes were uploaded to a public repository after project completion, and all necessary technical and user documentation was created to enable contributions from developers in our country.

If you are familiar with Python, you can set up and run the project as described in the "Installation and Running from Source Code" section below. If you are new to Python, you can download and install the compiled setup packages for Windows or Linux from the download link provided below.

## Installation and Running from Source Code

### a) Windows 10 and 11

First, Python 3.8 or higher should be installed on your computer. You can download it from this link:

    https://www.python.org/downloads/

If you have Git installed on your computer, create a local clone of this repository. If you are not using Git, download this repo as a zip file and extract it. Open a command prompt and navigate to the Pynar_Beta-main folder.

To install the required packages:

    pip install -r requirements.txt

![image](https://user-images.githubusercontent.com/854154/194746108-6d753b8b-2e2f-4626-a4ea-5d4e3844cd7b.png)

PyNar editor uses the open-source static code checking library [pyright](https://github.com/microsoft/pyright) to detect code errors before running the code. Download the compiled version of the Pyright program for Windows from [this link](https://www.pynar.org/releases/pyright/1.1.266/), and extract the win.zip file to any location. Copy the **pyright-win.exe** file and the **typeshed-fallback** folder from the dist folder to the **Bin** folder inside **PyNar_Beta-main**.

To run, execute the following command in the same folder to run the main.py file:

    python main.py

![image](https://user-images.githubusercontent.com/854154/194746862-960109b6-0193-4304-8f8a-7a5026036206.png)

### b) Linux (Debian-based distributions like Ubuntu, Pardus)

The following steps are given for Pardus 21 version but can be used for all Debian-based Linux distributions. Install the following packages:

    sudo apt-get update
    sudo apt-get install -y python3-pip

Navigate to the home directory of your current user:

    cd $HOME

After this, navigate to the folder where you extracted PyNar_Beta-main.zip:

    cd Downloads/PyNar_Beta-main/

Install the required packages:

    pip3 install -r requirements.txt

PyNar editor uses the open-source static code checking library [pyright](https://github.com/microsoft/pyright) to detect code errors before running the code. Download the compiled version of the Pyright program for Linux from [this link](https://www.pynar.org/releases/pyright/1.1.266/), and extract the linux.zip file to any location. Copy the **pyright-linux** file and the **typeshed-fallback** folder from the dist folder to the **Bin** folder inside **PyNar_Beta-main**.

To run, execute the following command in the same folder to run the main.py file:

    python3 main.py

## Compiled Versions for Windows or Linux

Setup programs for Windows 10 and 11 and DEB packages for Linux can be downloaded from the following link:

    https://www.pynar.org/releases/setup/

After downloading the package, the setup can be started by double-clicking for Windows. The setup program will automatically install Python if it's not already on your computer.

    Note: For some versions of Windows, if "SmartScreen" is active, a blue notification screen saying "Windows protected your PC" may appear. In this case, you can continue the installation by clicking "Run anyway." There is nothing harmful in the PyNar Editor setup program; this warning appears because we did not obtain a certificate for Windows due to the high cost.

For installation on Linux (for distributions using DEB package managers), the following command should be executed in the folder where you downloaded the pynar.deb package. The pynar.deb package depends only on the fonts-noto-color-emoji package. This package should be installed before installation.

    sudo apt-get install fonts-noto-color-emoji
    sudo dpkg -i pynar.deb

After the installation is complete, PyNar can be found under the "Education" section in the "Pardus" menu. Clicking it will create a link on the desktop, which can be used to start PyNar.

Note: Administrator rights are not required for the Windows installation, but root privileges are needed for installing Linux packages.

## Features and User Guide

All features of the PyNar editor and the user guide are published at the following link:

    https://www.pynar.org/help

## PyNar Editor Screenshot:

![image](https://user-images.githubusercontent.com/854154/194748948-71439f12-d8cc-4c48-84d8-45d07198d16e.png)

## Bug Reporting

You can report any potential bugs found in the program in the ***issues*** section. Please provide as much detail as possible when reporting errors.

## About

This project is supported by TÜBİTAK under the Priority Areas 1003-BIT-AKAY-2018-1 “Turkish Interface and Support Systems” within the scope of EEEAG 118E882 project titled "Developing a Turkish Python Code Editor with Intelligent Agents Based Interactive Help System that can Analyse Syntax Errors of Users."

## Contributing

If you wish to contribute to this project, you can contact the Project Lead via LinkedIn: [https://www.linkedin.com/in/ttbilgin/](https://www.linkedin.com/in/ttbilgin/)
