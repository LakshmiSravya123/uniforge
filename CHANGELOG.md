# Changelog

All notable changes to UniForge will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-11-04

### Added
- **Server-Side Pattern Storage**: Patterns now saved to `patterns.json` via REST API
- **Global Hotkey Support**: Register system-wide keyboard shortcuts (e.g., `ctrl+shift+p`)
- **Patterns API**: Full CRUD operations via `/patterns` endpoints (GET/POST/DELETE)
- **Named Pattern Replay**: Replay patterns by name via `/replay/name/<name>`
- **Hotkey Registration**: POST `/hotkey/register` endpoint for binding hotkeys
- **Health Monitoring**: GET `/health` endpoint for server status checks
- **Enhanced Frontend**: Hotkey input field with visual display in pattern list
- **Export/Import**: Backend-synced pattern export and import functionality
- **Voice Control**: Hands-free pattern replay via Web Speech API
- **Command Palette**: Cmd+K (or Ctrl+K) for quick actions
- **Drag & Drop Todos**: Reorder tasks intuitively in the UI
- **Modern UI**: Windsurf-inspired design with teal accents and smooth animations

### Changed
- **Unified Server**: Consolidated all endpoints into single Flask server on port 5001
- **Persistence**: Both todos and patterns now persist to JSON files (no more in-memory storage)
- **Frontend Storage**: Migrated from localStorage to backend API for patterns
- **OAuth Optional**: GitHub OAuth is now completely optional (no longer required)

### Fixed
- **Keyboard API**: Fixed invalid `keyboard.get_typed_strings()` usage in watcher
- **Port Conflicts**: Proper cleanup and port management
- **macOS Permissions**: Made keyboard features optional when permissions not granted
- **Error Handling**: Graceful degradation for optional features

### Documentation
- **README.md**: Complete rewrite with features comparison vs Cursor/Windsurf
- **QUICKSTART.md**: Comprehensive quick start and troubleshooting guide
- **WORKING_STATUS.md**: Detailed status of all fixes and enhancements
- **setup_permissions.sh**: Helper script for macOS accessibility setup
- **.env.template**: Template for optional environment variables

### Technical
- **Dependencies**: Flask, Flask-CORS, keyboard, requests, python-dotenv
- **Frontend**: Vanilla JavaScript, Vite, HTML5, CSS3
- **Backend**: Python 3.10+, Flask REST API
- **Storage**: JSON file-based persistence

## [Unreleased]

### Planned
- Configurable recording duration (query parameter)
- Enhanced error messages and validation
- Unit tests with pytest
- GitHub Actions CI/CD
- Binary releases for macOS/Windows/Linux
- Pattern sharing/marketplace
- Encrypted pattern storage
- Multi-user support

---

## Version History

- **v0.1.0** (2025-11-04) - Initial production release with server-side storage and hotkeys
- **v0.0.1** (2025-11-03) - MVP prototype with basic recording/replay
