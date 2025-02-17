# Project: Catch the Ball

Students: **Bùi Quốc Vĩnh Khang (230312)**, **Võ Kế Hoài (230309)**, **Trần Vũ Anh Quân (230329)**

This is a catch-the-ball project with a lot of features, built using pygame.

## Requirements

- Python 3.x

## Features

- **Basket Movement:** Control the basket using arrow keys or optional face tracking.
- **Power-ups:** Various effects like magnetic catch, speed boost, and decreased stun time.
- **Boss Battles:** Defeat bosses and earn upgrade cards.
- **Dynamic Backgrounds:** Backgrounds change as you progress.
- **Ranking System:** Earn ranks from D to SSS based on your performance.
- **Sound Effects & Music:** Background music and sound effects enhance gameplay.

## Installation

1. **Clone the repository**:
   ```sh
   git clone https://github.com/kgbqv/pygame-ball.git
   cd pygame-ball
   ```

2. **Create and activate a virtual environment**:
   - On Windows:
     ```sh
     python -m venv venv
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```sh
     python3 -m venv venv
     source venv/bin/activate
     ```

Note: If you do not want face tracking, you can go into `main.py` and set `minimal = True` in the first line. And then you can omit opencv-python and dlib from the required libraries.

3. **Install the required libraries**:
   ```sh
   pip install pygame pillow numpy opencv-python dlib  
   ```

## Usage

**Run the main script**:
   ```sh
   python main.py
   ```

## Controls

- **Arrow Keys:** Move the basket and selector left and right.
- **F:** Toggle face tracking (if available).
- **Space:** Shoot bullets (during boss fights).
- **M:** Return to the main menu.
- **B:** Go back (in menus).
- **Up/Down Arrow Keys:** Adjust volume (only in the options menu). And special movement in space.
- **Q:** Change webcam (only in the options menu, if face tracking is enabled).

## File Structure

📂 `assets/`      

📜 `main.py`      

📜 `test_render.py` 

📜 `head_pose.py`  

📜 `README.md` 