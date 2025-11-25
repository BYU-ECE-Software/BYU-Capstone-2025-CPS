# boot.py - WiFi Access Point Setup

import network
import json
import machine
import utime

def load_config():
    """Loads configuration from config.json file."""
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading config.json in boot.py: {e}")
        return {
            "MODE": "doorsim",
            "MRACS_ENABLED": False
        }

def setup_wifi():
    """Set up WiFi Access Point or Station mode based on MODE and MRACS settings."""
    config = load_config()
    mode = config.get('MODE', 'doorsim').lower()
    mracs_enabled = config.get('MRACS_ENABLED', False)
    
    ap = network.WLAN(network.AP_IF)
    sta = network.WLAN(network.STA_IF)
    
    # Disable both interfaces first
    ap.active(False)
    sta.active(False)
    utime.sleep_ms(100)
    
    # Determine if we should start Access Point
    start_ap = False
    if mode == 'raw':
        start_ap = True
    elif mode == 'doorsim' and not mracs_enabled:
        start_ap = True
    # If mode is 'accessory' or 'doorsim' with MRACS enabled, don't start AP
    
    if start_ap:
        # Start Access Point
        print("Starting WiFi Access Point...")
        
        # Ensure AP is fully deactivated first (always do a full reset)
        ap.active(False)
        utime.sleep_ms(500)  # Longer delay to ensure full deactivation
        
        # Activate AP first
        ap.active(True)
        utime.sleep_ms(300)  # Wait for AP to fully initialize
        
        # Configure AP parameters - set all at once to avoid state issues
        # This ensures password and authmode are set together
        try:
            ap.config(essid='opendoorsim', password='shortrange', authmode=network.AUTH_WPA_WPA2_PSK, channel=1, hidden=False)
        except TypeError:
            # Some MicroPython versions don't support all parameters
            ap.config(essid='opendoorsim', password='shortrange', authmode=network.AUTH_WPA_WPA2_PSK)
        
        utime.sleep_ms(300)  # Wait for configuration to fully apply
        
        # Verify configuration was set correctly
        current_essid = ap.config('essid')
        current_auth = ap.config('authmode')
        
        if current_essid != 'opendoorsim' or current_auth != network.AUTH_WPA_WPA2_PSK:
            # Reconfigure if not set correctly - do a full reset
            print("AP configuration verification failed, performing full reset...")
            ap.active(False)
            utime.sleep_ms(500)
            ap.active(True)
            utime.sleep_ms(300)
            try:
                ap.config(essid='opendoorsim', password='shortrange', authmode=network.AUTH_WPA_WPA2_PSK, channel=1, hidden=False)
            except TypeError:
                ap.config(essid='opendoorsim', password='shortrange', authmode=network.AUTH_WPA_WPA2_PSK)
            utime.sleep_ms(300)
        
        # Set IP configuration explicitly (optional but helps with stability)
        ap.ifconfig(('192.168.4.1', '255.255.255.0', '192.168.4.1', '192.168.4.1'))
        utime.sleep_ms(100)
        
        # Get AP IP address
        ap_ip = ap.ifconfig()[0]
        print(f"Access Point started!")
        print(f"SSID: {ap.config('essid')}")
        print(f"Password: shortrange")
        print(f"Auth Mode: {ap.config('authmode')}")
        print(f"AP IP: {ap_ip}")
        print(f"Connect to http://{ap_ip} for web interface")
        
        return ap_ip
    else:
        # Prepare for MQTT connection (Station mode)
        print("MRACS mode enabled - preparing for MQTT connection")
        print("WiFi Access Point will not be started")
        print("Device will connect to MQTT broker on startup")
        return None

# Run WiFi setup on boot
try:
    ap_ip = setup_wifi()
except Exception as e:
    print(f"Error setting up WiFi: {e}")
    print("Continuing without WiFi setup...")
