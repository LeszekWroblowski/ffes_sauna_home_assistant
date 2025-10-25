# Przykłady Automatyzacji dla FFES Sauna

## 1. Rozgrzewanie sauny przed powrotem do domu

Automatyczne włączenie sauny 30 minut przed Twoim spodziewanym powrotem:

```yaml
automation:
  - alias: "Sauna: Rozgrzej przed powrotem"
    description: "Włącz saunę gdy wyjeżdżam z pracy"
    trigger:
      - platform: zone
        entity_id: person.twoje_imie
        zone: zone.praca
        event: leave
    action:
      - service: button.press
        target:
          entity_id: button.ffes_sauna_start_heating
      - service: number.set_value
        target:
          entity_id: number.ffes_sauna_target_temperature
        data:
          value: 85
      - service: select.select_option
        target:
          entity_id: select.ffes_sauna_profile
        data:
          option: "Dry Sauna"
```

## 2. Powiadomienie gdy sauna jest gotowa

Otrzymaj powiadomienie gdy sauna osiągnie ustawioną temperaturę:

```yaml
automation:
  - alias: "Sauna: Powiadomienie - gotowa"
    description: "Powiadom gdy sauna osiągnie temperaturę"
    trigger:
      - platform: template
        value_template: >
          {{ states('sensor.ffes_sauna_temperature')|float >= 
             states('sensor.ffes_sauna_target_temperature')|float }}
    condition:
      - condition: state
        entity_id: sensor.ffes_sauna_status
        state: "heating"
    action:
      - service: notify.mobile_app_twoj_telefon
        data:
          title: "🧖 Sauna gotowa!"
          message: "Sauna osiągnęła {{ states('sensor.ffes_sauna_temperature') }}°C"
          data:
            actions:
              - action: "OPEN_SAUNA"
                title: "Otwórz kontrolkę"
```

## 3. Tygodniowy harmonogram sauny

Automatyczne włączanie sauny w określone dni tygodnia:

```yaml
automation:
  - alias: "Sauna: Harmonogram tygodniowy"
    description: "Włącz saunę w środy i piątki o 18:00"
    trigger:
      - platform: time
        at: "18:00:00"
    condition:
      - condition: time
        weekday:
          - wed
          - fri
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

## 4. Automatyczne wyłączenie po czasie

Wyłącz saunę automatycznie po 2 godzinach:

```yaml
automation:
  - alias: "Sauna: Auto wyłączenie"
    description: "Wyłącz saunę po 2 godzinach"
    trigger:
      - platform: state
        entity_id: sensor.ffes_sauna_status
        to: "heating"
        for:
          hours: 2
    action:
      - service: button.press
        target:
          entity_id: button.ffes_sauna_turn_off
      - service: notify.mobile_app_twoj_telefon
        data:
          title: "Sauna wyłączona"
          message: "Sauna została automatycznie wyłączona po 2 godzinach"
```

## 5. Ostrzeżenie o wysokiej temperaturze

Otrzymuj alert gdy temperatura przekroczy bezpieczny poziom:

```yaml
automation:
  - alias: "Sauna: Ostrzeżenie - wysoka temperatura"
    description: "Alert gdy temperatura > 100°C"
    trigger:
      - platform: numeric_state
        entity_id: sensor.ffes_sauna_temperature
        above: 100
    action:
      - service: notify.mobile_app_twoj_telefon
        data:
          title: "⚠️ Sauna - Wysoka temperatura!"
          message: "Temperatura w saunie: {{ states('sensor.ffes_sauna_temperature') }}°C"
          data:
            tag: "sauna_temp_warning"
            priority: high
```

## 6. Integracja z Google Calendar

Włącz saunę na podstawie wpisu w kalendarzu:

```yaml
automation:
  - alias: "Sauna: Kalendarz - przygotowanie"
    description: "Włącz saunę 45 minut przed wydarzeniem"
    trigger:
      - platform: calendar
        entity_id: calendar.home_activities
        event: start
        offset: "-00:45:00"
    condition:
      - condition: template
        value_template: "{{ 'sauna' in trigger.calendar_event.summary|lower }}"
    action:
      - service: button.press
        target:
          entity_id: button.ffes_sauna_start_heating
```

## 7. Tryb nocny - automatyczne wyciszenie

Automatycznie zmniejsz intensywność w godzinach nocnych:

```yaml
automation:
  - alias: "Sauna: Tryb nocny"
    description: "Zmniejsz temperaturę wieczorem"
    trigger:
      - platform: time
        at: "22:00:00"
    condition:
      - condition: state
        entity_id: sensor.ffes_sauna_status
        state: "heating"
    action:
      - service: number.set_value
        target:
          entity_id: number.ffes_sauna_target_temperature
        data:
          value: 60
