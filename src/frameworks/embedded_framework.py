"""
Ludwig Embedded Systems Framework

A lightweight framework for embedded systems and IoT development inspired by Arduino and Raspberry Pi ecosystems.
Provides hardware abstraction, sensor interfaces, and common embedded application patterns.
"""

import time
import json
import threading
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable


class EmbeddedDevice:
    """Base class for embedded devices."""
    
    def __init__(self, device_name: str = "Ludwig Device", version: str = "1.0.0"):
        """Initialize embedded device."""
        self.device_name = device_name
        self.version = version
        self.is_running = False
        self.sensors = {}
        self.actuators = {}
        self.services = {}
        self.event_handlers = {}
        self.config = {}
        
    def add_sensor(self, name: str, sensor_instance):
        """Add a sensor to the device."""
        self.sensors[name] = sensor_instance
        
    def add_actuator(self, name: str, actuator_instance):
        """Add an actuator to the device."""
        self.actuators[name] = actuator_instance
        
    def add_service(self, name: str, service_instance):
        """Add a service to the device."""
        self.services[name] = service_instance
        
    def get_sensor(self, name: str):
        """Get a sensor by name."""
        return self.sensors.get(name)
    
    def get_actuator(self, name: str):
        """Get an actuator by name."""
        return self.actuators.get(name)
    
    def get_service(self, name: str):
        """Get a service by name."""
        return self.services.get(name)
    
    def on(self, event: str, handler: Callable):
        """Add event handler."""
        if event not in self.event_handlers:
            self.event_handlers[event] = []
        self.event_handlers[event].append(handler)
        
    def emit(self, event: str, data: Any = None):
        """Emit an event."""
        if event in self.event_handlers:
            for handler in self.event_handlers[event]:
                handler(data)
    
    def start(self):
        """Start the embedded device."""
        self.is_running = True
        self.emit("device_started", {"device": self.device_name, "time": datetime.now()})
        print(f"🚀 {self.device_name} v{self.version} started!")
        return self._main_loop()
    
    def stop(self):
        """Stop the embedded device."""
        self.is_running = False
        self.emit("device_stopped", {"device": self.device_name, "time": datetime.now()})
        print(f"🛑 {self.device_name} stopped!")
    
    def _main_loop(self):
        """Main device loop (placeholder for actual implementation)."""
        while self.is_running:
            self._update_sensors()
            self._process_events()
            time.sleep(0.1)  # 100ms loop
        return True
    
    def _update_sensors(self):
        """Update all sensors."""
        for name, sensor in self.sensors.items():
            if hasattr(sensor, 'read'):
                try:
                    value = sensor.read()
                    self.emit(f"sensor_{name}", {"sensor": name, "value": value})
                except Exception as e:
                    self.emit("sensor_error", {"sensor": name, "error": str(e)})
    
    def _process_events(self):
        """Process pending events."""
        # Placeholder for event processing
        pass


class Sensor:
    """Base sensor class."""
    
    def __init__(self, name: str, pin: int = None):
        """Initialize sensor."""
        self.name = name
        self.pin = pin
        self.last_reading = None
        self.last_update = None
        
    def read(self):
        """Read sensor value (to be implemented by subclasses)."""
        raise NotImplementedError("Sensor must implement read method")
    
    def calibrate(self):
        """Calibrate sensor."""
        pass


class QRCodeScanner(Sensor):
    """QR Code scanner sensor."""
    
    def __init__(self, name: str = "qr_scanner"):
        """Initialize QR scanner."""
        super().__init__(name)
        self.last_scan = None
        
    def read(self):
        """Simulate QR code reading."""
        # In real implementation, this would interface with camera/scanner hardware
        # For simulation, return sample QR codes
        import random
        codes = [
            "PRODUCT:12345",
            "USER:john_doe",
            "URL:https://example.com",
            "PAYMENT:$25.99",
            None  # No scan
        ]
        scan_result = random.choice(codes)
        if scan_result:
            self.last_scan = {"code": scan_result, "timestamp": datetime.now()}
            return scan_result
        return None


