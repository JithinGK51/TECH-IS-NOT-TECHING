import tkinter as tk
from tkinter import messagebox, ttk
import random
import json
import os
import time
import math

# ----------------------------------------
# CONFIGURATION
# ----------------------------------------
TARGET_WORDS = ["Daksha Carnival"]
ALPHABETS = [chr(i) for i in range(97, 123)] + [" "] + [chr(i) for i in range(65, 91)]  # a-z, space, A-Z
LEADERBOARD_FILE = "leaderboard.json"

# Global variables
current_index = 0
typed_text = ""
single_click_after_id = None
glow_direction = 1
glow_intensity = 100
celebrating = False
countdown_timer = None
countdown_active = False

# Multiple words tracking
current_word_index = 0
words_completed = 0

# User data
current_user = {"team_name": ""}
game_start_time = 0
game_timer_id = None
game_timer_running = False

# Screen management
current_screen = "home"  # home, game

# Analog clock variables
analog_clock_canvas = None
clock_center_x = 0
clock_center_y = 0
clock_radius = 0
hour_hand = None
minute_hand = None
second_hand = None
clock_animation_id = None

# ----------------------------------------
# LEADERBOARD FUNCTIONS
# ----------------------------------------
def load_leaderboard():
    """Load leaderboard from JSON file"""
    try:
        if os.path.exists(LEADERBOARD_FILE):
            with open(LEADERBOARD_FILE, 'r') as f:
                return json.load(f)
    except:
        pass
    return []

def save_leaderboard(leaderboard_data):
    """Save leaderboard to JSON file"""
    try:
        with open(LEADERBOARD_FILE, 'w') as f:
            json.dump(leaderboard_data, f, indent=2)
    except:
        pass

def add_to_leaderboard(team_name, time_taken):
    """Add new entry to leaderboard"""
    leaderboard = load_leaderboard()
    
    # Add new entry
    new_entry = {
        "slno": len(leaderboard) + 1,
        "team_name": team_name,
        "time": round(time_taken, 2)
    }
    leaderboard.append(new_entry)
    
    # Sort by time (fastest first)
    leaderboard.sort(key=lambda x: x["time"])
    
    # Update serial numbers
    for i, entry in enumerate(leaderboard):
        entry["slno"] = i + 1
    
    save_leaderboard(leaderboard)
    return leaderboard

# ----------------------------------------
# TIMER FUNCTIONS
# ----------------------------------------
def start_game_timer():
    """Start the game timer"""
    global game_start_time, game_timer_id, game_timer_running
    game_start_time = time.time()
    game_timer_running = True
    update_game_timer()

def stop_game_timer():
    """Stop the game timer and return elapsed time"""
    global game_timer_running
    if game_timer_running:
        game_timer_running = False
        if game_timer_id:
            root.after_cancel(game_timer_id)
        # Stop analog clock animation
        stop_analog_clock()
        return time.time() - game_start_time
    return 0

