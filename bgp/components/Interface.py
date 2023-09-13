
class Interface:
    def __init__(self, name, ip_address, autonomous_system):
        self.name = name
        self.ip_address = ip_address
        self.autonomous_system = autonomous_system
        
    def __str__(self):
        return f"Name: {self.name}, IP Address: {self.ip_address}, Autonomous System: {self.autonomous_system}"