class BarcodeScanner(Sensor):
    """Barcode scanner sensor."""
    
    def __init__(self, name: str = "barcode_scanner"):
        """Initialize barcode scanner."""
        super().__init__(name)
        self.last_scan = None
        
    def read(self):
        """Simulate barcode reading."""
        import random
        barcodes = [
            "1234567890123",  # Sample UPC
            "9781234567890",  # Sample ISBN
            "0123456789012",  # Sample EAN
            None  # No scan
        ]
        scan_result = random.choice(barcodes)
        if scan_result:
            self.last_scan = {"barcode": scan_result, "timestamp": datetime.now()}
            return scan_result
        return None


class Display:
    """Base display class."""
    
    def __init__(self, name: str, width: int = 128, height: int = 64):
        """Initialize display."""
        self.name = name
        self.width = width
        self.height = height
        self.buffer = []
        
    def clear(self):
        """Clear display."""
        self.buffer = []
        print(f"📺 {self.name}: [CLEARED]")
        
    def print(self, text: str, line: int = 0):
        """Print text to display."""
        while len(self.buffer) <= line:
            self.buffer.append("")
        self.buffer[line] = text
        print(f"📺 {self.name}: {text}")
        
    def show_menu(self, items: List[str], selected: int = 0):
        """Show menu on display."""
        self.clear()
        for i, item in enumerate(items):
            prefix = "► " if i == selected else "  "
            self.print(f"{prefix}{item}", i)


class PaymentTerminal:
    """Payment terminal for POS systems."""
    
    def __init__(self, name: str = "payment_terminal"):
        """Initialize payment terminal."""
        self.name = name
        self.is_ready = True
        self.transaction_history = []
        
    def process_payment(self, amount: float, method: str = "card"):
        """Process a payment."""
        transaction = {
            "id": len(self.transaction_history) + 1,
            "amount": amount,
            "method": method,
            "timestamp": datetime.now(),
            "status": "approved"  # Simulate approval
        }
        
        self.transaction_history.append(transaction)
        print(f"💳 Payment processed: ${amount:.2f} via {method}")
        return transaction
    
    def refund(self, transaction_id: int):
        """Process a refund."""
        for transaction in self.transaction_history:
            if transaction["id"] == transaction_id:
                refund = {
                    "id": len(self.transaction_history) + 1,
                    "amount": -transaction["amount"],
                    "method": "refund",
                    "original_transaction": transaction_id,
                    "timestamp": datetime.now(),
                    "status": "approved"
                }
                self.transaction_history.append(refund)
                print(f"💸 Refund processed: ${-refund['amount']:.2f}")
                return refund
        return None


class InventoryService:
    """Inventory management service."""
    
    def __init__(self):
        """Initialize inventory service."""
        self.items = {}
        self.transactions = []
        
    def add_item(self, barcode: str, name: str, price: float, quantity: int = 0):
        """Add item to inventory."""
        self.items[barcode] = {
            "name": name,
            "price": price,
            "quantity": quantity,
            "last_updated": datetime.now()
        }
        
    def get_item(self, barcode: str):
        """Get item by barcode."""
        return self.items.get(barcode)
    
    def update_quantity(self, barcode: str, quantity_change: int):
        """Update item quantity."""
        if barcode in self.items:
            self.items[barcode]["quantity"] += quantity_change
            self.items[barcode]["last_updated"] = datetime.now()
            
            self.transactions.append({
                "barcode": barcode,
                "quantity_change": quantity_change,
                "timestamp": datetime.now()
            })
            
    def get_low_stock_items(self, threshold: int = 10):
        """Get items with low stock."""
        return {k: v for k, v in self.items.items() if v["quantity"] <= threshold}


