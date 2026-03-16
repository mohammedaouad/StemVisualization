# UI colors and stylesheet for the main window

BG       = "#080C10"
PANEL_BG = "#0E1318"
BORDER   = "#1E2830"
ACCENT   = "#C49A2A"
TEXT_DIM = "#4A5568"
TEXT_MED = "#8899AA"
TEXT_HI  = "#E2E8F0"

STYLE = f"""
QMainWindow, QWidget {{
    background-color: {BG};
    color: {TEXT_HI};
    font-family: 'Segoe UI', sans-serif;
}}
QLabel#title {{
    font-size: 11px; font-weight: 600;
    letter-spacing: 3px; color: {TEXT_DIM};
}}
QLabel#value {{
    font-size: 28px; font-weight: 300;
    color: {TEXT_HI}; font-family: 'Consolas', monospace;
}}
QLabel#unit {{
    font-size: 13px; color: {TEXT_DIM};
    font-family: 'Consolas', monospace;
}}
QLabel#panel_title {{
    font-size: 13px; font-weight: 600;
    letter-spacing: 2px; color: {TEXT_MED};
    padding: 8px 0px 4px 0px;
}}
QLabel#leg_text {{ font-size: 11px; color: {TEXT_MED}; padding-left: 4px; }}
QSlider::groove:horizontal {{
    height: 2px; background: {BORDER}; border-radius: 1px;
}}
QSlider::handle:horizontal {{
    background: {ACCENT}; width: 14px; height: 14px;
    margin: -6px 0; border-radius: 7px;
}}
QSlider::sub-page:horizontal {{ background: {ACCENT}; border-radius: 1px; }}
QFrame#separator {{ background-color: {BORDER}; max-width: 1px; min-width: 1px; }}
"""