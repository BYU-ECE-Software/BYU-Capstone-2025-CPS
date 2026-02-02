import time

from machine import Pin, I2C
from lcd_i2c import LCD_I2C #We might have to change where the pins are
import machine
import utime
import micropython
import json
import network
import ssd1306 # Import OLED driver
import formats # Import Wiegand formats
import webserver # Import web server

# --- Global Wiegand Variables ---
wiegand_bit_array = None
current_bit_index = 0
last_pulse_time_microsec = 0
pin_d0 = None
pin_d1 = None
micropython.alloc_emergency_exception_buf(100) # For ISR exceptions

# --- Global OLED Variable ---
display = None

# --- Configuration and Users ---
config = None
users = None
events = None

# --- Configuration Loading Functions ---

# Initialize I2C
# Default ESP32 pins: SDA=GPIO21, SCL=GPIO22
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)

# Initialize LCD
# Common addresses are 0x27 or 0x3F
# Change if your LCD has a different address
lcd = LCD_I2C(i2c, addr=0x27, cols=16, rows=2)

def load_config():
    """Loads configuration from config.json file."""
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading config.json: {e}")
        lcd.print(f"Error loading config.json: {e}")
        time.sleep(5)
        lcd.clear()
        # Return default config if file can't be loaded
        return {
            "D0_PIN": 21,
            "D1_PIN": 22,
            "MAX_BITS": 96,
            "CARD_READ_TIMEOUT_MS": 50,
            "SCL_PIN": 18,
            "SDA_PIN": 19,
            "SCREEN_WIDTH": 128,
            "SCREEN_HEIGHT": 32,
            "OLED_FLIPPED": False
        }

