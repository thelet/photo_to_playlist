# Quick Reference - What Controls What

Visual guide showing which setting in `quick_modifications.py` controls each UI element.

## Text Sizes Reference

| UI Element | Setting | Default | Location |
|------------|---------|---------|----------|
| App title "Your Ai DJ • Photo → Playlist" | `TEXT_SIZES["main_title"]` | `2.5rem` | Top of page |
| Section headers (1, 2, 3 with badges) | `TEXT_SIZES["section_header"]` | `1.5rem` | Each section |
| Sub-section headers (Vision, Text, etc.) | `TEXT_SIZES["subsection_header"]` | `1.1rem` | Within sections |
| Regular text | `TEXT_SIZES["normal_text"]` | `14px` | All body text |
| Captions/hints | `TEXT_SIZES["small_text"]` | `12px` | Under headers |
| Track titles in playlist | `TEXT_SIZES["track_title"]` | `13px` | Playlist window |
| Track artist/duration | `TEXT_SIZES["track_details"]` | `11px` | Playlist window |
| Buttons | `TEXT_SIZES["button_text"]` | `14px` | All buttons |
| Dropdowns | `TEXT_SIZES["dropdown_text"]` | `14px` | All dropdowns |

## Header Spacing Reference

Control padding and margins for all headers:

| Header Type | Setting | Default | What it controls |
|-------------|---------|---------|------------------|
| Main title top margin | `HEADER_SPACING["main_title_top"]` | `0` | Space above app title |
| Main title bottom margin | `HEADER_SPACING["main_title_bottom"]` | `1rem` | Space below app title |
| Section header top margin | `HEADER_SPACING["section_header_top"]` | `0` | Space above section headers |
| Section header bottom margin | `HEADER_SPACING["section_header_bottom"]` | `1rem` | Space below section headers |
| Section header padding | `HEADER_SPACING["section_header_padding"]` | `0` | Internal padding |
| Subsection top margin | `HEADER_SPACING["subsection_header_top"]` | `1rem` | Space above Vision, Text, etc. |
| Subsection bottom margin | `HEADER_SPACING["subsection_header_bottom"]` | `0.5rem` | Space below subsections |
| Subsection left padding | `HEADER_SPACING["subsection_header_left"]` | `0` | Left padding |
| Subsection right padding | `HEADER_SPACING["subsection_header_right"]` | `0` | Right padding |
| Photo preview top margin | `HEADER_SPACING["photo_preview_top"]` | `1rem` | Space above photo preview |
| Photo preview bottom margin | `HEADER_SPACING["photo_preview_bottom"]` | `0.5rem` | Space below photo preview |

## Color Reference

| Element | Setting | Default | Usage |
|---------|---------|---------|-------|
| Main text | `TEXT_COLORS["primary"]` | `#000000` | All regular text |
| Secondary text | `TEXT_COLORS["secondary"]` | `#333333` | Less important text |
| Muted text | `TEXT_COLORS["muted"]` | `#666666` | Very subtle text |
| Success messages | `TEXT_COLORS["success"]` | `#28a745` | "Photo uploaded!" |
| Error messages | `TEXT_COLORS["error"]` | `#dc3545` | Error alerts |
| Links | `TEXT_COLORS["link"]` | `#007bff` | "Open in Deezer" |
| Main background | `BACKGROUND_COLORS["main"]` | `#ffffff` | Page background |
| Section background | `BACKGROUND_COLORS["section"]` | `#f8f9fa` | Light gray areas |
| Primary button | `BACKGROUND_COLORS["button_primary"]` | `#007bff` | "Generate playlist" |

## Layout Reference

