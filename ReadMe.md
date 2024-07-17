# TouchTact Experiment Generation GUI

## Table of Contents
- [Overview](#overview)
- [Quick Start Guide](#quick-start-guide)
- [Requirements](#requirements)
- [Installation](#installation)
- [Visual Navigation Guide](#visual-navigation-guide)
- [Detailed Usage Guide](#detailed-usage-guide)
  - [1. Settings Configuration](#1-settings-configuration)
  - [2. Case Creation](#2-case-creation)
  - [3. Experiment Management](#3-experiment-management)
  - [4. Latency Management](#4-latency-management)
  - [5. Deploying Your Experiment](#5-deploying-your-experiment)
- [For Participants](#for-participants)
- [Contributing](#contributing)
- [File Structure](#file-structure)
- [File Attributions](#file-attributions)
- [License](#license)
- [Contact](#contact)

## Overview

TouchTact is a system for conducting touch interaction and haptic feedback experiments. This GUI application allows researchers to generate and manage experiments without coding. Experiments created here can be accessed by participants through the TouchTact iOS app.

## Quick Start Guide

1. [Install the application](#installation)
2. Run the application: `python main.py`
3. Configure settings in the [Settings tab](#1-settings-configuration)
4. Create cases in the [Case Creation window](#2-case-creation)
5. Combine cases into an experiment in the [Experiment tab](#3-experiment-management)
6. [Generate and deploy your experiment](#5-deploying-your-experiment)

## Requirements

- Python 3.x
- Tkinter (usually pre-installed with Python)
- NumPy
- SoundFile
- JsonSchema

## Installation

1. Fork this repository on GitHub
2. Clone your fork:
   ```
   git clone https://github.com/your-username/TouchTactServer.git
   ```
3. Navigate to the project directory:
   ```
   cd TouchTactServer
   ```
4. Install required packages:
   ```
   pip install -r requirements.txt
   ```


## Visual Navigation Guide

Here's a visual guide to help you navigate the main features of the TouchTact Experiment Generation GUI:

### 1. Main Application Window

![Main Application Window](/Files/Image/setting%20ui.png)

The main window contains two tabs:
- Settings: Configure global settings, manage user agreements, and access other features.
- Experiment: Create and manage experiments.

Key features in the Settings tab:
- Server/GitHub configuration
- User agreement management
- Survey link settings
- Access to Latency Management

### 2. Experiment Creation

![Experiment Creation](/Files/Image/experiment%20ui.png)

In the Experiment tab, you can:
- Set an Experiment ID
- Add existing cases to your experiment
- Create new cases
- Set a survey URL for the experiment

### 3. Case Creation

![Case Creation](/Files/Image/case%20ui%20upper.png)

The Case Creation window allows you to configure:
- Case ID
- Interaction type
- Custom text arrays
- Order arrays
- Audio and haptic file associations
- Timer and scoreboard settings
- Tutorial text

### 4. Latency Management

![Latency Management](/Files/Image/latency%20ui.png)

The Latency Management window enables you to:
- Set a global latency value
- Select audio and haptic files for latency adjustment
- Convert files with the specified latency

## Detailed Usage Guide

### 1. Settings Configuration

In the Settings tab:

- Set your GitHub username and repository name
- Manage user agreements
- Configure survey links
- Access the [Latency Management](#4-latency-management) tool

### 2. Case Creation

Click "Create New Case" in the Experiment tab to open the Case Creation window. Here you can:

- Set a Case ID
- Choose interaction type (tap, swipe)
- Configure custom text arrays
- Set order arrays
- Associate audio and haptic files
- Set up timer and scoreboard
- Write tutorial text

Tips:
- Use descriptive Case IDs
- Test different interaction types to suit your experiment
- Carefully consider your order and custom text arrays

### 3. Experiment Management

In the Experiment tab:

- Set an Experiment ID
- Add created cases to your experiment
- Arrange the order of cases
- Set a survey URL for post-experiment feedback

### 4. Latency Management

Access via the "Manage Latency" button in the Settings tab:

- Set a global latency value (in seconds)
- Select audio (.wav) and haptic (.ahap) files
- Click "Convert" to create latency-adjusted versions

Use this feature to study the effects of delayed feedback in your experiments.

### 5. Deploying Your Experiment

After setting up your experiment:

1. Click "Generate" in the Experiment tab
2. Commit and push changes to your GitHub repository:
   ```
   git add .
   git commit -m "Added new experiment: [Experiment ID]"
   git push origin main
   ```
3. The experiment is now accessible via the TouchTact iOS app

## For Participants

Participants need the following to access experiments via the TouchTact iOS app:

- Researcher's GitHub username
- Repository name (typically TouchTactServer)
- Experiment ID
- Assigned Participant ID


## Contributing

To extend TouchTact's functionality:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/NewFeature`)
3. Commit changes (`git commit -m 'Add NewFeature'`)
4. Push to the branch (`git push origin feature/NewFeature`)
5. Open a Pull Request

## File Structure

```
TouchTactServer/
│
├── Files/
│   ├── Audio/
│   │   ├── Original/
│   │   └── Latency/
│   ├── Haptic/
│   │   ├── Original/
│   │   └── Latency/
│   ├── Image/
│   ├── Case/
│   └── Experiment/
│
├── Schema/
│   ├── case.json
│   └── experiment.json
│
├── .gui/
│   ├── setting/
│   ├── case/
│   └── experiment/
│
├── main.py
├── settings_ui.py
├── case_ui.py
├── experiment_ui.py
├── latency_ui.py
├── custom_widget.py
├── default_configs.py
├── requirements.txt
└── README.md
```

## File Attributions

### Audio Files

Location: `Files/Audio/Original/`

1. Numerical Voice Prompts (1.wav to 9.wav) and DTMF Tone (Dtmf-0.wav)
   - Source: Voxeo Evolution
   - URL: https://evolution.voxeo.com/library/audio/prompts/
   - License: LGPL (GNU Lesser General Public License)

2. Alert Beep (33786__jobro__4-beep-c.wav)
   - Author: jobro
   - Source: Freesound
   - URL: https://freesound.org/people/jobro/sounds/33786/
   - License: Attribution 3.0 Unported (CC BY 3.0)
   - Attribution: "4 beep c.wav" by jobro (https://freesound.org/s/33786/)

### Haptic Files

Location: `Files/Haptic/Original/`

1. Dtmf-0.ahap
   - Description: Haptic pattern based on DTMF tone
   - Source: Custom-created based on Dtmf-0.wav

2. 33786__jobro__4-beep-c.ahap
   - Description: Haptic pattern based on alert beep
   - Source: Custom-created based on 33786__jobro__4-beep-c.wav

Note: All AHAP (Apple Haptic and Audio Pattern) files were created specifically for this project, based on the waveforms of their corresponding audio files.

## License and Citation

### License
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](http://creativecommons.org/licenses/by/4.0/)

TouchTact Experiment Generation GUI © 2023 by University of Southern California HaRVI Research Lab is licensed under CC BY 4.0. 

This license requires that reusers give credit to the creator. It allows reusers to distribute, remix, adapt, and build upon the material in any medium or format, even for commercial purposes.

To view a copy of this license, visit http://creativecommons.org/licenses/by/4.0/

### Attribution and Citation

If you use TouchTact in your research or project, please provide attribution by citing our paper and linking to our project:

```
Lee, S. H., Kollannur, & Culbertson H. (2025). 
TouchTact: A Performance-Centric Audio-Haptic Toolkit for Task-Oriented Mobile Interactions. [Paper DOI URL]

Project URL: [Project's GitHub URL]
```
## Contributors and Contact
This project was developed by the University of Southern California HaRVI Research Lab.

### Core Team
- Seung Heon Lee - Lead Engineer
- Sandeep Kollannur - Project Manager (sandeep.kollannur@usc.edu)
- Dr. Heather Culbertson - Research Advisor

### Contact
For questions or support regarding this project, please contact:
Sandeep Kollannur at sandeep.kollannur@usc.edu (University of Southern California, HaRVI Lab)