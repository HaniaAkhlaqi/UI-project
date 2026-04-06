# Gasthaus Peking Duck — Restaurant Menu App

A Python/Tkinter restaurant menu application built with a Model-View-Controller (MVC) architecture. This project demonstrates a multilingual menu user interface, group ordering, payment options, and dietary filtering.

## Features

- Full restaurant menu with categories: Starters, Soups, Main Courses, Desserts, Beverages, Set Meals, and Today's Special
- Multilingual UI support: English, German, and Chinese
- Dietary filters: vegan, vegetarian, gluten-free, lactose-free, non-alcoholic, and seafood
- Group ordering with multiple people/seats and per-person order tabs
- Order total calculation with tip support
- Payment actions: pay all or split bill with per-person totals
- Drag-and-drop and button-based item ordering
- Call service button with status toggle

## Files

- `menu.py` — Main application source code implementing the full Tkinter UI and MVC structure
- `menu-gemini2.py`, `menu-lovable.py` — Alternate menu prototypes or versions
- `README.md` — Project documentation

## Requirements

- Python 3.x
- Standard library only (`tkinter` is required for the GUI)

## Run the app

From the `UI-project` directory:

```bash
python3 menu.py
```

## Usage

1. Use the language buttons to switch the interface between English, German, and Chinese.
2. Browse menu categories and add items to the current order using the `+` button or drag-and-drop.
3. Add or remove people using the `+` / `-` controls in the order panel.
4. Switch between people in group order tabs to manage each person’s items.
5. Select a tip percentage to update the total amount.
6. Use `Pay All` to pay the full bill or `Split Bill` to calculate each person’s own payment.

## Notes

- The app stores orders in memory only and does not save data between runs.
- The current implementation is for desktop use with Tkinter and is not packaged as an installer.

## Future improvements

- Add persistence to save past orders
- Improve layout responsiveness for smaller windows, currently partially functional with existing scrol bars
- Add item images and richer menu styling
