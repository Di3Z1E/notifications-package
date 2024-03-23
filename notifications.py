import re
import tkinter as tk
import tkinter.font as tkfont


def close_window(root):
    """Close the notification window."""
    root.destroy()


def validate_font(font):
    """Validate the font provided by the user."""
    try:
        tkfont.nametofont(font)
        return True
    except tk.TclError:
        return False


def is_valid_color(color):
    """Checks if the provided string is a valid hex color code."""
    color_regex = r"^#[0-9A-Fa-f]{6}$"
    return re.match(color_regex, color) is not None


def show_toast(title="Missing Title", message="Missing Message", duration=2, color="#424242", position="bottom-right",
               icon=None, font=None):
    """
    Show a toast notification window.

    Args:
        title (str): The title of the notification (default is "Missing Title").
        message (str): The message of the notification (default is "Missing Message").
        duration (int): The duration of the notification appearance in seconds (default is 2).
        color (str): The background color of the notification (default is "#424242").
        position (str): The position of the notification (default is "bottom-right").
                        Possible values: "center", "bottom-left", "bottom-right", "bottom-center", "upper-center", "upper-left", "upper-right"
        icon (str): The path to the icon image file (default is None).
        font (str): The font name for the title and message labels (default is None).
    """

    if len(title) > 24:
        raise ValueError("Title length too long")

    if not is_valid_color(color):
        raise ValueError("Invalid color format. Use #RRGGBB format.")

    if len(message) > 120:
        raise ValueError("Notification message is too long, 120 characters allowed.")

    root = tk.Tk()
    root.title(title)

    # Remove the title bar
    root.overrideredirect(True)

    # Set background color
    root.configure(bg=color)

    # Calculate screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate required window height based on message length
    lines = message.split('\n')
    line_height = 15  # Adjust as needed
    message_height = len(lines) * line_height

    # Set window size
    window_width = 300
    window_height = max(message_height + 100, 100)  # Ensure a minimum height of 100 pixels

    # Set window position
    if position == "center":
        window_x = (screen_width - window_width) // 2
        window_y = (screen_height - window_height) // 2
    elif position == "bottom-left":
        window_x = 10
        window_y = screen_height - window_height - 30
    elif position == "bottom-right":
        window_x = screen_width - window_width - 10
        window_y = screen_height - window_height - 30
    elif position == "bottom-center":
        window_x = (screen_width - window_width) // 2
        window_y = screen_height - window_height - 30
    elif position == "upper-center":
        window_x = (screen_width - window_width) // 2
        window_y = 10
    elif position == "upper-left":
        window_x = 10
        window_y = 10
    elif position == "upper-right":
        window_x = screen_width - window_width - 10
        window_y = 10
    else:
        raise ValueError(
            "Invalid position. Possible values: 'center', 'bottom-left', 'bottom-right', 'bottom-center', 'upper-center', 'upper-left', 'upper-right'")

    root.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

    if icon:
        # Load and resize the icon
        try:
            img = tk.PhotoImage(file=icon)
            img = img.subsample(8, 8)  # Resize the icon to 4x4
            label_icon = tk.Label(root, image=img, bg=color)
            label_icon.image = img  # Keep reference to avoid garbage collection
            label_icon.place(x=10, y=10)  # Set icon position to the top left corner
        except Exception as e:
            print("Error loading icon:", e)
            # Display ℹ️ instead of the icon
            label_icon = tk.Label(root, text="ℹ️", font=("Arial", 12), bg=color)
            label_icon.place(x=10, y=10)  # Set icon position to the top left corner
    else:
        # Display ℹ️ instead of the icon
        label_icon = tk.Label(root, text="ℹ️", font=("Arial", 12), bg=color)
        label_icon.place(x=10, y=10)  # Set icon position to the top left corner

    if font:
        if validate_font(font):
            title_font = font
            message_font = font
        else:
            raise ValueError("Invalid font. Please choose one of the available fonts: {}".format(tkfont.names()))
    else:
        title_font = ("Arial", 12, "bold")
        message_font = ("Arial", 10)

    label_title = tk.Label(root, text=title, font=title_font, bg=color, fg="white")
    label_title.pack(pady=5)

    label_message = tk.Label(root, text=message, font=message_font, bg=color, fg="white", wraplength=window_width - 20)
    label_message.pack(pady=5)

    # Close window after specified duration
    root.after(duration * 1000, close_window, root)

    root.mainloop()