def load_users():
    """Loads users from users.json file."""
    try:
        with open('users.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading users.json: {e}")
        lcd.print(f"Error loading users.json: {e}")
        time.sleep(5)
        lcd.clear()
        return []

def load_events():
    """Loads events from events.json file."""
    try:
        with open('events.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading events.json: {e}")
        lcd.print(f"Error loading events.json: {e}")
        time.sleep(5)
        lcd.clear()
        return []

# --- Wiegand Bit Array Helpers ---

def set_bit_in_array(bit_position, value):
    """Sets a bit (0 or 1) at a given position in the wiegand_bit_array."""
    # This function is ONLY called by ISRs and always acts on the global buffer
    byte_index = bit_position // 8
    bit_in_byte_offset = 7 - (bit_position % 8) # Store MSB first
    if byte_index < len(wiegand_bit_array):
        if value:
            wiegand_bit_array[byte_index] |= (1 << bit_in_byte_offset)
        else:
            wiegand_bit_array[byte_index] &= ~(1 << bit_in_byte_offset)

def get_bit_from_array(buffer, bit_position):
    """
    Gets a bit (0 or 1) from a given position in the *specified* buffer.
    FIX: Now takes a 'buffer' argument to prevent race conditions.
    """
    byte_index = bit_position // 8
    bit_in_byte_offset = 7 - (bit_position % 8)
    if byte_index < len(buffer):
        return (buffer[byte_index] >> bit_in_byte_offset) & 1
    return None

def reset_wiegand_buffer():
    """Clears the buffer and resets counters for the next card read."""
    # This function is called from within a critical (IRQ-disabled) section
    global current_bit_index, last_pulse_time_microsec
    for i in range(len(wiegand_bit_array)):
        wiegand_bit_array[i] = 0
    current_bit_index = 0

# --- Interrupt Service Routines (ISRs) ---

def d0_pulse_handler(pin_obj):
    """Handles a pulse on the D0 line (bit value 0)."""
    global current_bit_index, last_pulse_time_microsec, config
    # This code runs in an interrupt and must be very fast
    if current_bit_index < config['MAX_BITS']:
        set_bit_in_array(current_bit_index, 0)
        current_bit_index += 1
    last_pulse_time_microsec = utime.ticks_us()

def d1_pulse_handler(pin_obj):
    """Handles a pulse on the D1 line (bit value 1)."""
    global current_bit_index, last_pulse_time_microsec, config
    # This code runs in an interrupt and must be very fast
    if current_bit_index < config['MAX_BITS']:
        set_bit_in_array(current_bit_index, 1)
        current_bit_index += 1
    last_pulse_time_microsec = utime.ticks_us()

# --- OLED Helper Functions ---
# (No changes needed)
# def lcd.print(line1, line2="", line3="", line4=""):
#     """Helper to clear and write text to the OLED."""
#     global display, config
#     if display:
#         display.fill(0) # Clear the screen
#         display.text(line1, 0, 0)
#         display.text(line2, 0, 8) # 8 pixels per line
#         if config['SCREEN_HEIGHT'] > 32:
#             display.text(line3, 0, 16)
#             display.text(line4, 0, 24)
#         display.show()

# --- Peripheral Control Functions (Placeholders) ---
# (No changes needed)
def door_open(duration=5):
    """Placeholder for door control - opens door for specified duration in seconds."""
    print(f"[PLACEHOLDER] Door open for {duration} seconds")

def door_close():
    """Placeholder for door control - closes door."""
    print("[PLACEHOLDER] Door close")

def light_on(light_id, duration=10):
    """Placeholder for light control - turns on light for specified duration in seconds."""
    print(f"[PLACEHOLDER] Light {light_id} on for {duration} seconds")

def light_off(light_id):
    """Placeholder for light control - turns off light."""
    print(f"[PLACEHOLDER] Light {light_id} off")

def buzzer_beep(count=1, duration=100):
    """Placeholder for buzzer control - beeps specified number of times."""
    print(f"[PLACEHOLDER] Buzzer beep {count} time(s), {duration}ms each")

# --- MQTT Functions (Full Implementation) ---
# (No changes needed in these functions)
mqtt_client = None
mqtt_connected = False
device_id = None

def get_device_id():
    """Get unique device ID (MAC address)."""
    global device_id
    if device_id is None:
        import network
        import ubinascii
        ap = network.WLAN(network.AP_IF)
        if ap.active():
            mac = ap.config('mac')
        else:
            sta = network.WLAN(network.STA_IF)
            if sta.active():
                mac = sta.config('mac')
            else:
                mac = b'\x00' * 6
        device_id = ubinascii.hexlify(mac).decode('utf-8')
    return device_id

def init_mqtt():
    """Initialize MQTT connection."""
    global mqtt_client, mqtt_connected, config
    try:
        try:
            from umqtt.simple import MQTTClient
        except ImportError:
            try:
                from umqtt.robust import MQTTClient
            except ImportError:
                print("[MQTT] umqtt library not found. Install with: upip install micropython-umqtt.simple")
                mqtt_client = None
                mqtt_connected = False
                return
        
        broker = config.get('MQTT_BROKER', '192.168.1.100')
        port = config.get('MQTT_PORT', 1883)
        client_id = config.get('MQTT_CLIENT_ID', '')
        if not client_id:
            client_id = f"opendoorsim_{get_device_id()[:8]}"
        
        username = config.get('MQTT_USERNAME', '')
        password = config.get('MQTT_PASSWORD', '')
        
        mqtt_client = MQTTClient(client_id, broker, port, username, password, keepalive=60)
        mqtt_connected = False
        print(f"[MQTT] Initialized with broker {broker}:{port}, client_id: {client_id}")
    except Exception as e:
        print(f"[MQTT] Error initializing: {e}")
        mqtt_client = None
        mqtt_connected = False

def mqtt_connect():
    """Connect to MQTT broker."""
    global mqtt_client, mqtt_connected, config
    if mqtt_client is None:
        return False
    
    try:
        mqtt_client.connect()
        mqtt_connected = True
        
        topic_prefix = config.get('MQTT_TOPIC_PREFIX', 'opendoorsim')
        device_id = get_device_id()
        
        command_topic = f"{topic_prefix}/{device_id}/command"
        mqtt_client.set_callback(mqtt_on_message)
        mqtt_client.subscribe(command_topic.encode())
        print(f"[MQTT] Subscribed to {command_topic}")
        
        broadcast_topic = f"{topic_prefix}/broadcast"
        mqtt_client.subscribe(broadcast_topic.encode())
        print(f"[MQTT] Subscribed to {broadcast_topic}")
        
        print("[MQTT] Connected successfully")
        return True
    except Exception as e:
        print(f"[MQTT] Connection failed: {e}")
        mqtt_connected = False
        return False

def mqtt_on_message(topic, message):
    """Callback for MQTT messages."""
    try:
        topic_str = topic.decode('utf-8') if isinstance(topic, bytes) else topic
        message_str = message.decode('utf-8') if isinstance(message, bytes) else message
        mqtt_callback(topic_str, message_str)
    except Exception as e:
        print(f"[MQTT] Error in message callback: {e}")

def mqtt_publish(topic, message):
    """Publish message to MQTT topic."""
    global mqtt_client, mqtt_connected
    if not mqtt_connected or mqtt_client is None:
        return False
    
    try:
        if isinstance(message, dict):
            import json
            message = json.dumps(message)
        elif not isinstance(message, (str, bytes)):
            message = str(message)
        
        if isinstance(message, str):
            message = message.encode('utf-8')
        if isinstance(topic, str):
            topic = topic.encode('utf-8')
        
        mqtt_client.publish(topic, message)
        return True
    except Exception as e:
        print(f"[MQTT] Publish error: {e}")
        mqtt_connected = False
        return False

def mqtt_subscribe(topic):
    """Subscribe to MQTT topic."""
    global mqtt_client, mqtt_connected
    if not mqtt_connected or mqtt_client is None:
        return False
    
    try:
        if isinstance(topic, str):
            topic = topic.encode('utf-8')
        mqtt_client.subscribe(topic)
        print(f"[MQTT] Subscribed to {topic.decode('utf-8')}")
        return True
    except Exception as e:
        print(f"[MQTT] Subscribe error: {e}")
        return False

def mqtt_callback(topic, message):
    """Handle incoming MQTT messages."""
    print(f"[MQTT] Received message on {topic}: {message}")
    
    try:
        if ':' in str(message):
            parts = str(message).split(':')
            if len(parts) == 2:
                fc = int(parts[0].strip())
                cn = int(parts[1].strip())
                print(f"[MQTT] Parsed as FC:CN - FC:{fc} CN:{cn}")
                handle_special_events(fc, cn)
                return
        
        event_code = int(str(message).strip())
        print(f"[MQTT] Parsed as event code - FC:-1 CN:{event_code}")
        handle_special_events(-1, event_code)
        
    except ValueError as e:
        print(f"[MQTT] Error parsing message '{message}': {e}")
    except Exception as e:
        print(f"[MQTT] Error handling message: {e}")

def mqtt_loop():
    """Process MQTT messages."""
    global mqtt_client, mqtt_connected
    if not mqtt_connected or mqtt_client is None:
        return
    
    try:
        mqtt_client.check_msg()
    except Exception as e:
        print(f"[MQTT] Error in loop: {e}")
        mqtt_connected = False
        utime.sleep(1)
        mqtt_connect()

# --- Wiegand Processing Functions ---

def calculate_parity(buffer, bit_positions_to_check, parity_type='Even'):
    """
    Calculates the parity for a given list of specific bit positions.
    FIX: Now takes a 'buffer' argument to read from.
    """
    count_of_ones = 0
    for bit_pos in bit_positions_to_check:
        bit_value = get_bit_from_array(buffer, bit_pos) # FIX: Pass buffer
        if bit_value is None:
            return None # Indicates a failure
        if bit_value == 1:
            count_of_ones += 1

    if parity_type == 'Even':
        return 0 if (count_of_ones % 2) == 0 else 1
    elif parity_type == 'Odd':
        return 1 if (count_of_ones % 2) == 0 else 0
    return None

def process_card_data(bits_received, data_buffer):
    """
    Processes the received Wiegand data using the formats dictionary.
    Returns a dictionary with the results.
    FIX: Now takes a 'data_buffer' argument to read from.
    """
    raw_bits_str = ""
    result = {
        "bits": bits_received,
        "name": "Unknown",
        "fc": -1,
        "cn": -1,
        "parity_ok": False,
        "raw_hex": ""
    }

    if bits_received == 0:
        print("[ERROR] No bits received.")
        lcd.print("[ERROR] No bits received.")
        return None

    # Build raw bit string for hex conversion
    full_binary_string = ""
    for i in range(bits_received):
        full_binary_string += str(get_bit_from_array(data_buffer, i)) # FIX: Pass data_buffer
    
    try:
        hex_value = int(full_binary_string, 2)
        result["raw_hex"] = f"0x{hex_value:X}"
    except ValueError:
        result["raw_hex"] = "Error"
        
    print(f"\n--- Card Swipe Detected ({bits_received} bits) ---")
    print(f"Binary: {full_binary_string}")
    print(f"Hex:    {result['raw_hex']}")

    format_info = formats.WIEGAND_FORMATS.get(bits_received)
    
    if not format_info:
        print(f"Format: Unknown. No format defined for {bits_received}-bit.")
        print("-----------------------------")
        return result # Return partial result

    result["name"] = format_info['name']
    print(f"Format: {result['name']}")

    # 1. Extract Facility Code
    fc_start = format_info['facility_code'].get('start', -1)
    fc_end = format_info['facility_code'].get('end', -1)
    
    if fc_start != -1:
        current_fc = 0
        for i in range(fc_start, fc_end + 1):
            bit = get_bit_from_array(data_buffer, i) # FIX: Pass data_buffer
            current_fc = (current_fc << 1) | bit
        result["fc"] = current_fc
        print(f"FC: {result['fc']}")
    else:
        print("FC: (Not defined for this format)")

    # 2. Extract Card Number
    cn_start = format_info['card_number']['start']
    cn_end = format_info['card_number']['end']
    current_cn = 0
    for i in range(cn_start, cn_end + 1):
        bit = get_bit_from_array(data_buffer, i) # FIX: Pass data_buffer
        current_cn = (current_cn << 1) | bit
    result["cn"] = current_cn
    print(f"CN: {result['cn']}")

    # 3. Do Parity Checks
    all_parity_ok = True
    if format_info['parity_checks']:
        for p_check in format_info['parity_checks']:
            actual_parity_bit_pos = p_check['parity_bit_pos']
            data_bits_for_parity = p_check['data_bits']
            parity_type = p_check['type']

            actual_parity_value = get_bit_from_array(data_buffer, actual_parity_bit_pos) # FIX: Pass data_buffer
            calculated_parity_value = calculate_parity(data_buffer, data_bits_for_parity, parity_type) # FIX: Pass data_buffer

            if actual_parity_value != calculated_parity_value:
                all_parity_ok = False
                print(f"  {parity_type} Parity (Bit {actual_parity_bit_pos}): FAIL (Actual={actual_parity_value}, Calc={calculated_parity_value})")
        
        result["parity_ok"] = all_parity_ok
        print(f"Parity: {'PASS' if all_parity_ok else 'FAIL'}")
    else:
        print("Parity: (No checks defined)")
        result["parity_ok"] = True # No checks to fail

    print("-----------------------------")
    return result

# --- Raw Mode Handler ---

def handle_raw_mode(result, data_buffer):
    """
    Handles raw mode card reading - displays raw data without access control.
    FIX: Now takes a 'data_buffer' argument to read from.
    """
    if not result:
        return
    
    # TODO: Add to card history for web interface
    # webserver.add_card_to_history(result)
    
    # Console output
    print(f"\n--- Raw Mode Card Read ---")
    print(f"Format: {result['name']}")
    if result['fc'] != -1:
        print(f"FC: {result['fc']}")
    else:
        print("FC: (Not defined for this format)")
    print(f"CN: {result['cn']}")
    print(f"Hex: {result['raw_hex']}")
    print(f"Parity: {'PASS' if result['parity_ok'] else 'FAIL'}")
    
    # Build binary string for display
    full_binary_string = ""
    for i in range(result['bits']):
        full_binary_string += str(get_bit_from_array(data_buffer, i)) # FIX: Pass data_buffer
    print(f"Binary: {full_binary_string}")
    print("-----------------------------")
    
    # OLED output
    oled_line_1 = f"FC: {result['fc']}" if result['fc'] != -1 else "FC: N/A"
    oled_line_2 = f"CN: {result['cn']}"
    oled_line_3 = result['raw_hex']
    oled_line_4 = f"Parity: {'PASS' if result['parity_ok'] else 'FAIL'}"
    lcd.print(oled_line_1, oled_line_2, oled_line_3, oled_line_4)

# --- Access Control Functions ---
# (No changes needed)
def find_user(fc, cn):
    """Searches users list for matching FC and CN. Returns user dict or None."""
    global users
    if users is None:
        return None
    
    for user in users:
        if fc == -1:
            if user.get('CN') == cn:
                return user
        else:
            if user.get('FC') == fc and user.get('CN') == cn:
                return user
    return None

def handle_access_granted(user):
    """Displays 'Access Granted' message with user name on OLED."""
    print(f"Access Granted: {user.get('Name', 'Unknown')}")
    lcd.print("Access Granted", user.get('Name', 'Unknown'), "", "")
    if user.get('Flag'):
        print(f"Flag: {user.get('Flag')}")

def handle_access_denied(reason, fc, cn):
    """Displays 'Access Denied' message with reason on OLED."""
    print(f"Access Denied: {reason}")
    if fc != -1:
        lcd.print("Access Denied", reason, f"FC: {fc} CN: {cn}", "")
    else:
        lcd.print("Access Denied", reason, f"CN: {cn}", "")

# --- Special Event Handler ---
# (No changes needed)
def handle_special_events(fc, cn):
    """
    Checks events.json for matching FC+CN and executes corresponding actions.
    """
    global events
    if events is None:
        return False
    
    for event in events:
        event_fc = event.get('FC')
        event_cn = event.get('CN')
        action = event.get('action')
        params = event.get('params', {})
        
        fc_match = (event_fc is None) or (event_fc == fc)
        cn_match = (event_cn is None) or (event_cn == cn)
        
        if fc_match and cn_match:
            print(f"Special event triggered: {action} for FC:{fc} CN:{cn}")
            
            if action == "door_open":
                door_open(params.get('duration', 5))
            elif action == "door_close":
                door_close()
            elif action == "light_on":
                light_on(params.get('light_id', 1), params.get('duration', 10))
            elif action == "light_off":
                light_off(params.get('light_id', 1))
            elif action == "buzzer_beep":
                buzzer_beep(params.get('count', 1), params.get('duration', 100))
            else:
                print(f"Unknown action: {action}")
            
            return True  # Event was handled
    
    return False  # No matching event found

# --- Main Event Handler ---
# (No changes needed)
def trigger_card_read_event(fc, cn, card_data):
    """
    Main event handler for card read events.
    """
    global config
    
    # TODO: Add to card history for web interface
    # webserver.add_card_to_history(card_data)
    
    special_event_triggered = handle_special_events(fc, cn)
    user = find_user(fc, cn)
    
    access_granted = False
    if user is None:
        handle_access_denied("Unknown User", fc, cn)
    elif not user.get('active', False):
        handle_access_denied("Card Disabled", fc, cn)
    else:
        handle_access_granted(user)
        access_granted = True
    
    if config.get('MRACS_ENABLED', False):
        topic_prefix = config.get('MQTT_TOPIC_PREFIX', 'opendoorsim')
        device_id = get_device_id()
        card_read_topic = f"{topic_prefix}/{device_id}/card_read"
        
        mqtt_message = {
            'fc': fc,
            'cn': cn,
            'bits': card_data.get('bits', 0),
            'hex': card_data.get('raw_hex', ''),
            'format': card_data.get('name', 'Unknown'),
            'parity_ok': card_data.get('parity_ok', False),
            'access_granted': access_granted,
            'user_name': user.get('Name', '') if user else '',
            'timestamp': utime.time()
        }
        
        mqtt_publish(card_read_topic, mqtt_message)

# --- Main ---
def main():
    global pin_d0, pin_d1, display, config, users, events, wiegand_bit_array
    
    print("Loading configuration...")
    lcd.print("Loading configuration...")
    config = load_config()
    users = load_users()
    events = load_events()
    
    mode = config.get('MODE', 'doorsim').lower()
    mracs_enabled = config.get('MRACS_ENABLED', False)
    print(f"System Mode: {mode.upper()}")
    lcd.print(f"System Mode: {mode.upper()}")
    print(f"MRACS Enabled: {mracs_enabled}")
    print(f"Loaded {len(users)} users from users.json")
    print(f"Loaded {len(events)} events from events.json")
    
    if mode not in ['raw', 'doorsim', 'accessory']:
        print(f"Warning: Invalid MODE '{mode}', defaulting to 'doorsim'")
        lcd.print(f"Warning: Invalid MODE '{mode}', defaulting to 'doorsim'")
        mode = 'doorsim'
    
    ap = network.WLAN(network.AP_IF)
    should_start_webserver = False
    if ap.active():
        should_start_webserver = True
        print("Access Point active - starting web server")
        webserver.start_server_non_blocking()
    
    if mode != 'accessory':
        wiegand_bit_array = bytearray(config['MAX_BITS'] // 8 + 1)
    
    if mracs_enabled and mode in ['doorsim', 'accessory']:
        print("Initializing MQTT (MRACS enabled)...")
        init_mqtt()
        if not mqtt_connect():
            print("MQTT connection failed - will retry")
            lcd.print("MQTT connection failed - will retry")
    else:
        print("MQTT disabled (MRACS not enabled or wrong mode)")
    
    print("OLED Display Initializing...")
    print(f"OLED SCL Pin: {config['SCL_PIN']}, SDA Pin: {config['SDA_PIN']}")
    
    try:
        i2c = I2C(0, scl=Pin(config['SCL_PIN']), sda=Pin(config['SDA_PIN']), freq=400000)
        print("Scanning I2C bus...")
        devices = i2c.scan()

        if not devices:
            print("No I2C devices found! Check OLED wiring.")
        else:
            print("I2C devices found:", [hex(device) for device in devices])
            oled_addr = 0x3C
            if oled_addr not in devices and (0x3D in devices):
                 oled_addr = 0x3D
            
            print(f"Initializing OLED at {hex(oled_addr)}...")
            display = ssd1306.SSD1306_I2C(
                config['SCREEN_WIDTH'], config['SCREEN_HEIGHT'], i2c, 
                addr=oled_addr, flipped=config['OLED_FLIPPED']
            )
            lcd.print("System Ready.", "Please swipe...")
            print("OLED Initialized.")
            
    except Exception as e:
        print(f"Error initializing OLED: {e}")
        print("Continuing without display...")

    if mode != 'accessory':
        print("Wiegand Reader Initializing...")
        print(f"Wiegand D0 Pin: {config['D0_PIN']}, D1 Pin: {config['D1_PIN']}")
        try:
            pin_d0 = Pin(config['D0_PIN'], Pin.IN, Pin.PULL_UP)
            pin_d1 = Pin(config['D1_PIN'], Pin.IN, Pin.PULL_UP)
            
            reset_wiegand_buffer() # Initialize buffer
            
            pin_d0.irq(trigger=Pin.IRQ_FALLING, handler=d0_pulse_handler)
            pin_d1.irq(trigger=Pin.IRQ_FALLING, handler=d1_pulse_handler)

            print("\nReader is active. Please swipe a card...")
            lcd.print("Reader is active. Please swipe a card...")

        except Exception as e:
            print(f"Error setting up Wiegand pins: {e}")
            lcd.print("PIN ERROR", str(e))
            return
    else:
        print("Accessory mode: Wiegand reader disabled")
        lcd.print("Accessory Mode", "Waiting for", "MQTT commands...", "")

    # --- FIX: Main loop restructured ---
    
    # Counter to run non-critical tasks less frequently
    loop_counter = 0
    # Run heavy tasks every 10 loops (approx 10 * 10ms = 100ms)
    NON_CRITICAL_TASKS_INTERVAL = 10 

    while True:
        try:
            # --- PRIORITY 1: Wiegand Reader Logic (if not accessory) ---
            if mode in ['raw', 'doorsim']:
                
                # Check if a card read is in progress
                if current_bit_index > 0:
                    
                    # A read is happening. Check for timeout.
                    time_since_last_pulse = utime.ticks_diff(utime.ticks_us(), last_pulse_time_microsec)
                    timeout_threshold = config['CARD_READ_TIMEOUT_MS'] * 1000
                    
                    if time_since_last_pulse > timeout_threshold:
                        # --- Card Read Finished ---
                        
                        # --- Start Critical Section ---
                        irq_state = machine.disable_irq()
                        # Copy the bit count and the *actual data*
                        bits_to_process = current_bit_index
                        data_to_process = bytearray(wiegand_bit_array) # Make a copy!
                        # Reset the global buffer NOW so new pulses are not missed
                        reset_wiegand_buffer()
                        machine.enable_irq(irq_state) 
                        # --- End Critical Section ---
                        
                        # Process the *copied* data
                        result = process_card_data(bits_to_process, data_to_process) # FIX: Pass copy
                        
                        if result:
                            if mode == 'raw':
                                handle_raw_mode(result, data_to_process) # FIX: Pass copy
                            elif mode == 'doorsim':
                                trigger_card_read_event(result['fc'], result['cn'], result)
                            
                            utime.sleep(4) # Hold result on screen
                            
                            if mode == 'raw':
                                lcd.print("Raw Mode Ready", "Please swipe...", "", "")
                            else:
                                lcd.print("System Ready.", "Please swipe...", "", "")
                            print("\n\nReader is active. Please swipe a card...")
                        else:
                            print("Card processing failed (0 bits or error). Buffer reset.")
                            lcd.print("Card processing failed (0 bits or error). Buffer reset.")
                    
                    else:
                        # Card is *currently* being read (between pulses)
                        # Do nothing else. Sleep for a tiny bit and re-check.
                        utime.sleep_us(100)
                        continue # Jump to start of while loop
                
                # --- PRIORITY 2: Idle Loop Tasks ---
                # This code only runs if current_bit_index == 0 (idle)
                
                loop_counter += 1
                if loop_counter >= NON_CRITICAL_TASKS_INTERVAL:
                    loop_counter = 0 # Reset counter
                    
                    # Run heavy tasks
                    if should_start_webserver:
                        webserver.process_requests()
                    
                    if mracs_enabled and mode == 'doorsim':
                        mqtt_loop()
                
                # Sleep to yield to interrupts and prevent busy-loop
                utime.sleep_ms(10) # 10ms is a good idle poll rate

            else:
                # --- Accessory Mode Loop (No Wiegand) ---
                if should_start_webserver:
                    webserver.process_requests()
                
                if mracs_enabled:
                    mqtt_loop()
                
                utime.sleep_ms(100) # Can sleep longer, no Wiegand to worry about

        except KeyboardInterrupt:
            print("Program stopped by user (Ctrl+C).")
            break
        except Exception as e:
            print(f"An error occurred in the main loop: {e}")
            lcd.print("LOOP ERROR", str(e))
            utime.sleep(5) # Pause on error
            
    # Cleanup
    if pin_d0: pin_d0.irq(handler=None)
    if pin_d1: pin_d1.irq(handler=None)
    print("Interrupts detached. Program End.")
    lcd.print("SYSTEM HALTED.")

# Run main program
if __name__ == '__main__':
    main()

