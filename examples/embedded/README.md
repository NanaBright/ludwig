<p align="center">
  <img src="https://raw.githubusercontent.com/NanaBright/ludwig/main/assets/logo.png" alt="Ludwig Logo" width="120"/>
</p>

# Ludwig Embedded Systems Examples

This directory contains example embedded applications demonstrating Ludwig's IoT and embedded systems capabilities.

## Available Examples

### 🌡️ IoT Device (`testiot_embedded.ludwig`)
Basic IoT device with temperature and motion sensors, cloud connectivity, and event handling.

**Features:**
- Temperature and motion monitoring
- WiFi connectivity
- Cloud data synchronization
- Real-time alerts

**Run:**
```bash
python testiot_embedded.ludwig
```

### 💳 Point of Sale System (`testpos_pos.ludwig`)
Complete POS system with barcode scanning, inventory management, and payment processing.

**Features:**
- Barcode/QR code scanning
- Inventory tracking
- Payment terminal integration
- Sales reporting
- Cloud backup

**Run:**
```bash
python testpos_pos.ludwig
```

### 📱 QR Kiosk (`testkiosk_kiosk.ludwig`)
Interactive kiosk system for information display and QR code interactions.

**Features:**
- QR code scanning
- Interactive display
- Auto-reset functionality
- User session management

**Run:**
```bash
python testkiosk_kiosk.ludwig
```

### 📦 Inventory Scanner (`warehousescanner_scanner.ludwig`)
Warehouse inventory management system with barcode scanning and cloud synchronization.

**Features:**
- Barcode scanning (add/remove/count modes)
- Inventory tracking
- Cloud synchronization
- Real-time updates

**Run:**
```bash
python warehousescanner_scanner.ludwig
```

### 🏠 Smart Home System (`smarthouse_smarthome.ludwig`)
Home automation system with device control, security, and environmental monitoring.

**Features:**
- Device management (lights, thermostat, cameras)
- Motion detection and security
- Temperature monitoring
- Automation rules
- Remote control via cloud

**Run:**
```bash
python smarthouse_smarthome.ludwig
```

### 🤖 Robotics Controller (`myrobot_robot.ludwig`)
Robot control system with navigation, obstacle avoidance, and autonomous operation.

**Features:**
- Motor and servo control
- Ultrasonic distance sensing
- Gyroscope and accelerometer
- Autonomous navigation
- Safety systems (auto-stop)
- Bluetooth communication

**Run:**
```bash
python myrobot_robot.ludwig
```

## Hardware Requirements

### Minimum Setup
- Raspberry Pi 3B+ or newer
- Python 3.7+
- GPIO access
- Internet connection (for cloud features)

### Recommended Components

#### Sensors
- **Temperature**: DS18B20, DHT22, or BME280
- **Motion**: PIR sensor (HC-SR501)
- **Distance**: Ultrasonic sensor (HC-SR04)
- **Light**: Photoresistor or BH1750
- **Barcode/QR**: USB scanner or camera module

#### Actuators
- **Display**: LCD (16x2, 20x4) or OLED
- **Motors**: Servo motors, stepper motors
- **Relays**: For controlling lights/appliances

#### Communication
- **WiFi**: Built-in (Raspberry Pi) or ESP8266/ESP32
- **Bluetooth**: Built-in or USB dongle
- **Camera**: Raspberry Pi Camera Module

## Getting Started

### 1. Hardware Setup
Connect your sensors and actuators to the appropriate GPIO pins:

```
Temperature (DS18B20): GPIO 4
Motion Sensor: GPIO 18
Ultrasonic Trigger: GPIO 23
Ultrasonic Echo: GPIO 24
Display SDA: GPIO 2
Display SCL: GPIO 3
```

### 2. Install Dependencies
```bash
# Install Ludwig embedded framework
cd /path/to/ludwig
pip install -r requirements.txt

# Install hardware libraries (Raspberry Pi)
sudo apt-get update
sudo apt-get install python3-rpi.gpio python3-smbus
pip install adafruit-circuitpython-dht
```

