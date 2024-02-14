# Daily Manager
A tool to manage tasks that you do every day 

## Description

A tool with an user interface that minimizes into the system tray when closed. It is used to manage daily tasks that the user has.

## Getting Started

### Dependencies

* Python
* pandas
* tkinter
* webbrowser
* pystray

### Installing

* Install all the modules listed in the dependencies
* Simply open a command line interface at the main.py file's location.

## Using the app

### Main Window
The user will see a window where they can see all of their daily tasks. Here they can interact with their daily tasks as well as create new daily tasks.

![input](https://github.com/JurajBorkaCode/World-data-viewer/blob/main/main%20window.PNG)

The user can interact by:
* Opening a daily task - This either opens a website or an application based on the users input when creating the daily task
* Complete a daily task - This sets a daily tasks status to complete and turns it green in the list
* Delete a daily task - This will delete a daily task from the list

* Once you fill in all of the information, you will be prompted asking you wether you want to generate the map.

* A SVG map will be generated and a list of unsupported countries will be listed.

![output](https://github.com/JurajBorkaCode/World-data-viewer/blob/main/new%20daily.PNG)

The user can create new daily tasks by filling in the fields. They can select what type of shortcut to use by clicking the daily type dropdown menu and the inputting the shortcut into the daily shortcut input box. This allows users to quickly access the daily tasks.

### System Tray
When the user closes the main window, the app will be minimized into the system tray and be given a dynamic menu.

![output](https://github.com/JurajBorkaCode/World-data-viewer/blob/main/system%20tray.PNG)

The user will be able to see all of their daily tasks from the menu. The tasks will be grayed out if they have been completed. If they have not been completed and they have a shortcut, the user will be able to click on them to open the daily task.

## Help
### moving to a new device
All of the data is stored in a dailies.csv file so if a user is moving to a new device, they just have to transfer the CSV file.

## Authors

Juraj Borka