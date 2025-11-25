# webserver.py - Web Interface Server for OpenDoorSim

import socket
import json
import network
import utime

# Global variables
card_history = []  # Store last 25 card reads
MAX_HISTORY = 25

def add_card_to_history(card_data):
    """Add a card read to the history, keeping only the last MAX_HISTORY entries."""
    global card_history
    card_history.insert(0, {
        'timestamp': utime.time(),
        'fc': card_data.get('fc', -1),
        'cn': card_data.get('cn', -1),
        'bits': card_data.get('bits', 0),
        'hex': card_data.get('raw_hex', ''),
        'parity_ok': card_data.get('parity_ok', False),
        'format': card_data.get('name', 'Unknown')
    })
    if len(card_history) > MAX_HISTORY:
        card_history = card_history[:MAX_HISTORY]

def get_ap_ip():
    """Get the Access Point IP address."""
    ap = network.WLAN(network.AP_IF)
    if ap.active():
        return ap.ifconfig()[0]
    return "192.168.4.1"  # Default AP IP

def load_config():
    """Load configuration from config.json."""
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except:
        return {}

def save_config(config):
    """Save configuration to config.json."""
    try:
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving config: {e}")
        return False

def load_users():
    """Load users from users.json."""
    try:
        with open('users.json', 'r') as f:
            return json.load(f)
    except:
        return []