### 3. Configure Hardware
Edit the example files to match your hardware configuration:

```ludwig
# In your .ludwig file
device.config = {
    "temperature_pin": 4,
    "motion_pin": 18,
    "wifi_ssid": "YourNetwork",
    "wifi_password": "YourPassword"
}
```

### 4. Run Examples
```bash
# Basic IoT device
python testiot_embedded.ludwig

# With debug output
LUDWIG_DEBUG=1 python testiot_embedded.ludwig

# Run as background service
nohup python testiot_embedded.ludwig > device.log 2>&1 &
```

## Customization

### Adding New Sensors
```ludwig
# Create custom sensor
class CustomSensor(Embedded.Sensor):
    def __init__(self):
        super().__init__("custom")
    
    def read_value(self):
        # Your sensor reading logic
        return sensor_value
    end
end

# Add to device
device.add_sensor("custom", CustomSensor())
```

### Cloud Integration
Configure cloud services for data synchronization:

```ludwig
cloud = device.get_service("cloud")
cloud.configure({
    "endpoint": "https://your-iot-platform.com/api",
    "api_key": "your-api-key",
    "device_id": "device-001"
})

# Send data
cloud.sync_data({
    "sensor_data": readings,
    "timestamp": datetime.now()
})
```

### Adding Automation Rules
```ludwig
# Smart home automation
home.add_rule("motion_lights", function():
    if motion_detected and hour > 18:
        home.control_device("living_room_light", {"state": "on"})
    end
end)
```

## Production Deployment

### Systemd Service
Create a systemd service for automatic startup:

```ini
# /etc/systemd/system/ludwig-iot.service
[Unit]
Description=Ludwig IoT Device
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/ludwig-device
ExecStart=/usr/bin/python3 /home/pi/ludwig-device/mydevice_embedded.ludwig
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable the service:
```bash
sudo systemctl enable ludwig-iot
sudo systemctl start ludwig-iot
```

### Monitoring
Monitor your device status:

```bash
# Check service status
sudo systemctl status ludwig-iot

# View logs
sudo journalctl -u ludwig-iot -f

# Monitor system resources
htop
```

## Troubleshooting

### Common Issues

#### GPIO Permission Denied
```bash
# Add user to gpio group
sudo usermod -a -G gpio $USER
# Log out and back in
```

#### Sensor Not Detected
```bash
# Check I2C devices
sudo i2cdetect -y 1

# Test GPIO pins
python3 -c "import RPi.GPIO as GPIO; GPIO.setmode(GPIO.BCM); GPIO.setup(18, GPIO.IN); print(GPIO.input(18))"
```

#### WiFi Connection Issues
```bash
# Check network status
iwconfig
sudo wpa_cli status

# Reset network
sudo systemctl restart dhcpcd
```

### Debug Mode
Enable verbose logging for troubleshooting:

```bash
export LUDWIG_LOG_LEVEL=DEBUG
python mydevice_embedded.ludwig
```

## Next Steps

1. **Try the examples** - Start with `testiot_embedded.ludwig`
2. **Connect real hardware** - Wire up sensors and test
3. **Customize for your needs** - Modify the code for your specific use case
4. **Deploy to production** - Set up as a system service
5. **Add cloud integration** - Connect to your preferred IoT platform
6. **Scale up** - Deploy multiple devices and create a fleet

## Resources

- [Ludwig Embedded Guide](../docs/EMBEDDED_GUIDE.md) - Comprehensive development guide
- [Ludwig Documentation](../docs/README.md) - Main documentation
- [Hardware Compatibility](https://ludwig-platform.com/hardware) - Supported hardware list
- [Community Examples](https://github.com/ludwig-platform/community-examples) - User-contributed examples

Happy building! 🚀