class WiFiService:
    """WiFi connectivity service."""
    
    def __init__(self):
        """Initialize WiFi service."""
        self.is_connected = False
        self.network_name = None
        self.signal_strength = 0
        
    def connect(self, ssid: str, password: str):
        """Connect to WiFi network."""
        # Simulate connection
        self.is_connected = True
        self.network_name = ssid
        self.signal_strength = 85  # Simulate good signal
        print(f"📶 Connected to WiFi: {ssid}")
        return True
    
    def disconnect(self):
        """Disconnect from WiFi."""
        self.is_connected = False
        self.network_name = None
        self.signal_strength = 0
        print("📶 WiFi disconnected")
    
    def get_status(self):
        """Get WiFi status."""
        return {
            "connected": self.is_connected,
            "network": self.network_name,
            "signal_strength": self.signal_strength
        }


class BluetoothService:
    """Bluetooth connectivity service."""
    
    def __init__(self):
        """Initialize Bluetooth service."""
        self.is_enabled = False
        self.paired_devices = []
        self.connected_device = None
        
    def enable(self):
        """Enable Bluetooth."""
        self.is_enabled = True
        print("📱 Bluetooth enabled")
        
    def disable(self):
        """Disable Bluetooth."""
        self.is_enabled = False
        self.connected_device = None
        print("📱 Bluetooth disabled")
        
    def pair_device(self, device_name: str, device_id: str):
        """Pair with a Bluetooth device."""
        if self.is_enabled:
            device = {"name": device_name, "id": device_id}
            self.paired_devices.append(device)
            print(f"📱 Paired with {device_name}")
            return True
        return False
    
    def connect_device(self, device_id: str):
        """Connect to paired device."""
        for device in self.paired_devices:
            if device["id"] == device_id:
                self.connected_device = device
                print(f"📱 Connected to {device['name']}")
                return True
        return False


class CloudService:
    """Cloud connectivity and data sync service."""
    
    def __init__(self, api_endpoint: str = "https://api.ludwig-embedded.com"):
        """Initialize cloud service."""
        self.api_endpoint = api_endpoint
        self.is_connected = False
        self.device_id = None
        self.sync_queue = []
        
    def authenticate(self, device_id: str, api_key: str):
        """Authenticate with cloud service."""
        # Simulate authentication
        self.device_id = device_id
        self.is_connected = True
        print(f"☁️ Connected to cloud service")
        return True
    
    def sync_data(self, data: Dict[str, Any]):
        """Sync data to cloud."""
        if self.is_connected:
            self.sync_queue.append({
                "data": data,
                "timestamp": datetime.now()
            })
            print(f"☁️ Data synced to cloud")
            return True
        else:
            # Queue for later sync
            self.sync_queue.append({
                "data": data,
                "timestamp": datetime.now()
            })
            print(f"📥 Data queued for sync (offline)")
            return False
    
    def get_updates(self):
        """Get updates from cloud."""
        if self.is_connected:
            # Simulate receiving updates
            return {
                "firmware_update": False,
                "config_updates": {},
                "messages": []
            }
        return None


# Application Templates

