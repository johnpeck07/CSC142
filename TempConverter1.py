#Solo code 5
import os
import sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import pygame
import pygwidgets

# ---------------- Constants ----------------
BLACK = (0, 0, 0)
BLACKISH = (10, 10, 10)
GRAY = (128, 128, 128)
WHITE = (255, 255, 255)
BACKGROUND_COLOR = (0, 180, 180)
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 640
FRAMES_PER_SECOND = 30

# ---------------- Initialize Pygame ----------------
pygame.init()
window = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
pygame.display.set_caption("Temperature Converter")
clock = pygame.time.Clock()

# ---------------- Widgets ----------------
convertedDisplay = pygwidgets.DisplayText(
    window, (0, 20), '32', fontSize=36, width=640,
    textColor=BLACK, justified='center'
)

userInputText = pygwidgets.InputText(
    window, (20, 100), '0', textColor=WHITE,
    backgroundColor=BLACK, fontSize=24, width=250
)

# Using Kalb's TextRadioButton with group name
celsiusRadio = pygwidgets.TextRadioButton(window, (50, 150), 'ConversionGroup',
                                          'Celsius', value=True)
fahrenheitRadio = pygwidgets.TextRadioButton(window, (50, 190), 'ConversionGroup',
                                             'Fahrenheit', value=False)

conversionButton = pygwidgets.TextButton(window, (50, 250), 'Convert')

# ---------------- Conversion function ----------------
def convert_temperature():
    temp_str = userInputText.getText()
    try:
        temp = float(temp_str)
    except ValueError:
        convertedDisplay.setText("Enter a valid number!")
        return

    if celsiusRadio.getValue():  # Celsius selected
        converted = (temp - 32) / (9/5)
        convertedDisplay.setText(f"{converted:.2f} °C")
    else:  # Fahrenheit selected
        converted = temp * 9/5 + 32
        convertedDisplay.setText(f"{converted:.2f} °F")

# ---------------- Main Loop ----------------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Handle widgets
        if userInputText.handleEvent(event):
            convert_temperature()  # Convert on Enter key
        if conversionButton.handleEvent(event):
            convert_temperature()
        if celsiusRadio.handleEvent(event):
            # Group ensures only one selected, so just update display
            convertedDisplay.setText("")
        if fahrenheitRadio.handleEvent(event):
            convertedDisplay.setText("")

    # Clear window
    window.fill(BACKGROUND_COLOR)

    # Draw widgets
    userInputText.draw()
    celsiusRadio.draw()
    fahrenheitRadio.draw()
    conversionButton.draw()
    convertedDisplay.draw()

    # Update display
    pygame.display.update()

    clock.tick(FRAMES_PER_SECOND)
