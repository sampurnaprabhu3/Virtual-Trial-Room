Virtual Trial Room (VTR) Application
This repository hosts the code for the Virtual Trial Room (VTR) Application, a project designed to allow users to digitally try on clothing in real-time using computer vision and image processing techniques. The application aims to enhance the online shopping experience by bridging the gap between viewing an item and seeing how it fits.

About the Project
The VTR application works by detecting a user's body landmarks (like shoulders, waist, and hips) from a live video feed or a static image. Key components include:
Body Pose Estimation: Utilizes libraries like MediaPipe and OpenCV to accurately identify and track the coordinates of the user's body parts.
Clothing Overlay: Digital clothing assets (found in the assets/ folder) are scaled, warped, and correctly positioned over the user's detected body area, accounting for movement and perspective to create a realistic try-on effect.

Technology Stack
This project is built primarily using Python and relies on a few key libraries for its functionality.
Technology                     Role
Python                         Core programming language
OpenCV                         Handling video streams and image manipulation
MediaPipe                      Advanced body and pose estimation
Custom Environment (mp_env)    Isolated environment for specialized libraries

Getting Started:
Follow these steps to set up and run the Virtual Trial Room application on your local machine.

Prerequisites
Python 3.x
Virtual Environment: The project is configured to run inside a virtual environment (either venv or mp_env).

Installation and Setup:
Clone the Repository: Since your repository is already online, you would use this command to download it to any machine:
git clone https://github.com/sampurnaprabhu3/Virtual-Trial-Room.git
cd Virtual-Trial-Room

Install Dependencies: If you have a requirements.txt file (which should be uploaded in the next commit), you can install all necessary libraries:
pip install -r requirements.txt


Execution
Run the main Python file to start the application:


python virtual_trial_room.py
📂 Repository Structure
The core files you uploaded are:

Virtual-Trial-Room/
├── assets/                  # Contains all digital clothing images (PNGs)
│   └── clothes/
├── mp_env/                  
├── .gitignore               # Ensures large environment files are never pushed
└── virtual_trial_room.py    # Main application logic
