# Autokinesis Tracker Eye Tracking Module (aktrack-goggle)

This repository contains the eye tracking module for the Autokinesis Tracker system, a research tool for tracking eye movements and visual perception.

![demo_5min_data](https://github.com/bingogome/aktrack-slicer/blob/main/demo_5min_data.gif)

## Overview

The Autokinesis Tracker eye tracking module (aktrack-goggle) handles communication with eye tracking hardware and provides visual stimuli for calibration and experiments. It works in conjunction with the [AkTrack UI](https://github.com/bingogome/aktrack-slicer/tree/main) to perform experiments measuring subjects' eye movements.

## Features

- Communication with eye tracking hardware via a .NET library
- Visual stimulus display for calibration and testing
- Network communication with the main AkTrack UI application
- Recording and timestamping of eye movement data
- Support for different experimental protocols (VPB-hfixed, VPB-hfree)
- Fullscreen display capabilities for visual stimuli

## Requirements

- Windows OS
- Python with tkinter library
- Eye tracker hardware and associated .NET DLL (referenced in the code as "EyeTrackerRemoteClient.dll")
- [AkTrack UI](https://github.com/bingogome/aktrack-slicer/tree/main) for experiment control

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/bingogome/aktrack-goggle.git
   ```

2. Ensure the eye tracker hardware is properly connected and the DLL is available at the specified path:
   ```
   C:\EyeTracker Debug 2018-22-08\EyeTrackerRemoteClient.dll
   ```

3. Ensure the eye tracker server is running at the specified IP address (10.17.101.204:9000).

## Usage

Run the application by executing:
```
python application.py
```

### Key Bindings

The application responds to the following key presses:

- `q` - Quit the application
- `c` - Toggle goggle calibration
- `a` - Toggle fullscreen mode
- `d` - Initialize a visual stimulus (dot) at the center
- `s` - Center the visual stimulus
- Arrow keys - Move the visual stimulus in respective directions
- `Escape` - Stop visual stimulus

## Components

- **VOG.py** - Interface with the eye tracking hardware
- **connections.py** - Network communication with the AkTrack UI
- **screendot.py** - Visual stimulus display 
- **application.py** - Main application integrating all components

## Network Communication

The application communicates with the AkTrack UI through UDP:
- Receiving commands on port 8297
- Sending acknowledgments on port 8293

## Experiment Protocols

The system supports different experimental protocols:
1. VPB-hfixed - Visual pursuit with head fixed
2. VPB-hfree - Visual pursuit with head free movement

Each protocol includes start and stop recording commands with appropriate event marking.

## Calibration

To perform eye tracker calibration:
1. Press `c` to start calibration mode
2. Use arrow keys to position the red dot at calibration positions
3. Press `Escape` to stop the current stimulus
4. Press `c` again to stop calibration recording

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Cite

@article{liu2024autokinesis,
  title={Autokinesis Reveals a Threshold for Perception of Visual Motion},
  author={Liu, Yihao and Tian, Jing and Martin-Gomez, Alejandro and Arshad, Qadeer and Armand, Mehran and Kheradmand, Amir},
  journal={Neuroscience},
  volume={543},
  pages={101--107},
  year={2024},
  publisher={Elsevier}
}

## Project Links

- [AkTrack UI](https://github.com/bingogome/aktrack-slicer/tree/main) - Main user interface for the Autokinesis Tracker system