| Element | Setting | Default | Effect |
|---------|---------|---------|--------|
| Upload section width | `LAYOUT["section_1_width"]` | `0.7` | Left column |
| Config section width | `LAYOUT["section_2_width"]` | `0.8` | Middle column |
| Playlist section width | `LAYOUT["section_3_width"]` | `1.5` | Right column |
| Section order | `LAYOUT["section_order"]` | `[1, 2, 3]` | Left to right order |
| Max content width | `LAYOUT["max_width"]` | `1500px` | Overall width |
| Top padding | `LAYOUT["padding_top"]` | `1.5rem` | Space from top |

## Spacing Reference

| Setting | Default | Where Used |
|---------|---------|------------|
| `SPACING["tiny"]` | `4px` | Minimal gaps |
| `SPACING["small"]` | `8px` | Small gaps |
| `SPACING["medium"]` | `16px` | Standard gaps |
| `SPACING["large"]` | `24px` | Section spacing |
| `SPACING["xlarge"]` | `32px` | Large spacing |
| `SPACING["border_radius"]` | `8px` | Rounded corners |

## Playlist Window Reference

| Setting | Default | Effect |
|---------|---------|--------|
| `PLAYLIST_WINDOW["max_height"]` | `430px` | Height before scrolling |
| `PLAYLIST_WINDOW["background"]` | `#020617` | Dark background |
| `PLAYLIST_WINDOW["border_radius"]` | `18px` | Rounded corners |
| `PLAYLIST_WINDOW["track_spacing"]` | `10px` | Space between tracks |
| `PLAYLIST_WINDOW["dot_colors"][0]` | `#ef4444` | Red dot (top right) |
| `PLAYLIST_WINDOW["dot_colors"][1]` | `#facc15` | Yellow dot |
| `PLAYLIST_WINDOW["dot_colors"][2]` | `#22c55e` | Green dot |

## Visibility Toggles

| Setting | Default | What it shows/hides |
|---------|---------|---------------------|
| `VISIBILITY["show_section_badges"]` | `True` | Numbered circles (1, 2, 3) |
| `VISIBILITY["show_section_icons"]` | `True` | Emojis (📷, ⚙️, 🎵) |
| `VISIBILITY["show_captions"]` | `True` | Instruction text |
| `VISIBILITY["show_playlist_dots"]` | `True` | Colored dots in playlist |

## Quick Copy-Paste Examples

### Make everything bigger
```python
TEXT_SIZES = {
    "section_header": "2rem",      # Was 1.5rem
    "subsection_header": "1.5rem", # Was 1.1rem
    "normal_text": "16px",         # Was 14px
    # ... update others proportionally
}
```

### Change accent color to purple
```python
BORDER_COLORS["badge"] = "#9b59b6"
BACKGROUND_COLORS["button_primary"] = "#9b59b6"
TEXT_COLORS["info"] = "#9b59b6"
TEXT_COLORS["link"] = "#9b59b6"
```

### Make upload section bigger, config smaller
```python
LAYOUT = {
    "section_1_width": 1.2,   # Was 0.7
    "section_2_width": 0.6,   # Was 0.8
    "section_3_width": 1.2,   # Was 1.5 (adjust to sum ~3.0)
}
```

### Increase playlist height
```python
PLAYLIST_WINDOW = {
    "max_height": "600px",    # Was 430px
    # ... keep other settings
}
```

## Pro Tips

1. **Keep proportions**: If you increase `section_header`, increase `subsection_header` proportionally
2. **Test contrast**: Dark text on dark backgrounds won't be readable
3. **Mobile-friendly**: Very large text may break on small screens
4. **Sum to 3.0**: Section widths should total around 3.0 for proper layout

## Color Palette Ideas

### Blue Theme (Default)
- Primary: `#007bff`
- Success: `#28a745`
- Background: `#ffffff`

### Green Theme
- Primary: `#10b981`
- Success: `#059669`
- Background: `#f0fdf4`

### Purple Theme
- Primary: `#8b5cf6`
- Success: `#10b981`
- Background: `#faf5ff`

### Dark Theme
- Primary: `#60a5fa`
- Success: `#34d399`
- Background: `#1f2937`
- Text Primary: `#f9fafb`

