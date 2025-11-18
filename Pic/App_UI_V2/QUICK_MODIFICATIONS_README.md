# Quick Modifications Guide

This guide explains how to use `quick_modifications.py` to easily customize the UI without touching multiple files.

## Overview

`quick_modifications.py` is a centralized configuration file that controls **all** visual aspects of the app:
- Text sizes for every element
- Colors for all text, backgrounds, and borders
- Spacing and padding
- Section widths and positions
- Component visibility

## How to Use

1. Open `quick_modifications.py`
2. Find the section you want to modify
3. Change the values
4. Save the file
5. Restart the app

That's it! No need to edit multiple files or search through CSS.

## Common Modifications

### Change Text Sizes

Edit the `TEXT_SIZES` dictionary:

```python
TEXT_SIZES: Dict[str, str] = {
    "main_title": "3rem",              # Make main title bigger
    "section_header": "2rem",          # Make section headers bigger
    "subsection_header": "1.5rem",     # Make sub-sections bigger
    # ... etc
}
```

### Change Colors

Edit the `TEXT_COLORS` and `BACKGROUND_COLORS` dictionaries:

```python
TEXT_COLORS: Dict[str, str] = {
    "primary": "#2c3e50",              # Change main text to dark blue-gray
    "secondary": "#7f8c8d",            # Change secondary text
    # ... etc
}

BACKGROUND_COLORS: Dict[str, str] = {
    "main": "#ecf0f1",                 # Change background to light gray
    # ... etc
}
```

### Change Section Widths

Edit the `LAYOUT` dictionary:

```python
LAYOUT: Dict[str, Any] = {
    "section_1_width": 1.0,            # Make upload section wider
    "section_2_width": 1.0,            # Make config section wider
    "section_3_width": 1.0,            # Make playlist section narrower
    # Must sum to ~3.0
}
```

### Reorder Sections

Change the section order:

```python
LAYOUT: Dict[str, Any] = {
    "section_order": [2, 1, 3],        # Put config first, upload second
}
```

### Hide Elements

Toggle visibility:

```python
VISIBILITY: Dict[str, bool] = {
    "show_section_badges": False,      # Hide numbered badges (1, 2, 3)
    "show_section_icons": False,       # Hide emoji icons
}
```

### Customize Playlist Window

Edit the `PLAYLIST_WINDOW` dictionary:

```python
PLAYLIST_WINDOW: Dict[str, Any] = {
    "max_height": "600px",             # Make playlist taller
    "background": "#1a1a2e",           # Change dark background
    "dot_colors": ["#ff6b6b", "#4ecdc4", "#ffe66d"],  # Custom dot colors
}
```

### Add Custom CSS

Add any custom CSS at the bottom:

```python
CUSTOM_CSS: str = """
/* Make all buttons rounded */
.stButton > button {
    border-radius: 20px !important;
}

/* Custom font */
* {
    font-family: 'Helvetica Neue', sans-serif !important;
}
"""
```

## File Structure

The settings flow like this:

```
quick_modifications.py  →  config.py  →  styles.py  →  app.py
     (source)              (imports)     (imports)     (uses)
```

## Tips

1. **Start Small**: Change one thing at a time to see the effect
2. **Use Browser Dev Tools**: Inspect elements to see what CSS is applied
3. **Keep Backups**: Copy `quick_modifications.py` before major changes
4. **Check Color Contrast**: Use tools like WebAIM to ensure text is readable
5. **Test Different Screen Sizes**: The app is responsive, test on different widths

## Common Issues

### Changes Don't Appear
- Make sure you saved the file
- Restart the Streamlit app (Ctrl+C, then run again)
- Clear browser cache

### Colors Look Wrong
- Check hex codes are valid (e.g., `#ff0000` not `ff0000`)
- Ensure color names are correct

### Layout Breaks
- Section widths must sum to ~3.0
- Spacing values should include units (e.g., `"16px"` not `16`)

## Examples

### Dark Theme
```python
BACKGROUND_COLORS = {
    "main": "#1a1a2e",
    "section": "#16213e",
    "card": "#0f3460",
}
TEXT_COLORS = {
    "primary": "#e5e5e5",
    "secondary": "#a0a0a0",
}
```

### Large Text (Accessibility)
```python
TEXT_SIZES = {
    "section_header": "2rem",
    "subsection_header": "1.5rem",
    "normal_text": "18px",
}
```

### Compact Layout
```python
SPACING = {
    "small": "4px",
    "medium": "8px",
    "large": "12px",
}
```

## Need Help?

If you break something:
1. Revert to the original `quick_modifications.py`
2. Check the syntax (Python dictionaries need commas!)
3. Look for typos in color codes or size values

Enjoy customizing your app! 🎨