class POSSystem(EmbeddedDevice):
    """Point of Sale system template."""
    
    def __init__(self):
        """Initialize POS system."""
        super().__init__("Ludwig POS System", "1.0.0")
        
        # Add hardware components
        self.add_sensor("barcode_scanner", BarcodeScanner())
        self.add_sensor("qr_scanner", QRCodeScanner())
        self.display = Display("pos_display", 240, 320)
        self.payment_terminal = PaymentTerminal()
        
        # Add services
        self.add_service("inventory", InventoryService())
        self.add_service("wifi", WiFiService())
        self.add_service("cloud", CloudService())
        
        # Current transaction
        self.current_transaction = []
        self.total = 0.0
        
        # Set up event handlers
        self.on("sensor_barcode_scanner", self._handle_barcode_scan)
        self.on("sensor_qr_scanner", self._handle_qr_scan)
        
    def _handle_barcode_scan(self, data):
        """Handle barcode scan."""
        barcode = data["value"]
        if barcode:
            inventory = self.get_service("inventory")
            item = inventory.get_item(barcode)
            if item:
                self.add_item_to_transaction(barcode, item)
            else:
                self.display.print(f"Item not found: {barcode}")
    
    def _handle_qr_scan(self, data):
        """Handle QR code scan."""
        qr_code = data["value"]
        if qr_code and qr_code.startswith("PAYMENT:"):
            amount = float(qr_code.split("$")[1])
            self.process_payment(amount, "qr_payment")
    
    def add_item_to_transaction(self, barcode: str, item: Dict[str, Any]):
        """Add item to current transaction."""
        self.current_transaction.append({
            "barcode": barcode,
            "name": item["name"],
            "price": item["price"],
            "quantity": 1
        })
        self.total += item["price"]
        self.display.print(f"Added: {item['name']} - ${item['price']:.2f}")
        self.display.print(f"Total: ${self.total:.2f}", 1)
    
    def process_payment(self, amount: float, method: str = "card"):
        """Process payment for current transaction."""
        if amount >= self.total:
            transaction = self.payment_terminal.process_payment(self.total, method)
            
            # Update inventory
            inventory = self.get_service("inventory")
            for item in self.current_transaction:
                inventory.update_quantity(item["barcode"], -item["quantity"])
            
            # Sync to cloud
            cloud = self.get_service("cloud")
            cloud.sync_data({
                "transaction": transaction,
                "items": self.current_transaction
            })
            
            # Clear transaction
            self.current_transaction = []
            self.total = 0.0
            self.display.print("Payment Complete!")
            return transaction
        else:
            self.display.print("Insufficient payment amount")
            return None


class QRKioskSystem(EmbeddedDevice):
    """QR Code kiosk system template."""
    
    def __init__(self):
        """Initialize QR kiosk system."""
        super().__init__("Ludwig QR Kiosk", "1.0.0")
        
        # Add hardware
        self.add_sensor("qr_scanner", QRCodeScanner())
        self.display = Display("kiosk_display", 480, 800)
        
        # Add services
        self.add_service("wifi", WiFiService())
        self.add_service("cloud", CloudService())
        
        # Kiosk state
        self.current_screen = "welcome"
        self.user_session = None
        
        # Event handlers
        self.on("sensor_qr_scanner", self._handle_qr_scan)
        
    def _handle_qr_scan(self, data):
        """Handle QR code scans."""
        qr_code = data["value"]
        if qr_code:
            if qr_code.startswith("USER:"):
                user_id = qr_code.split(":")[1]
                self.start_user_session(user_id)
            elif qr_code.startswith("URL:"):
                url = qr_code.split(":", 1)[1]
                self.display_content(url)
    
    def start_user_session(self, user_id: str):
        """Start user session."""
        self.user_session = {
            "user_id": user_id,
            "start_time": datetime.now()
        }
        self.display.print(f"Welcome, {user_id}!")
        self.current_screen = "menu"
    
    def display_content(self, url: str):
        """Display content from URL."""
        self.display.print(f"Loading: {url}")
        # In real implementation, would fetch and display content


class InventoryScanner(EmbeddedDevice):
    """Inventory scanning system template."""
    
    def __init__(self):
        """Initialize inventory scanner."""
        super().__init__("Ludwig Inventory Scanner", "1.0.0")
        
        # Add hardware
        self.add_sensor("barcode_scanner", BarcodeScanner())
        self.display = Display("scanner_display")
        
        # Add services
        self.add_service("inventory", InventoryService())
        self.add_service("wifi", WiFiService())
        self.add_service("cloud", CloudService())
        
        # Scanner state
        self.scan_mode = "count"  # count, add, remove
        self.scanned_items = []
        
        # Event handlers
        self.on("sensor_barcode_scanner", self._handle_barcode_scan)
        
    def _handle_barcode_scan(self, data):
        """Handle barcode scans."""
        barcode = data["value"]
        if barcode:
            inventory = self.get_service("inventory")
            item = inventory.get_item(barcode)
            
            if item:
                self.scanned_items.append({
                    "barcode": barcode,
                    "name": item["name"],
                    "timestamp": datetime.now()
                })
                self.display.print(f"Scanned: {item['name']}")
                
                # Sync to cloud
                cloud = self.get_service("cloud")
                cloud.sync_data({
                    "scan": {
                        "barcode": barcode,
                        "mode": self.scan_mode,
                        "timestamp": datetime.now()
                    }
                })
    
    def set_scan_mode(self, mode: str):
        """Set scanning mode."""
        self.scan_mode = mode
        self.display.print(f"Mode: {mode.title()}")


