"""Basic automation example - launch an app, find a window, take a screenshot."""

from pyguit import GUIController

with GUIController() as controller:
    # Launch the application
    controller.attach_openbox()

    controller.launch_app(
        app_name="my_app",
        path="/path/to/application",
    )

    # Wait for the main window to appear
    import time
    time.sleep(5)

    # Find and center the window
    window = controller.find_window("My Application")
    controller.center_window(window)

    # Take a screenshot
    controller.capture_screenshot("results/main_window.png")

    # Click a button found by reference image
    button = controller.wait_for_image(
        "references/start_button.png",
        timeout=10,
        confidence=0.9,
    )
    controller.click(*button)

    # Type text into a field
    controller.type_text("192.168.1.100", interval=0.05)

    # Take another screenshot
    controller.capture_screenshot("results/after_input.png")

    # Cleanup happens automatically via context manager
