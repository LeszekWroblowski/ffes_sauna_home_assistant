# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-24

### Added
- Initial release of FFES Sauna integration for Home Assistant
- Real-time temperature and humidity monitoring
- Full sauna status control (Off, Heating, Ventilation, Standby)
- Light and AUX output switches
- Quick control buttons for all sauna modes
- Profile selection with 7 preset modes:
  - Infrared Sauna
  - Dry Sauna
  - Wet Sauna
  - Ventilation
  - Steambath
  - Infrared CPIR
  - Infrared MIX
- Adjustable target temperature (20-110°C)
- Humidity control (0-100%)
- Config flow for easy UI-based setup
- Polish and English translations
- HACS compatibility
- Comprehensive documentation with:
  - Installation guide (INSTALL.md)
  - Automation examples (AUTOMATION_EXAMPLES.md)
  - README with usage instructions
- Data update coordinator for efficient polling (10-second interval)
- Device info for proper Home Assistant device registry integration

### Technical Details
- Async/await architecture for non-blocking operations
- Proper error handling and logging
- Automatic data refresh after commands
- REST API client with timeout handling
- Entity descriptions for all sensors, switches, buttons, selects, and numbers

## [Unreleased]

### Planned Features
- Climate entity integration for better thermostat-like control
- Session timer with countdown
- Energy consumption tracking (if supported by controller)
- Historical data graphs
- Advanced scheduling with calendar integration
- Mobile app notifications
- Voice assistant integrations (Alexa, Google Home)
- Multi-language support expansion
- Custom session presets
- Maintenance reminders

---

For detailed information about each release, see [Releases](https://github.com/LeszekWroblowski/ffes_sauna_home_assistant/releases)
