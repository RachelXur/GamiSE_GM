# GamiSE

## Contents of this file

 - Introduction
 - Requirements
 - Installation
 - Configuration
 - Link of Thesis
## Introduction

GamiSE is a gamified social engineering platform that merges modern gamification principles with social engineering training. Designed to be a motivating and enjoyable platform that enhances users' awareness and defense capabilities against social engineering (SE) attacks. Users can share SE-related experiences and information, fostering interaction through responses to other users' posts. GamiSE conducts phishing simulations with customized templates, allowing users to report SE attacks directly on the platform. As users engage in these activities, they earn points, achievements, badges, and rewards, providing positive reinforcement for their participation and performance in the training process.

There are three roles in GamiSE: Trainees, Admin, and IT department. The primary focus of SE attack simulations is on phishing attacks, while gamification elements center around points, badges, achievements, rewards, and leaderboards.

Trainees' functions include registration, logging in to GamiSE, changing profiles, resetting passwords, and checking SE-related information posted by other users or the IT department.

Admin functions encompass sending daily emails (containing SE-related news and tips on defending against SE attacks), launching phishing attacks, and adding gamification elements, which include establishing rules for points, badges, and achievements.

IT department functions involve checking trainees' reports (related to the phishing simulations launched by the admin) and submitting defending solutions for the phishing simulations.
## Requirements

- Front-end: HTML, CSS, jQuery, JavaScript
- Back-end: Python, Python Flask
- Database: PostgreSQL
- Could Server: Microsoft Azure Web APP Server
## Installation

- Set up the virtual environment.
- Navigate to the download folder within the virtual environment and install all the libraries listed in the requirements.txt file.
- Create the database.
- Configure the settings.
- Start the Flask application.
## Configuration

- 'SQLALCHEMY_DATABASE_URI' is for setting the database.
- 'SECRET_KEY' is the secure key for Flask.
- 'MAIL_USERNAME', 'MAIL_PASSWORD', 'MAIL_SERVER', 'MAIL_PORT' and 'MAIL_USE_SSL'. These email configurations are utilized for sending registration verification messages.
## Link of Thesis

- "Gamification Platform for Social Engineering Training and Awareness" (2021) (https://scholar.uwindsor.ca/etd/8775)