def save_users(users):
    """Save users to users.json."""
    try:
        with open('users.json', 'w') as f:
            json.dump(users, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving users: {e}")
        return False

def load_events():
    """Load events from events.json."""
    try:
        with open('events.json', 'r') as f:
            return json.load(f)
    except:
        return []

def save_events(events):
    """Save events to events.json."""
    try:
        with open('events.json', 'w') as f:
            json.dump(events, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving events: {e}")
        return False

def format_timestamp(timestamp):
    """Format Unix timestamp to readable string."""
    try:
        # MicroPython doesn't have full datetime, so use simple format
        return str(timestamp)
    except:
        return "Unknown"

def generate_html_home(config, users, events):
    """Generate HTML for the Home tab."""
    mracs_status = "Enabled" if config.get('MRACS_ENABLED', False) else "Disabled"
    mode = config.get('MODE', 'doorsim').upper()
    
    history_html = ""
    for card in card_history:
        timestamp_str = format_timestamp(card['timestamp'])
        parity_status = "PASS" if card['parity_ok'] else "FAIL"
        fc_display = str(card['fc']) if card['fc'] != -1 else "N/A"
        history_html += f"""
        <tr>
            <td>{timestamp_str}</td>
            <td>{fc_display}</td>
            <td>{card['cn']}</td>
            <td>{card['bits']}</td>
            <td>{card['hex']}</td>
            <td>{parity_status}</td>
            <td>{card['format']}</td>
        </tr>
        """
    
    if not history_html:
        history_html = "<tr><td colspan='7'>No card reads yet</td></tr>"
    
    return f"""
    <div id="home" class="tab-content active">
        <h2>System Status</h2>
        <div class="status-grid">
            <div class="status-item">
                <strong>Mode:</strong> {mode}
            </div>
            <div class="status-item">
                <strong>MRACS:</strong> {mracs_status}
            </div>
            <div class="status-item">
                <strong>Users:</strong> {len(users)}
            </div>
            <div class="status-item">
                <strong>Events:</strong> {len(events)}
            </div>
        </div>
        
        <h2>Configuration</h2>
        <div class="config-display">
            <p><strong>D0 Pin:</strong> {config.get('D0_PIN', 'N/A')}</p>
            <p><strong>D1 Pin:</strong> {config.get('D1_PIN', 'N/A')}</p>
            <p><strong>SCL Pin:</strong> {config.get('SCL_PIN', 'N/A')}</p>
            <p><strong>SDA Pin:</strong> {config.get('SDA_PIN', 'N/A')}</p>
            <p><strong>Screen:</strong> {config.get('SCREEN_WIDTH', 'N/A')}x{config.get('SCREEN_HEIGHT', 'N/A')}</p>
            <p><strong>MQTT Broker:</strong> {config.get('MQTT_BROKER', 'N/A')}</p>
        </div>
        
        <h2>Card Read History (Last 25)</h2>
        <table class="history-table">
            <thead>
                <tr>
                    <th>Timestamp</th>
                    <th>FC</th>
                    <th>CN</th>
                    <th>Bits</th>
                    <th>Hex</th>
                    <th>Parity</th>
                    <th>Format</th>
                </tr>
            </thead>
            <tbody>
                {history_html}
            </tbody>
        </table>
        
        <div class="button-group">
            <button onclick="location.reload()">Refresh</button>
            <button onclick="rebootDevice()">Reboot Device</button>
        </div>
    </div>
    """

def generate_html_users(users):
    """Generate HTML for the USERS tab."""
    users_html = ""
    for i, user in enumerate(users):
        active_checked = "checked" if user.get('active', True) else ""
        users_html += f"""
        <tr>
            <td><input type="number" name="fc_{i}" value="{user.get('FC', '')}" /></td>
            <td><input type="number" name="cn_{i}" value="{user.get('CN', '')}" /></td>
            <td><input type="text" name="name_{i}" value="{user.get('Name', '')}" /></td>
            <td><input type="text" name="flag_{i}" value="{user.get('Flag', '')}" /></td>
            <td><input type="checkbox" name="active_{i}" {active_checked} /></td>
            <td><button onclick="deleteUser({i})">Delete</button></td>
        </tr>
        """
    
    if not users_html:
        users_html = "<tr><td colspan='6'>No users defined</td></tr>"
    
    return f"""
    <div id="users" class="tab-content">
        <h2>User Management</h2>
        <form method="POST" action="/save_users">
            <table class="edit-table">
                <thead>
                    <tr>
                        <th>FC</th>
                        <th>CN</th>
                        <th>Name</th>
                        <th>Flag</th>
                        <th>Active</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody id="usersTable">
                    {users_html}
                </tbody>
            </table>
            <div class="button-group">
                <button type="button" onclick="addUserRow()">Add User</button>
                <button type="submit">Save Users</button>
                <button type="button" onclick="reloadUsers()">Reload</button>
            </div>
        </form>
    </div>
    """

def generate_html_events(events):
    """Generate HTML for the EVENTS tab."""
    events_html = ""
    for i, event in enumerate(events):
        fc_value = event.get('FC', '')
        cn_value = event.get('CN', '')
        action = event.get('action', '')
        params = json.dumps(event.get('params', {}))
        events_html += f"""
        <tr>
            <td><input type="number" name="fc_{i}" value="{fc_value}" placeholder="-1 for event code" /></td>
            <td><input type="number" name="cn_{i}" value="{cn_value}" /></td>
            <td><input type="text" name="action_{i}" value="{action}" /></td>
            <td><textarea name="params_{i}" rows="2">{params}</textarea></td>
            <td><button onclick="deleteEvent({i})">Delete</button></td>
        </tr>
        """
    
    if not events_html:
        events_html = "<tr><td colspan='5'>No events defined</td></tr>"
    
    return f"""
    <div id="events" class="tab-content">
        <h2>Event Management</h2>
        <form method="POST" action="/save_events">
            <table class="edit-table">
                <thead>
                    <tr>
                        <th>FC</th>
                        <th>CN</th>
                        <th>Action</th>
                        <th>Params (JSON)</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody id="eventsTable">
                    {events_html}
                </tbody>
            </table>
            <div class="button-group">
                <button type="button" onclick="addEventRow()">Add Event</button>
                <button type="submit">Save Events</button>
                <button type="button" onclick="reloadEvents()">Reload</button>
            </div>
        </form>
    </div>
    """

def generate_html_config(config):
    """Generate HTML for the CONFIG tab."""
    return f"""
    <div id="config" class="tab-content">
        <h2>Configuration</h2>
        <form method="POST" action="/save_config">
            <div class="config-form">
                <label>Mode:</label>
                <select name="MODE">
                    <option value="raw" {'selected' if config.get('MODE') == 'raw' else ''}>Raw</option>
                    <option value="doorsim" {'selected' if config.get('MODE') == 'doorsim' else ''}>Doorsim</option>
                    <option value="accessory" {'selected' if config.get('MODE') == 'accessory' else ''}>Accessory</option>
                </select>
                
                <label>MRACS Enabled:</label>
                <input type="checkbox" name="MRACS_ENABLED" {'checked' if config.get('MRACS_ENABLED', False) else ''} />
                
                <label>D0 Pin:</label>
                <input type="number" name="D0_PIN" value="{config.get('D0_PIN', 21)}" />
                
                <label>D1 Pin:</label>
                <input type="number" name="D1_PIN" value="{config.get('D1_PIN', 22)}" />
                
                <label>SCL Pin:</label>
                <input type="number" name="SCL_PIN" value="{config.get('SCL_PIN', 18)}" />
                
                <label>SDA Pin:</label>
                <input type="number" name="SDA_PIN" value="{config.get('SDA_PIN', 19)}" />
                
                <label>Screen Width:</label>
                <input type="number" name="SCREEN_WIDTH" value="{config.get('SCREEN_WIDTH', 128)}" />
                
                <label>Screen Height:</label>
                <input type="number" name="SCREEN_HEIGHT" value="{config.get('SCREEN_HEIGHT', 32)}" />
                
                <label>MQTT Broker:</label>
                <input type="text" name="MQTT_BROKER" value="{config.get('MQTT_BROKER', '192.168.1.100')}" />
                
                <label>MQTT Port:</label>
                <input type="number" name="MQTT_PORT" value="{config.get('MQTT_PORT', 1883)}" />
                
                <label>MQTT Client ID:</label>
                <input type="text" name="MQTT_CLIENT_ID" value="{config.get('MQTT_CLIENT_ID', '')}" />
            </div>
            <div class="button-group">
                <button type="submit">Save Config</button>
                <button type="button" onclick="reloadConfig()">Reload</button>
            </div>
        </form>
    </div>
    """
        # {generate_html_home(config, users, events)}
        # {generate_html_users(users)}
        # {generate_html_events(events)}
        # {generate_html_config(config)}
def generate_full_html(config, users, events):
    """Generate the complete HTML page."""
    return f"""<!DOCTYPE html>
<html>
<head>
    <title>OpenDoorSim Home</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: Arial, sans-serif; background: #f5f5f5; padding: 20px; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .header {{ background: #2c3e50; color: white; padding: 20px; border-radius: 8px 8px 0 0; }}
        .tabs {{ display: flex; background: #34495e; }}
        .tab {{ padding: 15px 20px; cursor: pointer; color: white; border: none; background: transparent; }}
        .tab:hover {{ background: #2c3e50; }}
        .tab.active {{ background: #2c3e50; }}
        .tab-content {{ display: none; padding: 20px; }}
        .tab-content.active {{ display: block; }}
        .status-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0; }}
        .status-item {{ background: #ecf0f1; padding: 15px; border-radius: 5px; }}
        .config-display {{ background: #ecf0f1; padding: 15px; border-radius: 5px; margin: 20px 0; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background: #34495e; color: white; }}
        tr:hover {{ background: #f5f5f5; }}
        .edit-table input, .edit-table textarea {{ width: 100%; padding: 5px; }}
        .button-group {{ margin-top: 20px; }}
        button {{ padding: 10px 20px; margin: 5px; background: #3498db; color: white; border: none; border-radius: 5px; cursor: pointer; }}
        button:hover {{ background: #2980b9; }}
        .config-form {{ display: grid; grid-template-columns: 150px 1fr; gap: 10px; align-items: center; margin: 20px 0; }}
        .config-form label {{ font-weight: bold; }}
        .config-form input, .config-form select {{ padding: 8px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>OpenDoorSim Control Panel</h1>
            <p>ESP32 Access Control System</p>
        </div>
        <div class="tabs">
            <button class="tab active" onclick="showTab('home')">Home</button>
            <button class="tab" onclick="showTab('users')">Users</button>
            <button class="tab" onclick="showTab('events')">Events</button>
            <button class="tab" onclick="showTab('config')">Config</button>
        </div>
        

    </div>
    <script>
        function showTab(tabName) {{
            document.querySelectorAll(".tab-content").forEach(function(tab) {{ tab.classList.remove("active"); }});
            document.querySelectorAll(".tab").forEach(function(tab) {{ tab.classList.remove("active"); }});
            document.getElementById(tabName).classList.add("active");
            event.target.classList.add("active");
        }}
        function rebootDevice() {{
            if (confirm("Reboot device?")) {{
                fetch("/reboot", {{method: "POST"}}).then(function() {{ location.reload(); }});
            }}
        }}
        function addUserRow() {{
            const table = document.getElementById("usersTable");
            const row = table.insertRow();
            const i = table.rows.length - 1;
            row.innerHTML = `
                <td><input type="number" name="fc_${{i}}" value="" /></td>
                <td><input type="number" name="cn_${{i}}" value="" /></td>
                <td><input type="text" name="name_${{i}}" value="" /></td>
                <td><input type="text" name="flag_${{i}}" value="" /></td>
                <td><input type="checkbox" name="active_${{i}}" checked /></td>
                <td><button onclick="this.parentElement.parentElement.remove()">Delete</button></td>
            `;
        }}
        function deleteUser(index) {{
            if (confirm("Delete this user?")) {{
                document.getElementById("usersTable").rows[index].remove();
            }}
        }}
        function addEventRow() {{
            const table = document.getElementById("eventsTable");
            const row = table.insertRow();
            const i = table.rows.length - 1;
            row.innerHTML = `
                <td><input type="number" name="fc_${{i}}" value="" placeholder="-1 for event code" /></td>
                <td><input type="number" name="cn_${{i}}" value="" /></td>
                <td><input type="text" name="action_${{i}}" value="" /></td>
                <td><textarea name="params_${{i}}" rows="2">{{}}</textarea></td>
                <td><button onclick="this.parentElement.parentElement.remove()">Delete</button></td>
            `;
        }}
        function deleteEvent(index) {{
            if (confirm("Delete this event?")) {{
                document.getElementById("eventsTable").rows[index].remove();
            }}
        }}
        function reloadUsers() {{ location.reload(); }}
        function reloadEvents() {{ location.reload(); }}
        function reloadConfig() {{ location.reload(); }}
    </script>
</body>
</html>"""

def parse_post_data(data):
    """Parse POST form data."""
    params = {}
    if 'Content-Type' in data:
        # Handle form-urlencoded data
        body = data.split('\r\n\r\n', 1)[1] if '\r\n\r\n' in data else data.split('\n\n', 1)[1]
        for pair in body.split('&'):
            if '=' in pair:
                key, value = pair.split('=', 1)
                params[key] = value.replace('+', ' ').replace('%3A', ':').replace('%2F', '/')
    return params

def handle_request(conn, addr):
    """Handle HTTP request."""
    try:
        request = conn.recv(1024).decode('utf-8')
        if not request:
            return
        
        # Parse request
        request_line = request.split('\n')[0]
        method, path, _ = request_line.split(' ', 2)
        
        # Load current data
        config = load_config()
        users = load_users() 
        events = load_events() 
        
        if path == '/' or path == '/index.html':
            # Serve main page
            html = generate_full_html(config, users, events) 
            # html = "<h1>Hello World</h1>" # TODO: remove this, its just a test webpage
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {len(html)}\r\n\r\n{html}"
            conn.send(response.encode())
            
        elif path == '/save_users' and method == 'POST':
            # Parse and save users
            params = parse_post_data(request)
            new_users = []
            i = 0
            while f'fc_{i}' in params:
                try:
                    fc = int(params.get(f'fc_{i}', '')) if params.get(f'fc_{i}', '') else None
                    cn = int(params.get(f'cn_{i}', '')) if params.get(f'cn_{i}', '') else None
                    if fc is not None and cn is not None:
                        new_users.append({
                            'FC': fc,
                            'CN': cn,
                            'Name': params.get(f'name_{i}', ''),
                            'Flag': params.get(f'flag_{i}', ''),
                            'active': f'active_{i}' in params
                        })
                except:
                    pass
                i += 1
            
            if save_users(new_users):
                response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<h1>Users saved!</h1><a href='/'>Back</a>"
            else:
                response = "HTTP/1.1 500 OK\r\nContent-Type: text/html\r\n\r\n<h1>Error saving users</h1>"
            conn.send(response.encode())
            
        elif path == '/save_events' and method == 'POST':
            # Parse and save events
            params = parse_post_data(request)
            new_events = []
            i = 0
            while f'fc_{i}' in params:
                try:
                    fc_str = params.get(f'fc_{i}', '')
                    cn_str = params.get(f'cn_{i}', '')
                    fc = int(fc_str) if fc_str else None
                    cn = int(cn_str) if cn_str else None
                    action = params.get(f'action_{i}', '')
                    params_json = params.get(f'params_{i}', '{}')
                    
                    if action:
                        event = {'action': action}
                        if fc is not None:
                            event['FC'] = fc
                        if cn is not None:
                            event['CN'] = cn
                        try:
                            event['params'] = json.loads(params_json)
                        except:
                            event['params'] = {}
                        new_events.append(event)
                except Exception as e:
                    print(f"Error parsing event {i}: {e}")
                i += 1
            
            if save_events(new_events):
                response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<h1>Events saved!</h1><a href='/'>Back</a>"
            else:
                response = "HTTP/1.1 500 OK\r\nContent-Type: text/html\r\n\r\n<h1>Error saving events</h1>"
            conn.send(response.encode())
            
        elif path == '/save_config' and method == 'POST':
            # Parse and save config
            params = parse_post_data(request)
            new_config = config.copy()
            
            if 'MODE' in params:
                new_config['MODE'] = params['MODE']
            if 'MRACS_ENABLED' in params:
                new_config['MRACS_ENABLED'] = True
            else:
                new_config['MRACS_ENABLED'] = False
            if 'D0_PIN' in params:
                new_config['D0_PIN'] = int(params['D0_PIN'])
            if 'D1_PIN' in params:
                new_config['D1_PIN'] = int(params['D1_PIN'])
            if 'SCL_PIN' in params:
                new_config['SCL_PIN'] = int(params['SCL_PIN'])
            if 'SDA_PIN' in params:
                new_config['SDA_PIN'] = int(params['SDA_PIN'])
            if 'SCREEN_WIDTH' in params:
                new_config['SCREEN_WIDTH'] = int(params['SCREEN_WIDTH'])
            if 'SCREEN_HEIGHT' in params:
                new_config['SCREEN_HEIGHT'] = int(params['SCREEN_HEIGHT'])
            if 'MQTT_BROKER' in params:
                new_config['MQTT_BROKER'] = params['MQTT_BROKER']
            if 'MQTT_PORT' in params:
                new_config['MQTT_PORT'] = int(params['MQTT_PORT'])
            if 'MQTT_CLIENT_ID' in params:
                new_config['MQTT_CLIENT_ID'] = params['MQTT_CLIENT_ID']
            
            if save_config(new_config):
                response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<h1>Config saved! Reboot required.</h1><a href='/'>Back</a>"
            else:
                response = "HTTP/1.1 500 OK\r\nContent-Type: text/html\r\n\r\n<h1>Error saving config</h1>"
            conn.send(response.encode())
            
        elif path == '/reboot' and method == 'POST':
            response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<h1>Rebooting...</h1>"
            conn.send(response.encode())
            conn.close()
            utime.sleep(1)
            import machine
            machine.reset()
            
        else:
            # 404
            response = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n<h1>404 Not Found</h1>"
            conn.send(response.encode())
            
    except Exception as e:
        print(f"Error handling request: {e}")
        try:
            response = "HTTP/1.1 500 Internal Server Error\r\n\r\n"
            conn.send(response.encode())
        except:
            pass
    finally:
        conn.close()

def start_server(port=80):
    """Start the web server."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', port))
    s.listen(5)
    print(f"Web server started on port {port}")
    print(f"Access at http://{get_ap_ip()}")
    
    while True:
        try:
            conn, addr = s.accept()
            handle_request(conn, addr)
        except Exception as e:
            print(f"Server error: {e}")
            utime.sleep(1)

# For non-blocking operation
server_socket = None

def start_server_non_blocking(port=80):
    """Start web server in non-blocking mode."""
    global server_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.settimeout(0.1)  # Non-blocking
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(5)
    print(f"Web server started (non-blocking) on port {port}")

def process_requests():
    """Process pending web server requests (call this in main loop)."""
    global server_socket
    if server_socket:
        try:
            conn, addr = server_socket.accept()
            handle_request(conn, addr)
        except OSError:
            pass  # No connection pending
        except Exception as e:
            print(f"Error processing request: {e}")