class SmartHomeSystem(EmbeddedDevice):
    """Smart home automation system."""
    
    def __init__(self):
        super().__init__("Smart Home System", "1.0.0")
        
        # Add sensors
        self.add_sensor("temperature", TemperatureSensor())
        self.add_sensor("motion", MotionSensor())
        self.add_sensor("light", LightSensor())
        
        # Add display
        self.display = Display("SmartHome Display")
        self.add_actuator("display", self.display)
        
        # Add services
        self.add_service("wifi", WiFiService())
        self.add_service("cloud", CloudService())
        
        # Smart home state
        self.devices = {}
        self.automation_rules = []
        self.is_armed = False
        
        # Event handlers
        self.on("sensor_motion", self._handle_motion)
        self.on("sensor_temperature", self._handle_temperature)
        
    def add_device(self, device_id: str, device_config: dict):
        """Add a smart device."""
        self.devices[device_id] = {
            "config": device_config,
            "state": "online",
            "last_update": datetime.now()
        }
        self.display.print(f"Device added: {device_id}")
        
    def _handle_motion(self, data):
        """Handle motion detection."""
        if data["detected"]:
            if self.is_armed:
                self.display.print("⚠️ Motion detected!")
                cloud = self.get_service("cloud")
                cloud.sync_data({
                    "alert": {
                        "type": "motion",
                        "timestamp": datetime.now(),
                        "armed": self.is_armed
                    }
                })
                
    def _handle_temperature(self, data):
        """Handle temperature changes."""
        temp = data["value"]
        if "thermostat" in self.devices:
            target = self.devices["thermostat"]["config"].get("target_temp", 22)
            if abs(temp - target) > 2:
                self.display.print(f"Temperature: {temp}°C (target: {target}°C)")
                
    def start_automation(self):
        """Start home automation."""
        self.start()
        self.display.print("Home automation active")
        
    def arm_system(self):
        """Arm security system."""
        self.is_armed = True
        self.display.print("Security system ARMED")
        
    def disarm_system(self):
        """Disarm security system."""
        self.is_armed = False
        self.display.print("Security system DISARMED")


class RoboticsSystem(EmbeddedDevice):
    """Robotics control system."""
    
    def __init__(self):
        super().__init__("Robotics System", "1.0.0")
        
        # Add sensors
        self.add_sensor("ultrasonic", UltrasonicSensor())
        self.add_sensor("gyroscope", GyroscopeSensor())
        self.add_sensor("accelerometer", AccelerometerSensor())
        
        # Add actuators
        self.add_actuator("motors", MotorController())
        self.add_actuator("servo", ServoController())
        self.display = Display("Robot Display")
        self.add_actuator("display", self.display)
        
        # Add services
        self.add_service("bluetooth", BluetoothService())
        
        # Robot state
        self.position = {"x": 0, "y": 0, "heading": 0}
        self.is_moving = False
        self.autonomous_mode = False
        
        # Event handlers
        self.on("sensor_ultrasonic", self._handle_obstacle)
        
    def initialize_hardware(self):
        """Initialize robot hardware."""
        self.display.print("Initializing hardware...")
        
        # Calibrate sensors
        gyro = self.get_sensor("gyroscope")
        gyro.calibrate()
        
        # Test motors
        motors = self.get_actuator("motors")
        motors.test()
        
        self.display.print("Hardware ready")
        
    def move_forward(self, distance: float = 10.0):
        """Move robot forward."""
        if not self.is_moving:
            self.is_moving = True
            motors = self.get_actuator("motors")
            motors.move_forward(distance)
            self.display.print(f"Moving forward {distance}cm")
            
    def turn_left(self, angle: float = 90.0):
        """Turn robot left."""
        motors = self.get_actuator("motors")
        motors.turn_left(angle)
        self.position["heading"] = (self.position["heading"] - angle) % 360
        self.display.print(f"Turned left {angle}°")
        
    def turn_right(self, angle: float = 90.0):
        """Turn robot right."""
        motors = self.get_actuator("motors")
        motors.turn_right(angle)
        self.position["heading"] = (self.position["heading"] + angle) % 360
        self.display.print(f"Turned right {angle}°")
        
    def stop(self):
        """Stop robot movement."""
        motors = self.get_actuator("motors")
        motors.stop()
        self.is_moving = False
        self.display.print("Stopped")
        
    def _handle_obstacle(self, data):
        """Handle obstacle detection."""
        distance = data["distance"]
        safety_distance = self.config.get("safety_distance", 30)
        
        if distance < safety_distance and self.is_moving:
            self.stop()
            self.display.print(f"Obstacle detected at {distance}cm")
            
    def enable_autonomous_mode(self):
        """Enable autonomous navigation."""
        self.autonomous_mode = True
        self.display.print("Autonomous mode ON")
        
    def disable_autonomous_mode(self):
        """Disable autonomous navigation."""
        self.autonomous_mode = False
        self.display.print("Autonomous mode OFF")


