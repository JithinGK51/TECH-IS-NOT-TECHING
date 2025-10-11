# 🎪 DAKSHA CARNIVAL - Typing Challenge Game

A professional fullscreen typing challenge game built with Python and Tkinter, featuring an immersive carnival-themed interface with global mouse controls and real-time timing.

## 🎮 Game Overview

**DAKSHA CARNIVAL** is an interactive typing challenge where players must type the phrase "Daksha Carnival" using only mouse clicks. The game features a beautiful carnival-themed interface with glow effects, animations, and a professional timer system.

## ✨ Features

### 🎯 Core Gameplay
- **Global Mouse Controls**: Left click anywhere to change letters, right click to type
- **Letter Cycling**: Cycle through a-z → space → A-Z → repeat
- **Target Phrase**: Type "Daksha Carnival" to complete the challenge
- **Real-time Timer**: Professional timer display in top-left corner
- **5-Second Countdown**: Auto-resets to 'a' if no action taken

### 🎨 Visual Design
- **Fullscreen Mode**: Immersive gaming experience
- **Carnival Theme**: Dark background with cyan accent colors (#00FFD6)
- **Glow Animations**: Dynamic color effects on UI elements
- **Professional Typography**: Orbitron and Consolas fonts
- **Hidden Cursor**: During gameplay for immersive experience

### 🏆 Game Management
- **Team Registration**: Enter team name to start
- **Leaderboard System**: Automatic time tracking and ranking
- **Celebration Effects**: Flying emojis and fullscreen congratulations
- **Persistent Data**: JSON-based leaderboard storage

## 🚀 Installation & Setup

### Prerequisites
- Python 3.7 or higher
- Tkinter (usually included with Python)
- Windows OS (for optimal experience)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/JithinGK51/TECH-IS-NOT-TECHING.git
   cd TECH-IS-NOT-TECHING
   ```

2. **Run the game**
   ```bash
   python CARNIVAL.PY
   ```

## 🎮 How to Play

### Game Controls
- **Left Click Anywhere** → Change Letter (cycle through a-z, space, A-Z)
- **Right Click Anywhere** → Type Letter (add selected letter to text)
- **Backspace Key** → Remove last character
- **ESC Key** → Exit game

### Game Flow
1. **Home Screen**: Enter your team name and click "START GAME"
2. **Game Screen**: Use mouse clicks to type "Daksha Carnival"
3. **Completion**: Enjoy the celebration and see your completion time
4. **Leaderboard**: Your time is automatically saved for ranking

## 📁 Project Structure

```
TECH-IS-NOT-TECHING/
├── CARNIVAL.PY          # Main game file
├── leaderboard.json     # Leaderboard data storage
├── README.md           # Project documentation
└── requirements.txt    # Python dependencies
```

## 🛠️ Technical Details

### Technologies Used
- **Python 3.13**: Core programming language
- **Tkinter**: GUI framework for the game interface
- **JSON**: Data storage for leaderboard
- **Time Module**: Timer functionality

### Key Components
- **Multi-Screen System**: Home, Game, and Celebration screens
- **Global Event Handling**: Mouse click detection across entire screen
- **Animation System**: Glow effects and flying emojis
- **Data Persistence**: JSON-based leaderboard storage
- **Timer System**: Real-time millisecond precision timing

## 🎯 Game Configuration

### Customizable Settings
- **Target Words**: Modify `TARGET_WORDS` list in `CARNIVAL.PY`
- **Letter Order**: Change `ALPHABETS` sequence
- **Timer Display**: Adjust timer position and styling
- **Color Scheme**: Modify color constants throughout the code

### Example Configuration
```python
TARGET_WORDS = ["Daksha Carnival"]  # Target phrase
ALPHABETS = [chr(i) for i in range(97, 123)] + [" "] + [chr(i) for i in range(65, 91)]
```

## 🏆 Leaderboard System

The game automatically tracks and ranks players based on completion time:

```json
[
  {
    "slno": 1,
    "team_name": "Team Alpha",
    "time": 45.23
  }
]
```

- **Automatic Sorting**: Fastest times appear first
- **Persistent Storage**: Data saved to `leaderboard.json`
- **Team-Based**: Uses team names instead of individual players

## 🎨 Customization Guide

### Changing Target Phrase
```python
TARGET_WORDS = ["Your Custom Phrase"]
```

### Modifying Letter Sequence
```python
ALPHABETS = [chr(i) for i in range(97, 123)] + [" "] + [chr(i) for i in range(65, 91)]
```

### Adjusting Colors
```python
# Main background
bg_color = "#0d1117"

# Accent color
accent_color = "#00FFD6"

# Button colors
button_bg = "#161B22"
```

## 🐛 Troubleshooting

### Common Issues

1. **Game won't start**
   - Ensure Python 3.7+ is installed
   - Check that Tkinter is available
   - Run from command line to see error messages

2. **Mouse clicks not working**
   - Ensure game is in fullscreen mode
   - Check that no other applications are blocking input
   - Try clicking directly on buttons first

3. **Timer not displaying**
   - Verify the game screen is active
   - Check that the timer label is properly positioned

## 🤝 Contributing

We welcome contributions to improve the DAKSHA CARNIVAL game! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add amazing feature'`
4. **Push to the branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Development Guidelines
- Follow Python PEP 8 style guidelines
- Add comments for complex functionality
- Test changes thoroughly before submitting
- Update documentation for new features

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Team

- **Developer**: Jithin GK
- **Project**: TECH IS NOT TECHING
- **Event**: DAKSHA CARNIVAL

## 🎪 About DAKSHA CARNIVAL

DAKSHA CARNIVAL is a tech event featuring innovative challenges and competitions. This typing challenge game was created to provide an engaging and professional gaming experience for participants.

## 📞 Support

For support, questions, or suggestions:
- **GitHub Issues**: [Create an issue](https://github.com/JithinGK51/TECH-IS-NOT-TECHING/issues)
- **Email**: Contact the development team
- **Event Support**: Reach out to DAKSHA CARNIVAL organizers

---

**Made with ❤️ for DAKSHA CARNIVAL - TECH IS NOT TECHING**

*Experience the future of interactive gaming!* 🚀