```

## 8. Inteligentne świecenie - synchronizacja z obecnością

Włącz światło gdy ktoś wchodzi do sauny:

```yaml
automation:
  - alias: "Sauna: Światło - detekcja ruchu"
    description: "Włącz światło gdy wykryto ruch"
    trigger:
      - platform: state
        entity_id: binary_sensor.sauna_motion
        to: "on"
    condition:
      - condition: not
        conditions:
          - condition: state
            entity_id: sensor.ffes_sauna_status
            state: "off"
    action:
      - service: switch.turn_on
        target:
          entity_id: switch.ffes_sauna_light
```

## 9. Sezonowe ustawienia

Dostosuj ustawienia sauny w zależności od pory roku:

```yaml
automation:
  - alias: "Sauna: Profil zimowy"
    description: "Wyższa temperatura zimą"
    trigger:
      - platform: state
        entity_id: sensor.ffes_sauna_status
        to: "heating"
    condition:
      - condition: template
        value_template: "{{ now().month in [12, 1, 2] }}"
    action:
      - service: number.set_value
        target:
          entity_id: number.ffes_sauna_target_temperature
        data:
          value: 90

  - alias: "Sauna: Profil letni"
    description: "Niższa temperatura latem"
    trigger:
      - platform: state
        entity_id: sensor.ffes_sauna_status
        to: "heating"
    condition:
      - condition: template
        value_template: "{{ now().month in [6, 7, 8] }}"
    action:
      - service: number.set_value
        target:
          entity_id: number.ffes_sauna_target_temperature
        data:
          value: 70
```

## 10. Dashboard z szybkim dostępem

Przykład karty Lovelace z pełną kontrolą:

```yaml
type: vertical-stack
cards:
  - type: glance
    title: Sauna - Stan
    entities:
      - entity: sensor.ffes_sauna_status
        name: Status
      - entity: sensor.ffes_sauna_temperature
        name: Temperatura
      - entity: sensor.ffes_sauna_humidity
        name: Wilgotność

  - type: entities
    title: Sterowanie
    entities:
      - entity: select.ffes_sauna_profile
        name: Profil
      - entity: number.ffes_sauna_target_temperature
        name: Temperatura docelowa
      - entity: number.ffes_sauna_humidity_setting
        name: Wilgotność

  - type: horizontal-stack
    cards:
      - type: button
        entity: button.ffes_sauna_start_heating
        name: Grzanie
        icon: mdi:fire
        tap_action:
          action: call-service
          service: button.press
          service_data:
            entity_id: button.ffes_sauna_start_heating
      
      - type: button
        entity: button.ffes_sauna_turn_off
        name: Wyłącz
        icon: mdi:power-off
        tap_action:
          action: call-service
          service: button.press
          service_data:
            entity_id: button.ffes_sauna_turn_off

  - type: entities
    title: Dodatkowo
    entities:
      - entity: switch.ffes_sauna_light
        name: Światło
      - entity: switch.ffes_sauna_aux
        name: AUX
```

## 11. Script - Szybkie presety

Stwórz skrypty dla różnych rodzajów sesji:

```yaml
script:
  sauna_quick_session:
    alias: "Sauna: Szybka sesja 45 min"
    sequence:
      - service: select.select_option
        target:
          entity_id: select.ffes_sauna_profile
        data:
          option: "Dry Sauna"
      - service: number.set_value
        target:
          entity_id: number.ffes_sauna_target_temperature
        data:
          value: 80
      - service: button.press
        target:
          entity_id: button.ffes_sauna_start_heating
      - delay: "00:45:00"
      - service: button.press
        target:
          entity_id: button.ffes_sauna_start_ventilation
      - delay: "00:15:00"
      - service: button.press
        target:
          entity_id: button.ffes_sauna_turn_off

  sauna_long_session:
    alias: "Sauna: Długa sesja relaksacyjna"
    sequence:
      - service: select.select_option
        target:
          entity_id: select.ffes_sauna_profile
        data:
          option: "Infrared Sauna"
      - service: number.set_value
        target:
          entity_id: number.ffes_sauna_target_temperature
        data:
          value: 65
      - service: switch.turn_on
        target:
          entity_id: switch.ffes_sauna_light
      - service: button.press
        target:
          entity_id: button.ffes_sauna_start_heating
```

## 12. Integracja z Alexa/Google Home

Stwórz skrypty, które możesz aktywować głosowo:

```yaml
script:
  sauna_voice_on:
    alias: "Włącz saunę"
    sequence:
      - service: button.press
        target:
          entity_id: button.ffes_sauna_start_heating
      - service: tts.google_translate_say
        data:
          entity_id: media_player.salon
          message: "Włączam saunę. Będzie gotowa za około 30 minut."

  sauna_voice_off:
    alias: "Wyłącz saunę"
    sequence:
      - service: button.press
        target:
          entity_id: button.ffes_sauna_turn_off
      - service: tts.google_translate_say
        data:
          entity_id: media_player.salon
          message: "Sauna została wyłączona."
```

Następnie możesz użyć tych skryptów w Alexa/Google Home przez Nabu Casa lub expose them directly.

---

Wszystkie te przykłady możesz dostosować do swoich potrzeb!