def update_game_timer():
    """Update the game timer display"""
    global game_timer_id
    if game_timer_running:
        elapsed = time.time() - game_start_time
        minutes = int(elapsed // 60)
        seconds = int(elapsed % 60)
        milliseconds = int((elapsed % 1) * 100)
        
        timer_text = f"⏱️ {minutes:02d}:{seconds:02d}.{milliseconds:02d}"
        timer_label.config(text=timer_text)
        
        # Update digital timer on the right side
        digital_timer_text = f"{minutes:02d}:{seconds:02d}.{milliseconds:02d}"
        digital_timer_label.config(text=digital_timer_text)
        
        game_timer_id = root.after(50, update_game_timer)  # Update every 50ms for smooth display
        # Update analog clock
        update_analog_clock()

# ----------------------------------------
# ANALOG CLOCK FUNCTIONS
# ----------------------------------------
def create_analog_clock():
    """Create the analog clock canvas and design"""
    global analog_clock_canvas, clock_center_x, clock_center_y, clock_radius
    
    # Create canvas for analog clock
    analog_clock_canvas = tk.Canvas(
        game_frame,
        width=200,
        height=200,
        bg="#1a1a2e",
        highlightthickness=0,
        relief="sunken",
        bd=3
    )
    analog_clock_canvas.place(x=20, y=20)  # Left side position
    
    # Clock dimensions
    clock_center_x = 100
    clock_center_y = 100
    clock_radius = 85
    
    # Draw clock face
    draw_clock_face()
    
    # Initialize clock hands
    initialize_clock_hands()

def draw_clock_face():
    """Draw the clock face with numbers and hour marks"""
    global analog_clock_canvas, clock_center_x, clock_center_y, clock_radius
    
    # Outer circle
    analog_clock_canvas.create_oval(
        clock_center_x - clock_radius,
        clock_center_y - clock_radius,
        clock_center_x + clock_radius,
        clock_center_y + clock_radius,
        outline="#00FFD6",
        width=3,
        fill="#0d1117"
    )
    
    # Inner circle
    analog_clock_canvas.create_oval(
        clock_center_x - clock_radius + 10,
        clock_center_y - clock_radius + 10,
        clock_center_x + clock_radius - 10,
        clock_center_y + clock_radius - 10,
        outline="#00FFD6",
        width=1,
        fill="#1a1a2e"
    )
    
    # Hour marks (12 positions)
    for i in range(12):
        angle = math.radians(i * 30 - 90)  # Start from top (12 o'clock)
        
        # Calculate positions for hour marks
        inner_radius = clock_radius - 15
        outer_radius = clock_radius - 5
        
        x1 = clock_center_x + inner_radius * math.cos(angle)
        y1 = clock_center_y + inner_radius * math.sin(angle)
        x2 = clock_center_x + outer_radius * math.cos(angle)
        y2 = clock_center_y + outer_radius * math.sin(angle)
        
        # Draw hour marks
        analog_clock_canvas.create_line(
            x1, y1, x2, y2,
            fill="#00FFD6",
            width=3
        )
        
        # Add hour numbers (12, 1, 2, 3, 6, 9)
        if i in [0, 3, 6, 9]:  # 12, 3, 6, 9 o'clock
            number_radius = clock_radius - 25
            num_x = clock_center_x + number_radius * math.cos(angle)
            num_y = clock_center_y + number_radius * math.sin(angle)
            
            hour_text = str(12 if i == 0 else i)
            analog_clock_canvas.create_text(
                num_x, num_y,
                text=hour_text,
                fill="#00FFD6",
                font=("Orbitron", 12, "bold")
            )
    
    # Center dot
    analog_clock_canvas.create_oval(
        clock_center_x - 5,
        clock_center_y - 5,
        clock_center_x + 5,
        clock_center_y + 5,
        fill="#00FFD6",
        outline="#00FFD6"
    )

def initialize_clock_hands():
    """Initialize the clock hands"""
    global hour_hand, minute_hand, second_hand
    
    # Create initial clock hands (pointing to 12:00:00)
    hour_hand = analog_clock_canvas.create_line(
        clock_center_x, clock_center_y,
        clock_center_x, clock_center_y - 40,
        fill="#FF6B6B",
        width=4,
        capstyle="round"
    )
    
    minute_hand = analog_clock_canvas.create_line(
        clock_center_x, clock_center_y,
        clock_center_x, clock_center_y - 60,
        fill="#4ECDC4",
        width=3,
        capstyle="round"
    )
    
    second_hand = analog_clock_canvas.create_line(
        clock_center_x, clock_center_y,
        clock_center_x, clock_center_y - 70,
        fill="#FFE66D",
        width=2,
        capstyle="round"
    )

def update_analog_clock():
    """Update the analog clock hands based on elapsed time"""
    global clock_animation_id
    
    if not game_timer_running or not analog_clock_canvas:
        return
    
    # Calculate elapsed time
    elapsed = time.time() - game_start_time
    
    # Convert to hours, minutes, seconds
    total_seconds = int(elapsed)
    hours = (total_seconds // 3600) % 12  # 12-hour format
    minutes = (total_seconds // 60) % 60
    seconds = total_seconds % 60
    
    # Calculate angles (in radians, starting from top)
    hour_angle = math.radians((hours * 30 + minutes * 0.5) - 90)
    minute_angle = math.radians((minutes * 6) - 90)
    second_angle = math.radians((seconds * 6) - 90)
    
    # Update hour hand
    hour_length = 40
    hour_x = clock_center_x + hour_length * math.cos(hour_angle)
    hour_y = clock_center_y + hour_length * math.sin(hour_angle)
    analog_clock_canvas.coords(hour_hand, clock_center_x, clock_center_y, hour_x, hour_y)
    
    # Update minute hand
    minute_length = 60
    minute_x = clock_center_x + minute_length * math.cos(minute_angle)
    minute_y = clock_center_y + minute_length * math.sin(minute_angle)
    analog_clock_canvas.coords(minute_hand, clock_center_x, clock_center_y, minute_x, minute_y)
    
    # Update second hand
    second_length = 70
    second_x = clock_center_x + second_length * math.cos(second_angle)
    second_y = clock_center_y + second_length * math.sin(second_angle)
    analog_clock_canvas.coords(second_hand, clock_center_x, clock_center_y, second_x, second_y)
    
    # Schedule next update
    clock_animation_id = root.after(100, update_analog_clock)

def stop_analog_clock():
    """Stop the analog clock animation"""
    global clock_animation_id
    if clock_animation_id:
        root.after_cancel(clock_animation_id)
        clock_animation_id = None

# ----------------------------------------
# GAME FUNCTIONS
# ----------------------------------------
def on_change_letter_click(event):
    """Handle left mouse click on CHANGE LETTER button"""
    change_letter()

def change_letter():
    """Change letter - cycles through a-z, space, A-Z"""
    global current_index, countdown_timer, countdown_active
    if celebrating:
        return
    
    # Cancel any existing countdown
    if countdown_timer:
        root.after_cancel(countdown_timer)
        countdown_active = False
    
    # Show current letter first, then increment for next click
    current_letter = ALPHABETS[current_index]
    current_index = (current_index + 1) % len(ALPHABETS)
    
    # Show "5" countdown only (no letter display)
    change_button.config(text="CHANGE LETTER\n5")
    root.update()  # Force immediate UI update
    
    # Start 5-second countdown
    countdown_active = True
    start_countdown()

def start_countdown():
    """Start 5-second countdown timer"""
    global countdown_timer, countdown_active
    countdown_seconds = 4  # Start from 4 since we already showed 5
    
    def countdown():
        nonlocal countdown_seconds
        if countdown_seconds > 0 and countdown_active:
            # Show countdown only (no letter display)
            change_button.config(text=f"CHANGE LETTER\n{countdown_seconds}")
            root.update()  # Force immediate UI update
            countdown_seconds -= 1
            countdown_timer = root.after(1000, countdown)
        elif countdown_active:  # countdown_seconds == 0
            # Reset to 'a' (first lowercase letter)
            current_index = 0
            change_button.config(text="CHANGE LETTER")
            countdown_active = False
            countdown_timer = None
    
    # Start countdown after 1 second (since we already showed 5)
    countdown_timer = root.after(1000, countdown)

def type_letter():
    """Type the currently selected letter"""
    global typed_text, current_index, countdown_timer, countdown_active
    if celebrating:
        return
    
    # Cancel countdown if active
    if countdown_timer:
        root.after_cancel(countdown_timer)
        countdown_active = False
        countdown_timer = None
    
    # Use the letter that was displayed (current_index was already incremented)
    letter = ALPHABETS[(current_index - 1) % len(ALPHABETS)]
    typed_text += letter
    text_display.config(text=typed_text)
    check_word()
    # reset selected letter to 'a'
    current_index = 0
    change_button.config(text="CHANGE LETTER")

def backspace():
    """Backspace"""
    global typed_text
    if celebrating:
        return
    if typed_text:
        typed_text = typed_text[:-1]
        text_display.config(text=typed_text)

def block_keys(event):
    """Block all keys except Backspace"""
    global typed_text
    if event.keysym == "BackSpace" and not celebrating:
        if typed_text:
            typed_text = typed_text[:-1]
            text_display.config(text=typed_text)
        return "break"
    return "break"

# ----------------------------------------
# CELEBRATION ANIMATION
# ----------------------------------------
celebration_emojis = ["🎉", "✨", "🎊", "💥", "💫", "🔥", "🌟", "🎆", "🎇", "🚀"]

def celebrate():
    """Show flying emojis and congratulations popup"""
    global celebrating
    celebrating = True
    
    # Stop timer and get completion time
    completion_time = stop_game_timer()
    
    text_display.config(text="🎉 DAKSHA CARNIVAL 🎉", fg="#00FFD6")
    
    # Create flying emojis
    for _ in range(25):
        create_flying_emoji()
    
    # Show congratulations popup with time
    show_congratulations_popup(completion_time)
    
    root.after(4000, end_celebration)

def show_congratulations_popup(completion_time):
    """Create animated congratulations popup with leaderboard button"""
    # Create popup window
    popup = tk.Toplevel(root)
    popup.title("🎉 Congratulations! 🎉")
    popup.configure(bg="#0d1117")
    popup.attributes("-topmost", True)
    popup.attributes('-fullscreen', True)
    # Show mouse cursor on popup window
    popup.config(cursor="")
    
    # Center the popup
    popup.transient(root)
    popup.grab_set()
    
    # Main congratulations frame
    congrats_frame = tk.Frame(popup, bg="#00FFD6", bd=5, relief="raised")
    congrats_frame.pack(expand=True, fill="both", padx=100, pady=100)
    
    # Time display
    minutes = int(completion_time // 60)
    seconds = int(completion_time % 60)
    milliseconds = int((completion_time % 1) * 100)
    time_str = f"{minutes:02d}:{seconds:02d}.{milliseconds:02d}"
    
    # Get team name
    team_name = current_user.get("team_name", "Unknown Team")
    
    # Congratulations text
    congrats_label = tk.Label(
        congrats_frame,
        text=f"DAKSHA CARNIVAL ROUND 5\n\n🎊 CONGRATULATIONS! 🎊\n\n👥 TEAM: {team_name}\n\n✨ YOU DID IT! ✨\n\n🎯 ALL WORDS COMPLETED! 🎯\n\n⏱️ TIME: {time_str}\n\n🏆 BEST DECISION EVER! 🏆\n\n🌟 AMAZING WORK! 🌟",
        font=("Orbitron", 20, "bold"),
        fg="#0d1117",
        bg="#00FFD6",
        justify="center"
    )
    congrats_label.pack(expand=True, fill="both", padx=30, pady=20)
    
    # Play again button (centered)
    play_again_btn = tk.Button(
        congrats_frame,
        text="🎮 PLAY AGAIN 🎮",
        font=("Consolas", 14, "bold"),
        fg="#00FFD6",
        bg="#0d1117",
        activebackground="#21262D",
        activeforeground="#00FFD6",
        relief="raised",
        bd=3,
        command=lambda: [popup.destroy(), end_celebration()]
    )
    play_again_btn.pack(pady=20)
    
    # Popup stays open until user manually closes or clicks a button

def create_flying_emoji():
    """Create a flying emoji randomly placed"""
    emoji = random.choice(celebration_emojis)
    label = tk.Label(
        root,
        text=emoji,
        font=("Segoe UI Emoji", random.randint(16, 32)),
        bg="#0d1117",
        fg="#00FFD6"
    )
    x = random.randint(0, 900)
    y = random.randint(400, 650)
    label.place(x=x, y=y)
    animate_emoji(label)

def animate_emoji(label):
    """Move emoji upward and fade"""
    def move():
        try:
            x, y = label.winfo_x(), label.winfo_y()
            if y < -30:
                label.destroy()
                return
            label.place(x=x + random.randint(-2, 2), y=y - random.randint(5, 10))
            root.after(50, move)
        except tk.TclError:
            pass
    move()

def end_celebration():
    """Reset everything and save to leaderboard"""
    global typed_text, current_index, celebrating, countdown_timer, countdown_active
    global current_word_index, words_completed
    
    # Save to leaderboard
    if current_user["team_name"]:
        completion_time = time.time() - game_start_time
        add_to_leaderboard(current_user["team_name"], completion_time)
    
    celebrating = False
    typed_text = ""
    current_index = 0
    current_word_index = 0
    words_completed = 0
    
    # Cancel any active countdown
    if countdown_timer:
        root.after_cancel(countdown_timer)
        countdown_active = False
        countdown_timer = None
    
    text_display.config(text="", fg="#00FFD6")
    change_button.config(text="CHANGE LETTER")
    
    # Return to home screen
    show_home_screen()

def check_word():
    """Check if typed word is correct"""
    global current_word_index, words_completed, typed_text
    
    if current_word_index < len(TARGET_WORDS):
        current_target = TARGET_WORDS[current_word_index]
        
        if typed_text.strip() == current_target:
            # Word completed!
            words_completed += 1
            current_word_index += 1
            
            # Show word completion feedback
            text_display.config(text=f"✅ {current_target} COMPLETED! ✅", fg="#00FF00")
            root.update()
            
            # Check if all words are completed
            if current_word_index >= len(TARGET_WORDS):
                # All words completed!
                root.after(1000, celebrate)  # Show celebration after 1 second
            else:
                # Move to next word
                typed_text = ""
                update_word_progress()
                next_word = TARGET_WORDS[current_word_index]
                text_display.config(text=f"Next: {next_word}", fg="#00FFD6")
                root.after(1500, lambda: text_display.config(text="", fg="#00FFD6"))

# ----------------------------------------
# SCREEN NAVIGATION
# ----------------------------------------
def hide_all_screens():
    """Hide all screen frames"""
    if 'home_frame' in globals():
        home_frame.pack_forget()
    if 'game_frame' in globals():
        game_frame.pack_forget()

def show_home_screen():
    """Show home screen"""
    global current_screen
    current_screen = "home"
    hide_all_screens()
    home_frame.pack(expand=True, fill="both")
    # Show mouse cursor on home screen
    root.config(cursor="")

def show_game_screen():
    """Show game screen and start timer"""
    global current_screen, current_word_index
    current_screen = "game"
    hide_all_screens()
    game_frame.pack(expand=True, fill="both")
    # Hide mouse cursor during gameplay for immersive experience
    root.config(cursor="none")
    # Reset word progress
    current_word_index = 0
    update_word_progress()
    
    # Create analog clock on the left side
    create_analog_clock()
    
    # Position digital timer on the right side dynamically
    screen_width = root.winfo_screenwidth()
    digital_timer_x = screen_width - 200  # 200px from right edge
    digital_timer_label.place(x=digital_timer_x, y=20)
    
    start_game_timer()

def update_word_progress():
    """Update the word progress display"""
    if current_word_index < len(TARGET_WORDS):
        current_word = TARGET_WORDS[current_word_index]
        progress_text = f"Word {current_word_index + 1} of {len(TARGET_WORDS)}: {current_word}"
        word_progress_label.config(text=progress_text)


# ----------------------------------------
# HOME SCREEN FUNCTIONS
# ----------------------------------------
def start_game():
    """Start the game with user validation"""
    team_name = team_name_entry.get().strip()
    
    if not team_name:
        messagebox.showerror("Error", "Please enter your team name!")
        return
    
    # Store user data
    current_user["team_name"] = team_name
    
    # Start game
    show_game_screen()

# ----------------------------------------
# GLOW EFFECT
# ----------------------------------------
def animate_glow():
    global glow_intensity, glow_direction
    glow_intensity += glow_direction * 5
    if glow_intensity >= 255:
        glow_direction = -1
    elif glow_intensity <= 100:
        glow_direction = 1
    hex_color = f"#{glow_intensity:02x}FFD6"
    
    # Apply glow to current screen elements
    if current_screen == "home":
        home_title.config(fg=hex_color)
    elif current_screen == "game":
        title.config(fg=hex_color)
        text_display.config(fg=hex_color)
        change_button.config(fg=hex_color)
        type_button.config(fg=hex_color)
        backspace_button.config(fg=hex_color)
    
    root.after(80, animate_glow)

# ----------------------------------------
# UI SETUP
# ----------------------------------------
root = tk.Tk()
root.title("💻 Tech Is Not Teching - DAKSHA CARNIVAL")
root.configure(bg="#0d1117")

# Set fullscreen mode
root.attributes('-fullscreen', True)

# Mouse cursor will be managed per screen

# Bind ESC key to exit
def exit_game(event=None):
    if messagebox.askokcancel("Exit Game", "Are you sure you want to exit the DAKSHA CARNIVAL?"):
        root.destroy()

root.bind('<Escape>', exit_game)

# Global mouse click functionality
def global_left_click(event):
    """Global left click - triggers CHANGE LETTER button"""
    if current_screen == "game":
        change_letter()

def global_right_click(event):
    """Global right click - triggers TYPE LETTER button"""
    if current_screen == "game":
        type_letter()

# Bind global mouse clicks to the root window
root.bind('<Button-1>', global_left_click)  # Left click anywhere
root.bind('<Button-3>', global_right_click)  # Right click anywhere

# ----------------------------------------
# HOME SCREEN
# ----------------------------------------
home_frame = tk.Frame(root, bg="#0d1117")
home_frame.pack(expand=True, fill="both")

# Home title
home_title = tk.Label(
    home_frame,
    text="🎪 DAKSHA CARNIVAL 🎪\n⚡ TECH IS NOT TECHING ⚡",
    font=("Orbitron", 36, "bold"),
    fg="#00FFD6",
    bg="#0d1117"
)
home_title.pack(pady=30)

# Game guide/instructions
guide_label = tk.Label(
    home_frame,
    text=(
        "🎮 INTERACTIVE TYPING CHALLENGE\n"
        "Professional Mouse-Controlled Interface\n\n"
        "🖱️ LEFT CLICK ANYWHERE → Navigate Letters (a-z → space → A-Z)\n"
        "⏰ AUTO-TIMEOUT → 5-second countdown resets to 'a'\n"
        "🖱️ RIGHT CLICK ANYWHERE → Input Selected Letter\n"
        "⌫ BACKSPACE KEY → Remove Last Character\n\n"
        "🎯 OBJECTIVE: Complete the phrase 'Daksha Carnival'\n"
        "⏱️ TIMER: Starts automatically upon first input\n\n"
        "🖱️ Left Click = Letter Selection | Right Click = Letter Input\n"
        "⌨️ Backspace = Character Deletion\n"
        "🚪 ESC Key = Exit Application"
    ),
    font=("Consolas", 12),
    fg="#FFFFFF",
    bg="#0d1117",
    justify="center"
)
guide_label.pack(pady=20)

# Input frame
input_frame = tk.Frame(home_frame, bg="#0d1117")
input_frame.pack(pady=30)

# Team name input
team_name_label = tk.Label(
    input_frame,
    text="👥 TEAM REGISTRATION:",
    font=("Consolas", 16, "bold"),
    fg="#FFFFFF",
    bg="#0d1117"
)
team_name_label.pack(pady=10)

team_name_entry = tk.Entry(
    input_frame,
    font=("Consolas", 14),
    width=30,
    justify="center"
)
team_name_entry.pack(pady=5)

# Start game button (centered)
start_btn = tk.Button(
    home_frame,
    text="🎮 START GAME 🎮",
    font=("Orbitron", 18, "bold"),
    fg="#00FFD6",
    bg="#161B22",
    activebackground="#21262D",
    activeforeground="#00FFD6",
    relief="raised",
    bd=3,
    width=15,
    height=2,
    command=start_game
)
start_btn.pack(pady=40)

# ----------------------------------------
# GAME SCREEN
# ----------------------------------------
game_frame = tk.Frame(root, bg="#0d1117")

# Timer in top-left corner
timer_label = tk.Label(
    game_frame,
    text="⏱️ 00:00.00",
    font=("Orbitron", 20, "bold"),
    fg="#00FFD6",
    bg="#0d1117",
    relief="raised",
    bd=2
)
timer_label.place(x=20, y=20)

# Digital timer on the right side
digital_timer_label = tk.Label(
    game_frame,
    text="00:00.00",
    font=("Orbitron", 24, "bold"),
    fg="#00FFD6",
    bg="#1a1a2e",
    relief="sunken",
    bd=3,
    padx=20,
    pady=10
)
# Position on the right side (will be positioned dynamically)
# digital_timer_label.place(x=800, y=20)  # Will be positioned in show_game_screen()

# Title frame
frame = tk.Frame(game_frame, bg="#00FFD6", bd=3, relief="groove")
frame.pack(pady=30, ipadx=10, ipady=10)

title = tk.Label(
    frame,
    text="💻 DAKSHA CARNIVAL 💻\n⚡ TECH IS NOT TECHING ⚡",
    font=("Orbitron", 26, "bold"),
    fg="#00FFD6",
    bg="#0d1117"
)
title.pack()

# Word progress display
word_progress_label = tk.Label(
    game_frame,
    text="Word 1 of 4: DAKSHA",
    font=("Consolas", 14, "bold"),
    fg="#00FFD6",
    bg="#0d1117"
)
word_progress_label.pack(pady=10)

info = tk.Label(
    game_frame,
    text=(
        "🎮 INTERACTIVE TYPING CHALLENGE - Professional Interface\n"
        "🔄 LEFT CLICK ANYWHERE → Navigate Letters (a-z → space → A-Z)\n"
        "⏰ AUTO-TIMEOUT → 5-second countdown resets to 'a'\n"
        "✍️ RIGHT CLICK ANYWHERE → Input Selected Letter\n"
        "⌫ BACKSPACE KEY → Remove Last Character\n\n"
        f"🎯 OBJECTIVE: Complete the phrase: {' → '.join(TARGET_WORDS)}\n"
        "⏱️ TIMER: Active and tracking your progress\n"
        "🖱️ Left Click = Letter Selection | Right Click = Letter Input\n"
        "⌨️ Backspace = Character Deletion\n"
        "🚪 ESC Key = Exit Application"
    ),
    font=("Consolas", 12),
    fg="#FFFFFF",
    bg="#0d1117",
    justify="center"
)
info.pack(pady=15)

text_display = tk.Label(
    game_frame,
    text="",
    font=("Courier", 32, "bold"),
    fg="#00FFD6",
    bg="#161B22",
    width=25,
    height=2,
    relief="sunken",
    bd=4
)
text_display.pack(pady=30)

# Button frame for controls
button_frame = tk.Frame(game_frame, bg="#0d1117")
button_frame.pack(pady=20)

# Left side - Change letter button
change_button = tk.Button(
    button_frame,
    text="CHANGE LETTER",
    font=("Consolas", 14, "bold"),
    fg="#00FFD6",
    bg="#161B22",
    activebackground="#21262D",
    activeforeground="#00FFD6",
    relief="raised",
    bd=3,
    width=15,
    height=3
)
change_button.pack(side="left", padx=10)

# Bind left mouse click to change letter button
change_button.bind("<Button-1>", on_change_letter_click)

# Right side - Type letter button
type_button = tk.Button(
    button_frame,
    text="TYPE LETTER\n✍️",
    font=("Consolas", 14, "bold"),
    fg="#00FFD6",
    bg="#161B22",
    activebackground="#21262D",
    activeforeground="#00FFD6",
    relief="raised",
    bd=3,
    width=15,
    height=3,
    command=type_letter
)
type_button.pack(side="right", padx=10)

# Bind right mouse click to type letter button
type_button.bind("<Button-3>", lambda event: type_letter())

# Backspace button (visual only - works with keyboard Backspace key)
backspace_button = tk.Button(
    game_frame,
    text="BACKSPACE\n⌫",
    font=("Consolas", 14, "bold"),
    fg="#00FFD6",
    bg="#161B22",
    activebackground="#21262D",
    activeforeground="#00FFD6",
    relief="raised",
    bd=3,
    width=12,
    height=2,
    state="disabled"  # Disable mouse clicks on this button
)
backspace_button.pack(pady=15)

footer = tk.Label(
    game_frame,
    text="💡 PROFESSIONAL CONTROLS: Left Click = Letter Selection | Right Click = Letter Input 💡",
    font=("Consolas", 13, "italic"),
    fg="#999999",
    bg="#0d1117"
)
footer.pack(side="bottom", pady=15)


# ----------------------------------------
# EVENTS
# ----------------------------------------
# Keep keyboard backspace functionality
root.bind_all("<Key>", block_keys)

# ----------------------------------------
# RUN ANIMATION + MAINLOOP
# ----------------------------------------
# Start with home screen
show_home_screen()
animate_glow()
root.mainloop()