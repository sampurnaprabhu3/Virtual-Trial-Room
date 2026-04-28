# Virtual Trial Room (VTR)

> Try clothes on digitally — real-time clothing overlay using computer vision and body pose estimation.

---

## The Problem

Online shoppers can't tell how clothes will actually fit them. Return rates in fashion e-commerce are as high as 40% — largely because of fit uncertainty. VTR bridges that gap by letting users see how an item looks on their actual body, in real time, before buying.

---

## What it does

VTR uses a live webcam feed or static image to detect a user's body landmarks (shoulders, waist, hips) and overlays digital clothing assets onto them — scaled, warped, and repositioned as the user moves — creating a realistic virtual try-on experience.

---

## Key Features

- **Real-time body pose estimation** — detects and tracks body landmarks frame-by-frame using MediaPipe
- **Clothing overlay** — digital clothing assets are scaled and warped to fit the user's detected body proportions
- **Movement tracking** — overlay adjusts dynamically as the user moves
- **Modular clothing assets** — swap in any clothing PNG from the assets folder

---

## Tech Stack

| Technology | Role |
|---|---|
| Python | Core language |
| OpenCV | Video stream handling and image manipulation |
| MediaPipe | Body and pose estimation |
| Custom env (mp_env) | Isolated environment for specialized libraries |

---

## Getting Started

### Prerequisites
- Python 3.x
- Virtual environment (venv or mp_env)

### Installation

```bash
# Clone the repo
git clone https://github.com/sampurnaprabhu3/Virtual-Trial-Room.git
cd Virtual-Trial-Room

# Install dependencies
pip install -r requirements.txt

# Run the app
python virtual_trial_room.py
```

---

## Repository Structure

```
Virtual-Trial-Room/
├── assets/
│   └── clothes/        # Digital clothing PNGs
├── mp_env/             # Custom virtual environment
├── virtual_trial_room.py   # Main application logic
└── .gitignore
```

---

## My Role

Built as part of my undergraduate coursework at Vidyalankar Institute of Technology. Designed and developed the computer vision pipeline, clothing overlay logic, and pose estimation integration.

---

## Future Scope

- Web-based version (no install needed)
- Support for full outfits, accessories, and shoes
- Size recommendation based on body measurements
- Integration with live e-commerce product catalogues