# Additional sensor classes for advanced systems
class TemperatureSensor(Sensor):
    """Temperature sensor."""
    
    def __init__(self):
        super().__init__("temperature")
        
    def read_value(self):
        # Simulate temperature reading
        import random
        return random.uniform(18.0, 26.0)


class MotionSensor(Sensor):
    """Motion detection sensor."""
    
    def __init__(self):
        super().__init__("motion")
        
    def read_value(self):
        # Simulate motion detection
        import random
        return random.choice([True, False])


class LightSensor(Sensor):
    """Light intensity sensor."""
    
    def __init__(self):
        super().__init__("light")
        
    def read_value(self):
        # Simulate light reading (0-1000 lux)
        import random
        return random.randint(0, 1000)


class UltrasonicSensor(Sensor):
    """Ultrasonic distance sensor."""
    
    def __init__(self):
        super().__init__("ultrasonic")
        
    def read_value(self):
        # Simulate distance reading (in cm)
        import random
        return random.randint(5, 200)


class GyroscopeSensor(Sensor):
    """Gyroscope sensor."""
    
    def __init__(self):
        super().__init__("gyroscope")
        self.calibrated = False
        
    def calibrate(self):
        """Calibrate gyroscope."""
        self.calibrated = True
        
    def read_value(self):
        # Simulate gyroscope reading (degrees/second)
        import random
        return {"x": random.uniform(-10, 10), "y": random.uniform(-10, 10), "z": random.uniform(-10, 10)}


class AccelerometerSensor(Sensor):
    """Accelerometer sensor."""
    
    def __init__(self):
        super().__init__("accelerometer")
        
    def read_value(self):
        # Simulate accelerometer reading (g-force)
        import random
        return {"x": random.uniform(-2, 2), "y": random.uniform(-2, 2), "z": random.uniform(-2, 2)}


# Additional actuator classes
class MotorController:
    """Motor controller for robotics."""
    
    def __init__(self):
        self.speed = 0
        self.direction = "stop"
        
    def test(self):
        """Test motor functionality."""
        pass
        
    def move_forward(self, distance: float):
        """Move forward specified distance."""
        self.direction = "forward"
        self.speed = 50
        
    def move_backward(self, distance: float):
        """Move backward specified distance."""
        self.direction = "backward"
        self.speed = 50
        
    def turn_left(self, angle: float):
        """Turn left by specified angle."""
        self.direction = "left"
        
    def turn_right(self, angle: float):
        """Turn right by specified angle."""
        self.direction = "right"
        
    def stop(self):
        """Stop motors."""
        self.direction = "stop"
        self.speed = 0


class ServoController:
    """Servo motor controller."""
    
    def __init__(self):
        self.angle = 90
        
    def set_angle(self, angle: float):
        """Set servo angle."""
        self.angle = max(0, min(180, angle))
