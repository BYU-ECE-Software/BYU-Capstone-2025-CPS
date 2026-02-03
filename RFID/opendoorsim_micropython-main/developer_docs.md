# OpenDoorSim Developer Documentation

## Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [File Structure](#file-structure)
4. [Key Libraries](#key-libraries)
5. [Core Functions Reference](#core-functions-reference)
6. [Configuration](#configuration)
7. [Hardware Pinout](#hardware-pinout)
8. [Wiegand Protocol](#wiegand-protocol)
9. [Card Formats](#card-formats)
10. [Data Flow](#data-flow)
11. [Web Interface](#web-interface)
12. [MQTT Integration](#mqtt-integration)
13. [Extending the System](#extending-the-system)

---

## Project Overview

**OpenDoorSim** is an open-source RFID door access control system built with MicroPython for ESP32 microcontrollers. It reads access control cards via the Wiegand protocol and manages door access through user validation.

### Key Features

- Wiegand protocol support (26, 32, 34, 35, 37, 48-bit formats)
- Web-based management interface
- OLED and LCD display support
- MQTT integration for remote control (MRACS)
- Configurable access control with user database
- Special event triggers for custom actions

### Operation Modes

| Mode | Description |
|------|-------------|
| `raw` | Displays raw card data without access control checks |
| `doorsim` | Full access control with user validation and event handling |
| `accessory` | MQTT-only operation without local Wiegand reader |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        HARDWARE LAYER                        │
│  RFID Reader (Wiegand D0/D1) ──────→ GPIO21/GPIO22          │
│  I2C Display (LCD/OLED)      ──────→ GPIO18/GPIO19          │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────┐
│                    INTERRUPT LAYER                            │
│  d0_pulse_handler() ──→ Captures bit value 0                 │
│  d1_pulse_handler() ──→ Captures bit value 1                 │
│  (Fills wiegand_bit_array with incoming card data)           │
└──────────────────────┬───────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────┐
│                    MAIN EVENT LOOP                            │
│  - Monitors for card read completion (timeout detection)      │
│  - Processes card data when complete                          │
│  - Handles web server requests                                │
│  - Manages MQTT communication                                 │
└──────────────────────┬───────────────────────────────────────┘
                       │
        ┌──────────────┴──────────────┐
        ▼                             ▼
┌───────────────────┐      ┌───────────────────────┐
│ ACCESS CONTROL    │      │ EVENT HANDLING        │
│ process_card_data │      │ handle_special_events │
│ find_user         │      │ (door_open, lights,   │
│ grant/deny access │      │  buzzer, custom)      │
└───────────────────┘      └───────────────────────┘
        │                             │
        ▼                             ▼
┌───────────────────────────────────────────────────────────────┐
│                      OUTPUT LAYER                              │
│  LCD Display ←── Status messages                              │
│  OLED Display ←── Detailed information                        │
│  MQTT Broker ←── Card read events and status                  │
└───────────────────────────────────────────────────────────────┘
```

---

## File Structure

```
opendoorsim_micropython-main/
├── main.py           # Core application logic (~810 lines)
├── boot.py           # WiFi initialization and setup (~108 lines)
├── webserver.py      # Web management interface (~625 lines)
├── formats.py        # Wiegand card format definitions (~75 lines)
├── ssd1306.py        # OLED display driver (~120 lines)
├── lcd_i2c.py        # LCD display driver (~193 lines)
├── config.json       # System configuration
├── users.json        # Authorized users database
├── events.json       # Special event triggers
└── developer_docs.md # This documentation
```

### File Descriptions

| File | Purpose |
|------|---------|
| `main.py` | Core application: interrupt handlers, card processing, access control, main loop |
| `boot.py` | Runs on startup: initializes WiFi (AP or Station mode) |
| `webserver.py` | Non-blocking HTTP server for web-based management |
| `formats.py` | Defines Wiegand card formats with bit positions and parity rules |
| `ssd1306.py` | I2C driver for SSD1306 OLED displays (128x32) |
| `lcd_i2c.py` | I2C driver for character LCDs with PCF8574 backpack |
| `config.json` | Runtime configuration (pins, modes, MQTT settings) |
| `users.json` | Array of authorized users with FC, CN, name, and flags |
| `events.json` | Special event definitions triggered by specific cards |

---

## Key Libraries

### Built-in MicroPython Libraries

| Library | Usage |
|---------|-------|
| `machine` | GPIO pin control, I2C communication, interrupt handling |
| `network` | WiFi Access Point and Station configuration |
| `socket` | HTTP web server implementation |
| `json` | Configuration and data file parsing |
| `utime` | Timing functions for Wiegand protocol and timeouts |
| `framebuf` | Frame buffer for OLED display rendering |

### Custom Modules

| Module | Usage |
|--------|-------|
| `formats` | Wiegand format definitions (FC/CN bit positions, parity) |
| `ssd1306` | OLED display driver class |
| `lcd_i2c` | LCD display driver class |
| `webserver` | Non-blocking HTTP server functions |

### Optional External Libraries

| Library | Usage |
|---------|-------|
| `umqtt.simple` | Basic MQTT client for remote communication |
| `umqtt.robust` | Robust MQTT client with auto-reconnect |

---

## Core Functions Reference

### Interrupt Service Routines (main.py)

#### `d0_pulse_handler(pin)`
Handles falling edge interrupt on D0 pin (represents bit value 0).

```python
def d0_pulse_handler(pin):
    # Sets current bit to 0 in wiegand_bit_array
    # Increments current_bit_index
    # Updates last_pulse_time_microsec
```

#### `d1_pulse_handler(pin)`
Handles falling edge interrupt on D1 pin (represents bit value 1).

```python
def d1_pulse_handler(pin):
    # Sets current bit to 1 in wiegand_bit_array
    # Increments current_bit_index
    # Updates last_pulse_time_microsec
```

### Bit Manipulation Functions (main.py)

#### `set_bit_in_array(array, bit_index, value)`
Sets a specific bit in the byte array (MSB-first ordering).

| Parameter | Type | Description |
|-----------|------|-------------|
| `array` | bytearray | Target byte array |
| `bit_index` | int | Bit position (0-indexed from MSB) |
| `value` | int | Bit value (0 or 1) |

#### `get_bit_from_array(array, bit_index)`
Extracts a specific bit from the byte array.

| Parameter | Type | Description |
|-----------|------|-------------|
| `array` | bytearray | Source byte array |
| `bit_index` | int | Bit position to extract |
| **Returns** | int | Bit value (0 or 1) |

### Card Processing Functions (main.py)

#### `process_card_data(bit_array, bit_count)`
Main card parsing function. Extracts FC and CN based on configured format.

| Parameter | Type | Description |
|-----------|------|-------------|
| `bit_array` | bytearray | Raw card data bits |
| `bit_count` | int | Number of bits received |
| **Returns** | dict | Parsed card data with FC, CN, hex, binary, parity status |

**Return Dictionary Structure:**
```python
{
    "fc": int,           # Facility Code
    "cn": int,           # Card Number
    "hex": str,          # Hexadecimal representation
    "binary": str,       # Binary representation
    "parity_valid": bool,# Parity check result
    "format": str,       # Detected format name
    "bit_count": int     # Total bits received
}
```

#### `calculate_parity(bit_array, parity_spec)`
Validates parity bits according to format specification.

| Parameter | Type | Description |
|-----------|------|-------------|
| `bit_array` | bytearray | Card data bits |
| `parity_spec` | dict | Parity specification from format |
| **Returns** | bool | True if parity is valid |

#### `reset_wiegand_buffer()`
Clears the Wiegand bit array and resets the bit index for next card read.

### Access Control Functions (main.py)

#### `find_user(fc, cn)`
Searches the users database for a matching FC:CN combination.

| Parameter | Type | Description |
|-----------|------|-------------|
| `fc` | int | Facility Code |
| `cn` | int | Card Number |
| **Returns** | dict/None | User record if found, None otherwise |

#### `trigger_card_read_event(card_data)`
Main event handler called when a complete card read is detected.

| Parameter | Type | Description |
|-----------|------|-------------|
| `card_data` | dict | Parsed card data from `process_card_data()` |

**Behavior by Mode:**
- **RAW**: Displays card data without access checks
- **DOORSIM**: Validates user, grants/denies access, triggers events
- **ACCESSORY**: Publishes to MQTT only

#### `handle_access_granted(user, card_data)`
Called when a valid, active user is found.

| Parameter | Type | Description |
|-----------|------|-------------|
| `user` | dict | User record from users.json |
| `card_data` | dict | Parsed card data |

#### `handle_access_denied(reason, card_data)`
Called when access is denied.

| Parameter | Type | Description |
|-----------|------|-------------|
| `reason` | str | Denial reason ("unknown_card", "inactive", etc.) |
| `card_data` | dict | Parsed card data |

#### `handle_special_events(fc, cn)`
Checks events.json for matching FC:CN and executes defined actions.

| Parameter | Type | Description |
|-----------|------|-------------|
| `fc` | int | Facility Code |
| `cn` | int | Card Number |

**Supported Actions:**
- `door_open` - Activate door relay for specified duration
- `light_on` / `light_off` - Control lighting
- `buzzer_beep` - Sound buzzer
- Custom actions via MQTT publish

### MQTT Functions (main.py)

#### `init_mqtt()`
Initializes the MQTT client with configured broker settings.

#### `mqtt_connect()`
Establishes connection to the MQTT broker.

| **Returns** | bool | True if connection successful |

#### `mqtt_publish(topic, message)`
Publishes a message to the specified MQTT topic.

| Parameter | Type | Description |
|-----------|------|-------------|
| `topic` | str | MQTT topic (prefixed with MQTT_TOPIC_PREFIX) |
| `message` | str | Message payload |

#### `mqtt_subscribe(topic)`
Subscribes to an MQTT topic for incoming commands.

| Parameter | Type | Description |
|-----------|------|-------------|
| `topic` | str | MQTT topic to subscribe to |

#### `mqtt_callback(topic, message)`
Callback handler for incoming MQTT messages.

| Parameter | Type | Description |
|-----------|------|-------------|
| `topic` | bytes | Topic the message was received on |
| `message` | bytes | Message payload |

#### `mqtt_loop()`
Processes pending MQTT messages. Called periodically from main loop.

---

## Configuration

### config.json Structure

```json
{
    "MODE": "doorsim",
    "MRACS_ENABLED": false,
    "D0_PIN": 21,
    "D1_PIN": 22,
    "MAX_BITS": 96,
    "CARD_READ_TIMEOUT_MS": 200,
    "SCL_PIN": 18,
    "SDA_PIN": 19,
    "SCREEN_WIDTH": 128,
    "SCREEN_HEIGHT": 32,
    "OLED_FLIPPED": false,
    "MQTT_BROKER": "192.168.1.100",
    "MQTT_PORT": 1883,
    "MQTT_CLIENT_ID": "",
    "MQTT_USERNAME": "",
    "MQTT_PASSWORD": "",
    "MQTT_TOPIC_PREFIX": "opendoorsim"
}
```

### Configuration Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `MODE` | string | "doorsim" | Operation mode: "raw", "doorsim", "accessory" |
| `MRACS_ENABLED` | bool | false | Enable MQTT remote access control |
| `D0_PIN` | int | 21 | GPIO pin for Wiegand D0 line |
| `D1_PIN` | int | 22 | GPIO pin for Wiegand D1 line |
| `MAX_BITS` | int | 96 | Maximum bits to capture per card read |
| `CARD_READ_TIMEOUT_MS` | int | 200 | Timeout (ms) to detect end of card read |
| `SCL_PIN` | int | 18 | I2C clock pin for displays |
| `SDA_PIN` | int | 19 | I2C data pin for displays |
| `SCREEN_WIDTH` | int | 128 | OLED display width in pixels |
| `SCREEN_HEIGHT` | int | 32 | OLED display height in pixels |
| `OLED_FLIPPED` | bool | false | Flip OLED display orientation |
| `MQTT_BROKER` | string | "" | MQTT broker IP address |
| `MQTT_PORT` | int | 1883 | MQTT broker port |
| `MQTT_CLIENT_ID` | string | "" | MQTT client identifier |
| `MQTT_USERNAME` | string | "" | MQTT authentication username |
| `MQTT_PASSWORD` | string | "" | MQTT authentication password |
| `MQTT_TOPIC_PREFIX` | string | "opendoorsim" | Prefix for all MQTT topics |

### users.json Structure

```json
[
    {
        "FC": 123,
        "CN": 45678,
        "Name": "John Doe",
        "Flag": "",
        "active": true
    }
]
```

| Field | Type | Description |
|-------|------|-------------|
| `FC` | int | Facility Code |
| `CN` | int | Card Number |
| `Name` | string | User display name |
| `Flag` | string | CTF flag or notes (optional) |
| `active` | bool | Whether user has access |

### events.json Structure

```json
[
    {
        "FC": 99,
        "CN": 4944,
        "action": "door_open",
        "params": {
            "duration": 5
        }
    }
]
```

| Field | Type | Description |
|-------|------|-------------|
| `FC` | int | Facility Code to match |
| `CN` | int | Card Number to match |
| `action` | string | Action to execute |
| `params` | object | Action-specific parameters |

---

## Hardware Pinout

### Default GPIO Assignments

| Function | GPIO Pin | Description |
|----------|----------|-------------|
| Wiegand D0 | 21 | Data line 0 (bit value 0) |
| Wiegand D1 | 22 | Data line 1 (bit value 1) |
| I2C SCL | 18 | I2C clock for displays |
| I2C SDA | 19 | I2C data for displays |

### Wiegand Reader Connection

```
RFID Reader          ESP32
-----------          -----
D0 (Green)    ───→   GPIO21
D1 (White)    ───→   GPIO22
GND (Black)   ───→   GND
VCC (Red)     ───→   5V (or 12V depending on reader)
```

### I2C Display Connection

```
Display              ESP32
-------              -----
SCL           ───→   GPIO18
SDA           ───→   GPIO19
GND           ───→   GND
VCC           ───→   3.3V
```

---

## Wiegand Protocol

### Overview

The Wiegand protocol is a one-way communication standard used by RFID card readers. Data is transmitted over two lines (D0 and D1) using pulse-based signaling.

### Signal Characteristics

- **Idle State**: Both D0 and D1 are HIGH
- **Bit 0**: D0 pulses LOW for 20-100μs
- **Bit 1**: D1 pulses LOW for 20-100μs
- **Bit Interval**: 1-2ms between pulses
- **Card Read Complete**: No pulses for >50ms (configured as 200ms default)

### Timing Diagram

```
D0: ────┐  ┌────────────────┐  ┌────────
        └──┘                └──┘
           Bit 0              Bit 0

D1: ──────────────┐  ┌──────────────────
                  └──┘
                  Bit 1
```

### Implementation Details

1. **Interrupt-Driven Capture**: Both D0 and D1 are configured with falling-edge interrupts
2. **Bit Storage**: Bits are stored MSB-first in a byte array
3. **Timeout Detection**: Card read completion detected via configurable timeout
4. **Critical Sections**: IRQs disabled during data copy to prevent corruption

---

## Card Formats

### Supported Formats (formats.py)

| Format | Total Bits | FC Bits | FC Range | CN Bits | CN Range |
|--------|------------|---------|----------|---------|----------|
| 26-bit H10301 | 26 | 8 (1-8) | 0-255 | 16 (9-24) | 0-65535 |
| 32-bit ATS | 32 | 13 (1-13) | 0-8191 | 17 (14-30) | 0-131071 |
| 34-bit HID | 34 | 16 (1-16) | 0-65535 | 16 (17-32) | 0-65535 |
| 35-bit Corp1000 | 35 | 12 (2-13) | 0-4095 | 20 (14-33) | 0-1048575 |
| 37-bit H10302 | 37 | 0 | N/A | 35 (1-35) | 0-34359738367 |
| 48-bit Corp1000 | 48 | 22 (2-23) | 0-4194303 | 23 (24-46) | 0-8388607 |

### Format Definition Structure

```python
WIEGAND_FORMATS = {
    26: {
        "name": "STANDARD 26-bit (H10301)",
        "fc_bits": (1, 8),      # Start bit, length
        "cn_bits": (9, 16),     # Start bit, length
        "parity": {
            "even": {"bit": 0, "range": (1, 12)},
            "odd": {"bit": 25, "range": (13, 24)}
        }
    },
    # ... additional formats
}
```

### Parity Calculation

- **Even Parity**: Parity bit + data bits should have even number of 1s
- **Odd Parity**: Parity bit + data bits should have odd number of 1s

```
26-bit Example:
Bit 0 (Even Parity) covers bits 1-12
Bit 25 (Odd Parity) covers bits 13-24

P | FC (8 bits) | CN (16 bits) | P
0 | 1-8         | 9-24         | 25
```

---

## Data Flow

### Card Read Sequence

```
1. Card presented to reader
           │
           ▼
2. Reader sends Wiegand pulses
           │
           ▼
3. ISRs capture bits into wiegand_bit_array
   - d0_pulse_handler() for 0 bits
   - d1_pulse_handler() for 1 bits
           │
           ▼
4. Main loop detects timeout (no pulses for 200ms)
           │
           ▼
5. IRQs disabled, data copied to processing buffer
           │
           ▼
6. process_card_data() extracts FC/CN
   - Determines format from bit count
   - Extracts FC from configured bit positions
   - Extracts CN from configured bit positions
   - Validates parity
           │
           ▼
7. trigger_card_read_event() handles result
           │
     ┌─────┴─────┐
     ▼           ▼
8a. RAW Mode    8b. DOORSIM Mode
    Display         find_user()
    raw data            │
                   ┌────┴────┐
                   ▼         ▼
               Found     Not Found
               check     deny access
               active        │
                   │         ▼
              ┌────┴────┐   Display
              ▼         ▼   "Unknown"
           Active    Inactive
           grant     deny access
           access         │
              │           ▼
              ▼      Display
         Display     "Inactive"
         "Granted"
              │
              ▼
9. handle_special_events() checks events.json
           │
           ▼
10. Execute matching actions (door_open, etc.)
           │
           ▼
11. MQTT publish (if MRACS enabled)
           │
           ▼
12. Reset buffer for next card
```

---

## Web Interface

### Accessing the Interface

1. Connect to WiFi AP: `opendoorsim` (password: `shortrange`)
2. Navigate to: `http://192.168.4.1`

### HTTP Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Main dashboard (HTML) |
| POST | `/save_users` | Update users.json |
| POST | `/save_events` | Update events.json |
| POST | `/save_config` | Update config.json |
| POST | `/reboot` | Reboot the device |

### Dashboard Tabs

1. **Home**: System status, current configuration, last 25 card reads
2. **Users**: Manage authorized users (add/edit/delete)
3. **Events**: Configure special event triggers
4. **Config**: Modify system settings

### webserver.py Key Functions

#### `start_server_non_blocking()`
Initializes the HTTP server socket without blocking the main loop.

#### `process_requests()`
Handles one HTTP request per call. Called from main loop at ~100ms intervals.

#### `generate_full_html()`
Generates the complete HTML dashboard with embedded CSS and JavaScript.

---

## MQTT Integration

### Topic Structure

All topics are prefixed with `MQTT_TOPIC_PREFIX` (default: "opendoorsim").

| Topic | Direction | Description |
|-------|-----------|-------------|
| `{prefix}/card_read` | Publish | Card read events |
| `{prefix}/access` | Publish | Access granted/denied events |
| `{prefix}/status` | Publish | System status updates |
| `{prefix}/command` | Subscribe | Incoming commands |

### Card Read Message Format

```json
{
    "fc": 123,
    "cn": 45678,
    "format": "26-bit H10301",
    "access": "granted",
    "user": "John Doe",
    "timestamp": 1234567890
}
```

### Command Message Format

```json
{
    "action": "door_open",
    "params": {
        "duration": 5
    }
}
```

### Enabling MQTT

1. Set `MRACS_ENABLED` to `true` in config.json
2. Configure `MQTT_BROKER` with broker IP address
3. Optionally set authentication credentials
4. Reboot the device

---

## Extending the System

### Adding a New Card Format

1. Edit `formats.py`
2. Add new format to `WIEGAND_FORMATS` dictionary:

```python
WIEGAND_FORMATS[40] = {
    "name": "Custom 40-bit Format",
    "fc_bits": (1, 16),      # FC starts at bit 1, 16 bits long
    "cn_bits": (17, 22),     # CN starts at bit 17, 22 bits long
    "parity": {
        "even": {"bit": 0, "range": (1, 19)},
        "odd": {"bit": 39, "range": (20, 38)}
    }
}
```

### Adding a New Event Action

1. Edit the `handle_special_events()` function in `main.py`
2. Add a new action handler:

```python
elif action == "custom_action":
    param1 = params.get("param1", default_value)
    # Implement custom action logic
    print(f"Executing custom action with {param1}")
```

3. Add event to `events.json`:

```json
{
    "FC": 100,
    "CN": 12345,
    "action": "custom_action",
    "params": {
        "param1": "value"
    }
}
```

### Adding a New Display Type

1. Create a new driver file (e.g., `new_display.py`)
2. Implement required methods:
   - `__init__(i2c, addr)`
   - `print(text)` or `text(text, x, y)`
   - `clear()`
   - `show()` (if buffered)

3. Import and initialize in `main.py`:

```python
from new_display import NewDisplay
display = NewDisplay(i2c, 0x27)
```

### Adding New Web Endpoints

1. Edit `webserver.py`
2. Add route handling in `process_requests()`:

```python
elif path == "/new_endpoint" and method == "POST":
    # Parse request body
    data = json.loads(body)
    # Process data
    result = process_new_endpoint(data)
    # Send response
    send_json_response(client, result)
```

---

## Troubleshooting

### Common Issues

| Issue | Possible Cause | Solution |
|-------|----------------|----------|
| No card reads | Wiring incorrect | Check D0/D1 connections |
| Partial reads | Timeout too short | Increase `CARD_READ_TIMEOUT_MS` |
| Parity errors | Format mismatch | Verify card format matches config |
| Display blank | I2C address wrong | Scan I2C bus for correct address |
| Web unreachable | Not connected to AP | Connect to `opendoorsim` WiFi |
| MQTT not connecting | Broker unreachable | Verify broker IP and port |

### Debug Output

Enable debug output by adding print statements in `main.py`:

```python
# In process_card_data()
print(f"Raw bits: {bit_count}")
print(f"Binary: {binary_str}")
print(f"FC: {fc}, CN: {cn}")
```

### I2C Bus Scan

```python
from machine import Pin, I2C
i2c = I2C(0, scl=Pin(18), sda=Pin(19))
devices = i2c.scan()
print(f"I2C devices found: {[hex(d) for d in devices]}")
```

---

## License

OpenDoorSim is open-source software. See the project repository for license details.

## Credits

Developed by shortrange.tech
