/**
 * Sagatoy WiFi Setup Web Server
 * 
 * Creates a simple web page for families to configure WiFi
 * No app needed - just use a browser!
 * 
 * Flow:
 * 1. ESP32 starts in AP mode (creates WiFi network)
 * 2. User connects to "Sagatoy-Setup" 
 * 3. User opens browser -> sees setup page
 * 4. User enters WiFi name & password
 * 5. ESP32 saves and connects to real WiFi
 */

#include <WiFi.h>
#include <WebServer.h>
#include <Preferences.h>
#include <DNSServer.h>

// Configuration
const char* AP_SSID = "Sagatoy-Setup";
const char* AP_PASSWORD = "sagatoy123";  // Simple password for families
// SECURITY NOTE: Change this password in production!
// Consider using a random password generated per-device
const char* AP_IP = "192.168.1.1";

// DNS for captive portal
DNSServer dnsServer;
WebServer server(80);

// Storage
Preferences preferences;

// HTML for the setup page (compact version)
const char SETUP_PAGE[] = R"rawliteral(
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Sagatoy Setup</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
               background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
               min-height: 100vh; display: flex; align-items: center; justify-content: center; margin: 0; }
        .container { background: white; padding: 30px; border-radius: 20px; 
                     box-shadow: 0 10px 40px rgba(0,0,0,0.2); max-width: 400px; width: 90%; }
        h1 { color: #667eea; text-align: center; margin-bottom: 10px; }
        p { color: #666; text-align: center; margin-bottom: 20px; }
        .logo { font-size: 50px; text-align: center; margin-bottom: 10px; }
        input { width: 100%; padding: 15px; margin: 10px 0; border: 2px solid #ddd; 
                border-radius: 10px; box-sizing: border-box; font-size: 16px; }
        input:focus { border-color: #667eea; outline: none; }
        button { width: 100%; padding: 15px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                  color: white; border: none; border-radius: 10px; font-size: 18px; cursor: pointer;
                  margin-top: 10px; font-weight: bold; }
        button:hover { opacity: 0.9; }
        .status { text-align: center; padding: 20px; color: #666; }
        .success { color: #4CAF50; }
        .error { color: #f44336; }
        .instructions { background: #f5f5f5; padding: 15px; border-radius: 10px; margin-bottom: 20px; }
        .instructions ol { margin: 0; padding-left: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">🧸</div>
        <h1>Sagatoy Setup</h1>
        <div class="instructions">
            <strong>How to connect:</strong>
            <ol>
                <li>Select your home WiFi below</li>
                <li>Enter your WiFi password</li>
                <li>Click "Connect"</li>
            </ol>
        </div>
        <form id="setupForm">
            <input type="text" id="ssid" name="ssid" placeholder="WiFi Network Name" required>
            <input type="password" id="password" name="password" placeholder="WiFi Password" required>
            <button type="submit" id="connectBtn">Connect</button>
        </form>
        <div id="status" class="status"></div>
    </div>
    <script>
        document.getElementById('setupForm').onsubmit = function(e) {
            e.preventDefault();
            var btn = document.getElementById('connectBtn');
            var status = document.getElementById('status');
            
            btn.disabled = true;
            btn.textContent = 'Connecting...';
            status.innerHTML = 'Sending your WiFi info to Sagatoy...';
            
            var formData = new FormData();
            formData.append('ssid', document.getElementById('ssid').value);
            formData.append('password', document.getElementById('password').value);
            
            fetch('/save', {
                method: 'POST',
                body: formData
            })
            .then(response => response.text())
            .then(data => {
                if (data.includes('OK')) {
                    status.innerHTML = '<p class="success">✅ Success!</p><p>Sagatoy is connecting to your WiFi...</p><p>Wait a moment, then talk to your toy!</p>';
                    btn.textContent = 'Connected!';
                } else {
                    status.innerHTML = '<p class="error">❌ ' + data + '</p>';
                    btn.disabled = false;
                    btn.textContent = 'Try Again';
                }
            })
            .catch(err => {
                status.innerHTML = '<p class="error">❌ Error: ' + err + '</p>';
                btn.disabled = false;
                btn.textContent = 'Try Again';
            });
        };
    </script>
</body>
</html>
)rawliteral";

void setupAccessPoint() {
    // Start AP mode
    WiFi.mode(WIFI_AP);
    WiFi.softAP(AP_SSID, AP_PASSWORD);
    
    Serial.print("AP started: ");
    Serial.println(AP_SSID);
    Serial.print("IP: ");
    Serial.println(WiFi.softAPIP());

    // Setup DNS for captive portal (redirect all domains to our page)
    dnsServer.onAny([]()
    {
        server.handleRequest();
    });
    dnsServer.start(53, "*", WiFi.softAPIP());
    
    // Set up web server routes
    server.on("/", HTTP_GET, []()
    {
        server.send(200, "text/html", SETUP_PAGE);
    });
    
    server.on("/save", HTTP_POST, []()
    {
        String ssid = server.arg("ssid");
        String password = server.arg("password");
        
        if (ssid.length() > 0 && password.length() > 0) {
            // Save to preferences
            preferences.begin("sagatoy", false);
            preferences.putString("wifi_ssid", ssid);
            preferences.putString("wifi_pass", password);
            preferences.end();
            
            Serial.print("WiFi saved: ");
            Serial.println(ssid);
            
            server.send(200, "text/plain", "OK - Saved! Restarting...");
            delay(1000);
            
            // Restart to connect to real WiFi
            ESP.restart();
        } else {
            server.send(400, "text/plain", "Missing SSID or Password");
        }
    });
    
    server.onNotFound([]()
    {
        server.send(200, "text/html", SETUP_PAGE);
    });
    
    server.begin();
    Serial.println("Web server started!");
}

void tryConnectWiFi() {
    preferences.begin("sagatoy", false);
    String ssid = preferences.getString("wifi_ssid", "");
    String password = preferences.getString("wifi_pass", "");
    preferences.end();
    
    if (ssid.length() > 0) {
        Serial.print("Trying to connect to: ");
        Serial.println(ssid);
        
        WiFi.mode(WIFI_STA);
        WiFi.begin(ssid.c_str(), password.c_str());
        
        int attempts = 0;
        while (WiFi.status() != WL_CONNECTED && attempts < 20) {
            delay(500);
            Serial.print(".");
            attempts++;
        }
        
        if (WiFi.status() == WL_CONNECTED) {
            Serial.println("\nWiFi connected!");
            Serial.print("IP: ");
            Serial.println(WiFi.localIP());
            return;  // Connected!
        }
    }
    
    // If not connected, start AP mode for setup
    Serial.println("\nNo saved WiFi or connection failed - starting setup mode...");
    setupAccessPoint();
}

void setup() {
    Serial.begin(115200);
    Serial.println("\n=== Sagatoy WiFi Setup ===");
    
    // Try to connect to saved WiFi first
    tryConnectWiFi();
}

void loop() {
    // Handle DNS and web requests
    dnsServer.processNextRequest();
    server.handleClient();
}