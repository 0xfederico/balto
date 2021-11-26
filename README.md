# Balto
[0. Introduction](#0-introduction)<br>
[1. Installation (Debian based distributions)](#1-installation-debian-based-distributions)<br>
[2. Populate the database](#2-populate-the-database)<br>
[3. Start the **development** server](#3-start-the-development-server)<br>
[4. Used technologies](#4-used-technologies)<br>
[5. License](#5-license)

## 0. Introduction
Balto is an FLOSS project for the management of a kennel and the recording of daily activities
usually carried out by volunteers.<br>
Main features:
- Creation of groups with specific permissions.
- Registration and management of users and assignment to qualifying groups.
- Setting the features of the structure: legal information, areas and boxes.
- Registration of the types of activities to be carried out and linked with a qualifying permission.
- Registration of animals with their characteristics: general, descriptive, health and management.
- Multicast notification system.
- Events registration.
- Research in events with different filters.

## 1. Installation (Debian based distributions)
Install python 3.X & pipenv: `apt install python3 pipenv`<br>
Change directory: `cd {insert_your_folder}`<br>
Clone repository: `git clone git@gitlab.com:0xfederico/balto.git`<br>
Change directory: `cd balto`<br>
Create virtualenv and install all dependencies: `pipenv install`<br>

## 2. Populate the database
Migrate: `python3 manage.py migrate`<br>
Create superuser: `python3 manage.py createsuperuser`<br>

## 3. Start the **development** server
Activate the virtualenv end spawn a shell inside: `pipenv shell`

Two execution options are supported:
- Run server on localhost: `python3 manage.py runserver`<br>
  :warning: Only you can access the website. :warning:<br>
  Now you can access the website at http://127.0.0.1:8000
- Run server inside your LAN: `python3 manage.py runserver 0.0.0.0:8000`<br>
  :warning: All devices in your own network can access the website, it is useful to see the website on smartphones. :warning:<br>
  Now you can access the website at http://{YOUR_LAN_IP_ADDRESS}:8000

## 4. Used technologies
- Python 3.9
- Django
- django-crispy-forms
- Pillow
- django-sslserver
- netifaces

## 5. License
**GNU AFFERO GENERAL PUBLIC LICENSE Version 3**.<br>
Please read the [`LICENSE`](/LICENSE) file.
