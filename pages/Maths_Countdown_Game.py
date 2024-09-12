import streamlit as st
import random
import itertools
import operator
import time
#import pygame


st.set_page_config(layout="wide")

# Function to generate random numbers based on the user’s choice
def generate_numbers(large_count):
    # Define ranges
    large_numbers = list(range(11, 101, 5))  # Large numbers between 11 and 100
    small_numbers = list(range(1, 11))       # Small numbers between 1 and 10
    
    # Select large and small numbers based on user input
    selected_large = random.sample(large_numbers, large_count)
    selected_small = random.sample(small_numbers, 6 - large_count)
    
    # Combine numbers and return
    selected_numbers = selected_large + selected_small
    random.shuffle(selected_numbers)
    
    return selected_numbers

# Function to generate a target number between 200 and 1000
def generate_target():
    return random.randint(101, 999)


# Initialize pygame mixer
#pygame.mixer.init()

# # Function to play sound in a loop
# def play_sound(sound_file):
#     pygame.mixer.music.load(sound_file)
#     pygame.mixer.music.play(-1)  # Play in a loop

# # Function to stop the sound
# def stop_sound():
#     pygame.mixer.music.stop()

# Countdown timer function and play music during countdown
def countdown_timer(duration):
    # Countdown mechanism with session state
    ph = st.empty()  # Placeholder for countdown display

    # Start playing the sound
    #play_sound('sound/alarm.mp3')  # Replace 'alarm.mp3' with your sound file

    # Countdown loop
    for secs in range(duration, 0, -1):
        mm, ss = divmod(secs, 60)
        ph.metric("Countdown", f"{mm:02d}:{ss:02d}")
        time.sleep(1)

    # Stop the sound after countdown finishes
    #stop_sound()

    # Display countdown finished
    ph.metric("Countdown", "00:00")

    # Mark timer as finished
    st.session_state.timer_started = False

# Solve the generated numbers to reach the target number
def find_solution(selected_numbers, target):
    # Available operators and their functions
    operators = [('+', operator.add), ('-', operator.sub), ('*', operator.mul), ('/', operator.truediv)]

    # Helper function to recursively find the solution
    def evaluate_expression(numbers, operations):
        # Try each permutation of numbers
        for num_order in itertools.permutations(numbers):
            # Try each combination of operations
            for ops in itertools.product(operations, repeat=len(numbers) - 1):
                # Generate expressions step by step
                expression = str(num_order[0])
                value = num_order[0]
                steps = [f"Start with `{num_order[0]}`"]

                try:
                    # Apply each operator between the numbers
                    for i, (symbol, func) in enumerate(ops):
                        next_value = func(value, num_order[i + 1])
                        
                        # Check if the result is a whole number and non-negative
                        if next_value == int(next_value) and next_value >= 0:
                            value = int(next_value)
                            expression += f" {symbol} {num_order[i + 1]}"
                            steps.append(f"Apply `{symbol}` to `{num_order[i + 1]}`: `{value}`")
                        else:
                            break  # If not, break out of the loop

                    # Check if the evaluated expression matches the target
                    if value == target:
                        steps.append(f"### Final result: `{value}`")
                        solution = f"### **Found Solution:**\n`{expression} = {target}`\n\n**Steps:**\n" + "\n".join(f"- {step}" for step in steps)
                        return solution
                except ZeroDivisionError:
                    continue  # Skip division by zero errors

        return "### **No solution found.**"

    # Attempt to find a solution with permutations and operations
    solution = evaluate_expression(selected_numbers, operators)

    # Display the result
    st.markdown(solution)

# Function to reset the game state
def reset_game():
    st.session_state.selected_numbers = []
    st.session_state.target_number = 0
    st.session_state.generated = False
    st.session_state.timer_started = False
    st.session_state.solution_shown = False
    #stop_sound()  # Stop the sound when resetting the game

# Initialize session state variables
if "selected_numbers" not in st.session_state:
    st.session_state.selected_numbers = []
if "target_number" not in st.session_state:
    st.session_state.target_number = 0
if "generated" not in st.session_state:
    st.session_state.generated = False
if "timer_started" not in st.session_state:
    st.session_state.timer_started = False
if "solution_shown" not in st.session_state:
    st.session_state.solution_shown = False

# Initialize the Streamlit app
st.title(":male-technologist: Maths Countdown Game :1234:")

st.markdown("### **Game Rules.**")
st.markdown("1. Select between 0 to 4 number of large numbers to generate. Large numbers are between **11 and 100** and Small numbers are between **1 and 10**.")
st.markdown("2. Click on the 'Generate' button to generate numbers and target.")
st.markdown("3. Start the timer and find a solution to reach the target number.")
st.markdown("4. Click on the 'Show Solution' button to display the solution.")
st.markdown("---")
st.markdown("### :microphone: Who is the boss when it comes to numbers? :male-detective:")
st.markdown("### :mega: Let the game begin!!!!! :fireworks:")
st.markdown("---")

st.markdown("---")

with st.sidebar:
    reset_button = st.button("Reset Game")

    if reset_button:
        reset_game()

# Step 1: Generate Numbers and Target
with st.form("generate_form"):
    st.subheader("Step 1: Generate Numbers and Target")
    large_count = st.number_input("Number of Large Numbers (0 to 4):", min_value=0, max_value=4, value=2)
    generate_button = st.form_submit_button("Generate")

    if generate_button:
        st.session_state.selected_numbers = generate_numbers(large_count)
        st.session_state.target_number = generate_target()
        st.session_state.generated = True
        st.session_state.solution_shown = False
        st.session_state.timer_started = False

# Display selected numbers and target if generated
if st.session_state.generated:
    st.markdown(f"### **Selected Numbers:** `{', '.join(map(str, st.session_state.selected_numbers))}`")
    st.markdown(f"### **Target Number:** `{st.session_state.target_number}`")

# Step 2: Start Timer
if st.session_state.generated and not st.session_state.timer_started and not st.session_state.solution_shown:
    with st.form("timer_form"):
        st.subheader("Step 2: Start Timer")
        timer_duration = st.selectbox("Select Countdown Duration (Secs):", [30, 45, 60], index=0)
        start_timer = st.form_submit_button("Start Timer")

        if start_timer:
            st.session_state.timer_started = True
            countdown_timer(timer_duration)
            st.session_state.timer_started = False  # Reset after timer ends

# Step 3: Show Solution
if st.session_state.generated and not st.session_state.timer_started:
    with st.form("solution_form"):
        st.subheader("Step 3: Show Solution")
        show_solution = st.form_submit_button("Show Solution")

        if show_solution:
            st.session_state.solution_shown = True
            find_solution(st.session_state.selected_numbers, st.session_state.target_number)

