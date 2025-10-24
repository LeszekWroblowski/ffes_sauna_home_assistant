# FFES Sauna Integration for Home Assistant

Custom integration for FFES Sauna controllers with full control and monitoring capabilities.

## Features

- 🌡️ Real-time temperature and humidity monitoring
- 🔥 Full sauna control (heating, ventilation, standby, off)
- 💡 Light and AUX control
- 📊 Session management with customizable profiles
- 🎚️ Adjustable temperature and humidity settings
- 🇵🇱 Polish and English translations

## Installation

### HACS (Recommended)

1. Open HACS in your Home Assistant
2. Click on "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL: `https://github.com/LeszekWroblowski/ffes_sauna_home_assistant`
6. Select category: "Integration"
7. Click "Add"
8. Find "FFES Sauna Control" in HACS and install it
9. Restart Home Assistant

### Manual Installation

1. Copy the `ffes_sauna` folder to your `custom_components` directory
2. Restart Home Assistant

## Configuration

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for "FFES Sauna"
4. Enter your sauna controller's IP address (e.g., `192.168.0.208`)
5. Click Submit

The integration will automatically discover all available features.

## Entities

After configuration, the following entities will be created:

### Sensors
- **Temperature** - Current sauna temperature
- **Humidity** - Current humidity level
- **Target Temperature** - Set temperature
- **Status** - Current operating status
- **Profile** - Active sauna profile
- **Session Time** - Configured session duration
- **Ventilation Time** - Ventilation period
- **Aromatherapy** - Aromatherapy level
- **Humidity Setting** - Humidity/vaporizer setting

### Switches
- **Light** - Sauna light control
- **AUX** - Auxiliary output control

### Buttons
- **Turn Off** - Turn off the sauna
- **Start Heating** - Begin heating
- **Start Ventilation** - Start ventilation
- **Standby** - Put sauna in standby mode

### Controls
- **Profile** - Select sauna profile (Infrared, Dry, Wet, etc.)
- **Target Temperature** - Set desired temperature (20-110°C)
- **Humidity Setting** - Adjust humidity level (0-100%)

## Usage Examples

### Automation Example

Turn on sauna before arriving home:

```yaml
automation:
  - alias: "Preheat Sauna"
    trigger:
      - platform: time
        at: "17:00:00"
    condition:
      - condition: state
        entity_id: person.your_name
        state: "not_home"
    action:
      - service: button.press
        target:
          entity_id: button.ffes_sauna_start_heating
      - service: number.set_value
        target:
          entity_id: number.ffes_sauna_target_temperature
        data:
          value: 80
```

### Dashboard Card Example

```yaml
type: vertical-stack
cards:
  - type: entities
    title: Sauna Control
    entities:
      - entity: sensor.ffes_sauna_status
      - entity: sensor.ffes_sauna_temperature
      - entity: sensor.ffes_sauna_humidity
      - entity: number.ffes_sauna_target_temperature
      - entity: select.ffes_sauna_profile
      - type: divider
      - entity: button.ffes_sauna_start_heating
      - entity: button.ffes_sauna_start_ventilation
      - entity: button.ffes_sauna_standby
      - entity: button.ffes_sauna_turn_off
      - type: divider
      - entity: switch.ffes_sauna_light
      - entity: switch.ffes_sauna_aux
```

## Sauna Profiles

1. **Infrared Sauna** - Low temperature infrared heating
2. **Dry Sauna** - Traditional high-temperature dry sauna
3. **Wet Sauna** - Sauna with added humidity
4. **Ventilation** - Air circulation mode
5. **Steambath** - High humidity steam mode
6. **Infrared CPIR** - Ceramic infrared heating
7. **Infrared MIX** - Mixed infrared heating

## Troubleshooting

### Cannot Connect
- Verify the IP address is correct
- Ensure the sauna controller is powered on
- Check that Home Assistant can reach the controller's network
- Try accessing `http://[IP]/sauna-data` in a browser

### Entities Not Updating
- Check Home Assistant logs for errors
- Verify network connectivity to the controller
- The integration polls every 10 seconds by default

### Commands Not Working
- Check that the controller responds to manual commands
- Review Home Assistant logs for error messages
- Ensure no firewall is blocking communication

## Support

For issues, feature requests, or questions:
- GitHub Issues: [https://github.com/LeszekWroblowski/ffes_sauna_home_assistant/issues](https://github.com/LeszekWroblowski/ffes_sauna_home_assistant/issues)

## License

MIT License - see LICENSE file for details

## Credits

Created for FFES Sauna Controllers
