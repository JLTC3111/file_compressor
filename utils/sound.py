import subprocess

def play_success_sound():
    """Play a success sound (macOS system sound)."""
    try:
        subprocess.run(['afplay', '/System/Library/Sounds/Glass.aiff'])
    except Exception:
        pass 