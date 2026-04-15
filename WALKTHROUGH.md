# CryptoSign - Modern UI/UX Upgrade

The CryptoSign project has been upgraded from a legacy set of Python CLI/Tkinter scripts to a modern, responsive web application. This provides a unified "full flow" demo as requested, using **Bootstrap 5** and **Bootstrap Icons** for a premium aesthetic.

## Key Changes

### 1. Unified Backend Architecture
Replaced separate Python scripts (`register_user.py`, `key_generation.py`, etc.) with a single, consolidated Flask application `app.py`. This app provides:
- **RESTful API**: Endpoints for each operation (Register, Key Gen, Sign, Verify).
- **Static Template Serving**: Serves the modern frontend dashboard.

### 2. Premium Dashboard UI
Created a single-page dashboard (`templates/index.html`) featuring:
- **Responsive Navigation**: Sidebar-based navigation for different "crypto" stages.
- **Glassmorphism Design**: Modern, semi-transparent dark-themed cards.
- **Real-time Status Updates**: AJAX-powered interaction with the API.
- **Micro-animations**: Smooth tab transitions and visual feedback.

### 3. Clean Project Structure
Removed all redundant UI files and CLI entry points:
- Deleted `app_ui.py` (Tkinter).
- Deleted `main.py`, `register_user.py`, `key_generation.py`, `sign_message.py`, and `verify_signature.py` (CLI UI).

## New File Structure
- `app.py`: New Flask backend.
- `templates/index.html`: New Bootstrap 5 dashboard.
- `requirements.txt`: Project dependencies.
- `keys/`: Storage for generated RSA keys.
- `users.json`: Persistent user registry.

## How to Run
I've created a workflow to simplify running the demo:
1. Open the terminal.
2. Run `/run-demo` (if your environment supports it) or simply run:
   ```bash
   python app.py
   ```
3. Visit `http://127.0.0.1:5000` in your browser.
