# Instrukcja Instalacji FFES Sauna dla Home Assistant

## Wymagania

- Home Assistant w wersji 2023.1.0 lub nowszej
- HACS (Home Assistant Community Store) zainstalowany
- Sterownik sauny FFES z dostępem do sieci
- Znany adres IP sterownika sauny

## Metoda 1: Instalacja przez HACS (Zalecana)

### Krok 1: Dodanie niestandardowego repozytorium

1. Otwórz Home Assistant
2. Przejdź do **HACS** w menu bocznym
3. Kliknij **Integracje**
4. Kliknij trzy kropki w prawym górnym rogu
5. Wybierz **Niestandardowe repozytoria**
6. Wklej URL: `https://github.com/LeszekWroblowski/ffes_sauna_home_assistant`
7. Wybierz kategorię: **Integracja**
8. Kliknij **Dodaj**

### Krok 2: Instalacja integracji

1. Wyszukaj "FFES Sauna Control" w HACS
2. Kliknij **Pobierz**
3. Kliknij **Pobierz** ponownie w oknie dialogowym
4. Zrestartuj Home Assistant

### Krok 3: Konfiguracja

1. Przejdź do **Ustawienia** → **Urządzenia i usługi**
2. Kliknij **+ Dodaj integrację**
3. Wyszukaj "FFES Sauna"
4. Wprowadź adres IP sterownika (np. `192.168.0.208`)
5. Kliknij **Wyślij**

✅ Gotowe! Integracja jest skonfigurowana.

## Metoda 2: Instalacja ręczna

### Krok 1: Pobranie plików

1. Pobierz najnowszą wersję z [GitHub](https://github.com/LeszekWroblowski/ffes_sauna_home_assistant/releases)
2. Rozpakuj archiwum

### Krok 2: Kopiowanie plików

1. Połącz się z Home Assistant przez SSH lub Samba
2. Przejdź do katalogu `config`
3. Utwórz folder `custom_components` (jeśli nie istnieje)
4. Skopiuj folder `ffes_sauna` do `config/custom_components/`

Struktura powinna wyglądać tak:
```
config/
└── custom_components/
    └── ffes_sauna/
        ├── __init__.py
        ├── manifest.json
        ├── config_flow.py
        ├── coordinator.py
        ├── sensor.py
        ├── switch.py
        ├── button.py
        ├── select.py
        ├── number.py
        ├── const.py
        ├── strings.json
        └── translations/
            ├── en.json
            └── pl.json
```

### Krok 3: Restart i konfiguracja

1. Zrestartuj Home Assistant
2. Przejdź do **Ustawienia** → **Urządzenia i usługi**
3. Kliknij **+ Dodaj integrację**
4. Wyszukaj "FFES Sauna"
5. Wprowadź adres IP sterownika
6. Kliknij **Wyślij**

## Weryfikacja instalacji

Po pomyślnej instalacji powinieneś zobaczyć:

### Encje (Entities):
- 9 sensorów (temperatura, wilgotność, status, itp.)
- 2 przełączniki (światło, AUX)
- 4 przyciski (wyłącz, grzanie, wentylacja, standby)
- 1 wybór (profil sauny)
- 2 kontrolki liczbowe (temperatura docelowa, wilgotność)

### Urządzenie (Device):
- **Nazwa**: FFES Sauna
- **Producent**: FFES
- **Model**: Sauna Controller

## Testowanie połączenia

### Test 1: Sprawdź sensory
1. Przejdź do **Narzędzia deweloperskie** → **Stany**
2. Wyszukaj `sensor.ffes_sauna_temperature`
3. Sprawdź czy pokazuje aktualną temperaturę

### Test 2: Przetestuj przycisk
1. Znajdź `button.ffes_sauna_start_heating`
2. Kliknij **Wywołaj usługę**
3. Sprawdź czy sauna zaczyna się grzać

## Rozwiązywanie problemów

### Nie można połączyć
```bash
# Sprawdź czy sterownik odpowiada
ping 192.168.0.208

# Sprawdź czy endpoint działa
curl http://192.168.0.208/sauna-data
```

### Brak encji
1. Sprawdź logi: **Ustawienia** → **System** → **Logi**
2. Wyszukaj "ffes_sauna"
3. Usuń integrację i dodaj ponownie

### Encje się nie aktualizują
1. Sprawdź logi pod kątem błędów połączenia
2. Zweryfikuj że sterownik jest włączony
3. Sprawdź konfigurację sieci

## Aktualizacja

### Przez HACS
1. Otwórz HACS → Integracje
2. Znajdź "FFES Sauna Control"
3. Kliknij **Aktualizuj**
4. Zrestartuj Home Assistant

### Ręcznie
1. Pobierz nową wersję
2. Zastąp pliki w `custom_components/ffes_sauna`
3. Zrestartuj Home Assistant

## Wsparcie

Potrzebujesz pomocy?
- 📖 Przeczytaj [README](README.md)
- 🐛 Zgłoś problem na [GitHub Issues](https://github.com/LeszekWroblowski/ffes_sauna_home_assistant/issues)
- 💬 Dołącz do dyskusji na [Home Assistant Community](https://community.home-assistant.io/)
