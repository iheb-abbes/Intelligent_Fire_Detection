import tkinter as tk
from pc_system.modules.communication import CommunicationModule

class FireSystemUI:
    def __init__(self, pi_ip):
        self.comm = CommunicationModule(pi_ip)
        self.root = tk.Tk()
        self.root.title("Fire System Control Panel (4.6)")
        self.root.geometry("300x150")
        
        self.label = tk.Label(self.root, text="System Status: Monitoring", fg="blue")
        self.label.pack(pady=10)

        # The Remote Deactivation Button required by Spec 4.6
        self.stop_button = tk.Button(self.root, text="STOP ALARM / RESET", 
                                     command=self.deactivate_alarm, 
                                     bg="red", fg="white", height=2, width=20)
        self.stop_button.pack(pady=10)

    def deactivate_alarm(self):
        print("[UI] Requesting remote deactivation...")
        if self.comm.send_alert("off"):
            self.label.config(text="Status: Alarm Deactivated", fg="green")
        else:
            self.label.config(text="Status: Connection Error", fg="red")

    def run(self):
        # We use update instead of mainloop to allow it to run with OpenCV
        self.root.update()