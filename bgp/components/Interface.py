
class Interface:
    def __init__(self, name, ip_address, AS):
        self.name = name
        self.ip_address = ip_address
        self.AS = AS
        
    def __str__(self):
        return f"ID: {self.name} | IP: {self.ip_address} | AS: {self.AS}"