import pygame
import sys
import pygwidgets

# ---------------- Constants ----------------
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
FPS = 30

pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Temperature Converter")
clock = pygame.time.Clock()

# ---------------- Widgets ----------------
oLabelInput = pygwidgets.DisplayText(window, (50, 20), "Enter Temperature:", fontSize=24)
oTempInput = pygwidgets.InputText(window, (50, 50), "", fontSize=24)

oLabelConversion = pygwidgets.DisplayText(window, (50, 90), "Conversion Type:", fontSize=24)

# Two RadioButtons (singular)
oToC = pygwidgets.TextRadioButton(window, (50, 120), "To Celsius")
oToF = pygwidgets.TextRadioButton(window, (50, 150), "To Fahrenheit")

# Default selection
oToC.setSelected(True)
oToF.setSelected(False)

oConvertButton = pygwidgets.TextButton(window, (50, 200), "Convert")
oOutput = pygwidgets.DisplayText(window, (50, 240), "", fontSize=24)

# ---------------- Helper function ----------------
def draw_radio_highlight():
    """Draw a rectangle behind the selected radio button for visual highlight."""
    if oToC.getSelected():
        pygame.draw.rect(window, GRAY, (oToC.getRect().x - 5, oToC.getRect().y - 5,
                                        oToC.getRect().width + 10, oToC.getRect().height + 10))
    elif oToF.getSelected():
        pygame.draw.rect(window, GRAY, (oToF.getRect().x - 5, oToF.getRect().y - 5,
                                        oToF.getRect().width + 10, oToF.getRect().height + 10))

# ---------------- Main Loop ----------------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # Radio button events
        if oToC.handleEvent(event):
            oToC.setSelected(True)
            oToF.setSelected(False)
            oOutput.setValue("")
        if oToF.handleEvent(event):
            oToC.setSelected(False)
            oToF.setSelected(True)
            oOutput.setValue("")

        # Convert button or Enter key
        if oTempInput.handleEvent(event) or oConvertButton.handleEvent(event):
            temp = oTempInput.getText()
            if temp.replace('.', '', 1).isdigit():
                value = float(temp)
                if oToC.getSelected():
                    converted = (value - 32) / (9/5)
                    oOutput.setValue(f"{converted:.2f} °C")
                else:
                    converted = value * 9/5 + 32
                    oOutput.setValue(f"{converted:.2f} °F")
            else:
                oOutput.setValue("Enter a number!")

    # Clear screen
    window.fill(WHITE)

    # Draw highlight behind selected radio button
    draw_radio_highlight()

    # Draw widgets
    oLabelInput.draw()
    oTempInput.draw()
    oLabelConversion.draw()
    oToC.draw()
    oToF.draw()
    oConvertButton.draw()
    oOutput.draw()

    pygame.display.update()
    clock.tick(FPS)