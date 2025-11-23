"""
saunis server swapper
Portable application to change game server for Rainbow Six Siege accounts
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import os
import sys
from pathlib import Path
from ubisoft_id_fetcher import get_ubisoft_id_from_username
from game_settings_manager import find_game_settings_files, update_server_setting



class ServerChangerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("saunis server swapper")
        self.root.geometry("600x550")
        self.root.resizable(False, False)
        
        # Dark mode color scheme with purple accent
        self.colors = {
            'bg': '#1e1e1e',
            'fg': '#e0e0e0',
            'frame_bg': '#2d2d2d',
            'entry_bg': '#3a3a3a',
            'entry_fg': '#ffffff',
            'button_bg': '#7b2cbf',
            'button_hover': '#9d4edd',
            'button_active': '#5a189a',
            'accent': '#9d4edd',
            'text_bg': '#252525',
            'text_fg': '#d4d4d4',
            'border': '#404040',
            'success': '#4caf50',
            'error': '#f44336'
        }
        
        # Configure root background
        self.root.configure(bg=self.colors['bg'])
        
        # Server mapping
        self.server_map = {
            "Default": "default",
            "US-West": "playfab/westus",
            "US-Central": "playfab/centralus",
            "US-South-Central": "playfab/southcentralus",
            "East-US": "playfab/eastus",
            "Brazil": "playfab/brazilsouth",
            "EU-North": "playfab/northeurope",
            "EU-West": "playfab/westeurope",
            "UAE": "playfab/uaenorth",
            "South Africa": "playfab/southafricanorth",
            "Asia-East": "playfab/eastasia",
            "Asia-Southeast": "playfab/southeastasia",
            "Japan": "playfab/japaneast",
            "Australia": "playfab/australiaeast"
        }
        
        self.setup_dark_theme()
        self.setup_ui()
        self.setup_text_tags()
    
    def setup_dark_theme(self):
        """Configure dark theme styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure base frame style
        style.configure('Dark.TFrame', background=self.colors['bg'])
        style.configure('Dark.TLabel', background=self.colors['bg'], foreground=self.colors['fg'])
        style.configure('Dark.TEntry', fieldbackground=self.colors['entry_bg'], 
                       foreground=self.colors['entry_fg'], bordercolor=self.colors['border'],
                       insertcolor=self.colors['fg'], borderwidth=1)
        style.map('Dark.TEntry', 
                 bordercolor=[('focus', self.colors['accent'])],
                 lightcolor=[('focus', self.colors['accent'])],
                 darkcolor=[('focus', self.colors['accent'])])
        style.configure('Dark.TCombobox', fieldbackground=self.colors['entry_bg'],
                       foreground=self.colors['entry_fg'], bordercolor=self.colors['border'],
                       arrowcolor=self.colors['fg'], borderwidth=1)
        style.map('Dark.TCombobox',
                 fieldbackground=[('readonly', self.colors['entry_bg'])],
                 bordercolor=[('focus', self.colors['accent'])],
                 lightcolor=[('focus', self.colors['accent'])],
                 darkcolor=[('focus', self.colors['accent'])])
        style.configure('Dark.TButton', background=self.colors['button_bg'],
                      foreground='white', borderwidth=0, focuscolor='none',
                      font=('Consolas', 10, 'bold'), padding=10)
        style.map('Dark.TButton',
                 background=[('active', self.colors['button_hover']),
                           ('pressed', self.colors['button_active'])],
                 foreground=[('active', 'white')])
        style.configure('Dark.TCheckbutton', background=self.colors['bg'],
                       foreground=self.colors['fg'], focuscolor='none')
        style.map('Dark.TCheckbutton',
                 background=[('active', self.colors['bg'])],
                 foreground=[('active', self.colors['fg'])])
    
    def setup_ui(self):
        # Main container with padding
        main_frame = tk.Frame(self.root, bg=self.colors['bg'], padx=25, pady=25)
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title with accent color - using Consolas for a more unique font
        title_label = tk.Label(main_frame, text="saunis", 
                              font=("Consolas", 24, "bold"),
                              bg=self.colors['bg'], fg=self.colors['accent'])
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 2))
        
        subtitle_label = tk.Label(main_frame, text="server swapper", 
                                  font=("Consolas", 14),
                                  bg=self.colors['bg'], fg=self.colors['fg'])
        subtitle_label.grid(row=1, column=0, columnspan=2, pady=(0, 2))
        
        tagline_label = tk.Label(main_frame, text="(i dont make uis)", 
                                font=("Consolas", 10, "italic"),
                                bg=self.colors['bg'], fg=self.colors['fg'])
        tagline_label.grid(row=2, column=0, columnspan=2, pady=(0, 25))
        
        # Username section
        username_frame = tk.LabelFrame(main_frame, text="Ubisoft Username", 
                                       bg=self.colors['bg'], fg=self.colors['accent'],
                                       font=('Consolas', 9, 'bold'),
                                       padx=15, pady=15,
                                       relief=tk.FLAT, bd=1,
                                       highlightbackground=self.colors['border'],
                                       highlightthickness=1)
        username_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        username_inner = tk.Frame(username_frame, bg=self.colors['bg'])
        username_inner.pack(fill=tk.BOTH, expand=True)
        
        self.username_var = tk.StringVar()
        self.username_entry = ttk.Entry(username_inner, textvariable=self.username_var, 
                                       style='Dark.TEntry', width=32, font=('Consolas', 10))
        self.username_entry.pack(side=tk.LEFT, padx=(0, 15))
        
        self.skip_username_var = tk.BooleanVar()
        skip_checkbox = ttk.Checkbutton(username_inner, text="Skip (Change all accounts)", 
                                        variable=self.skip_username_var,
                                        command=self.on_skip_toggle,
                                        style='Dark.TCheckbutton')
        skip_checkbox.pack(side=tk.LEFT)
        
        # Server selection
        server_frame = tk.LabelFrame(main_frame, text="Select Server", 
                                     bg=self.colors['bg'], fg=self.colors['accent'],
                                     font=('Consolas', 9, 'bold'),
                                     padx=15, pady=15,
                                     relief=tk.FLAT, bd=1,
                                     highlightbackground=self.colors['border'],
                                     highlightthickness=1)
        server_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        self.server_var = tk.StringVar(value="Default")
        server_combo = ttk.Combobox(server_frame, textvariable=self.server_var, 
                                   values=list(self.server_map.keys()), 
                                   state="readonly", width=29, style='Dark.TCombobox',
                                   font=('Consolas', 10))
        server_combo.pack()
        
        # Action button with accent styling
        button_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        button_frame.grid(row=5, column=0, columnspan=2, pady=(0, 20))
        
        self.change_button = ttk.Button(button_frame, text="Change Server", 
                                        command=self.on_change_server, 
                                        style='Dark.TButton', width=25)
        self.change_button.pack()
        
        # Status/log area
        log_frame = tk.LabelFrame(main_frame, text="Status Log", 
                                  bg=self.colors['bg'], fg=self.colors['accent'],
                                  font=('Consolas', 9, 'bold'),
                                  padx=10, pady=10,
                                  relief=tk.FLAT, bd=1,
                                  highlightbackground=self.colors['border'],
                                  highlightthickness=1)
        log_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Custom styled text widget
        self.log_text = scrolledtext.ScrolledText(log_frame, height=12, width=55, 
                                                  state=tk.DISABLED, wrap=tk.WORD,
                                                  bg=self.colors['text_bg'],
                                                  fg=self.colors['text_fg'],
                                                  font=('Consolas', 9),
                                                  insertbackground=self.colors['accent'],
                                                  selectbackground=self.colors['accent'],
                                                  selectforeground='white',
                                                  relief=tk.FLAT,
                                                  borderwidth=0,
                                                  padx=10, pady=10)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(6, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
    
    def on_skip_toggle(self):
        """Enable/disable username entry based on skip checkbox"""
        if self.skip_username_var.get():
            self.username_var.set("")
            self.username_entry.config(state="disabled")
            # Update style for disabled state
            style = ttk.Style()
            style.map('Dark.TEntry',
                     fieldbackground=[('disabled', self.colors['frame_bg'])],
                     foreground=[('disabled', '#808080')])
        else:
            self.username_entry.config(state="normal")
            # Reset to normal style
            style = ttk.Style()
            style.map('Dark.TEntry',
                     fieldbackground=[('!disabled', self.colors['entry_bg'])],
                     foreground=[('!disabled', self.colors['entry_fg'])])
    
    def log(self, message):
        """Add message to log area with color coding"""
        self.log_text.config(state=tk.NORMAL)
        
        # Color code messages
        if message.startswith("✓") or "SUCCESS" in message:
            self.log_text.insert(tk.END, message + "\n", "success")
        elif message.startswith("✗") or "ERROR" in message or "FAILED" in message:
            self.log_text.insert(tk.END, message + "\n", "error")
        elif "=" in message and len(message) > 10:  # Separator lines
            self.log_text.insert(tk.END, message + "\n", "separator")
        else:
            self.log_text.insert(tk.END, message + "\n")
        
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.root.update()
    
    def setup_text_tags(self):
        """Configure text color tags"""
        self.log_text.tag_config("success", foreground=self.colors['success'])
        self.log_text.tag_config("error", foreground=self.colors['error'])
        self.log_text.tag_config("separator", foreground=self.colors['accent'])
    
    def on_change_server(self):
        """Handle server change button click"""
        username = self.username_var.get().strip()
        skip_username = self.skip_username_var.get()
        selected_server = self.server_var.get()
        
        if not skip_username and not username:
            messagebox.showwarning("Warning", "Please enter a Ubisoft username or select 'Skip' to change all accounts.")
            return
        
        # Disable button during operation
        self.change_button.config(state="disabled")
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
        
        # Update button text to show processing
        self.change_button.config(text="Processing...")
        
        # Run in separate thread to avoid blocking UI
        thread = threading.Thread(target=self.change_server_thread, 
                                 args=(username, skip_username, selected_server))
        thread.daemon = True
        thread.start()
    
    def change_server_thread(self, username, skip_username, selected_server):
        """Thread function to handle server change"""
        try:
            self.log("=" * 50)
            self.log("Starting server change process...")
            self.log(f"Selected server: {selected_server}")
            self.log("=" * 50)
            
            ubisoft_id = None
            game_settings_files = []
            
            if skip_username:
                self.log("\nSkipping username lookup - will change all accounts")
                # Find all GameSettings.ini files
                game_settings_files = find_game_settings_files()
                if not game_settings_files:
                    self.log("ERROR: No GameSettings.ini files found!")
                    messagebox.showerror("Error", "No GameSettings.ini files found in:\n"
                                                "C:\\Users\\<User>\\Documents\\My Games\\Rainbow Six - Siege\\\n"
                                                "or\n"
                                                "C:\\Users\\<User>\\OneDrive\\Documents\\My Games\\Rainbow Six - Siege\\")
                    self.change_button.config(state="normal")
                    return
                self.log(f"Found {len(game_settings_files)} GameSettings.ini file(s)")
            else:
                self.log(f"\nLooking up Ubisoft ID for username: {username}")
                # Get Ubisoft ID
                ubisoft_id, success = get_ubisoft_id_from_username(username)
                
                if not success or not ubisoft_id:
                    self.log(f"ERROR: Could not acquire Ubisoft ID for username '{username}'")
                    messagebox.showerror("Error", f"Could not find Ubisoft ID for username '{username}'.\n"
                                                 "Please check the username and try again.")
                    self.change_button.config(state="normal")
                    return
                
                self.log(f"✓ Successfully acquired Ubisoft ID: {ubisoft_id}")
                
                # Find GameSettings.ini for this account
                game_settings_files = find_game_settings_files(ubisoft_id)
                if not game_settings_files:
                    self.log(f"ERROR: No GameSettings.ini file found for Ubisoft ID: {ubisoft_id}")
                    messagebox.showerror("Error", f"Could not find GameSettings.ini file for account '{username}'.\n"
                                                 f"Ubisoft ID: {ubisoft_id}\n\n"
                                                 "Please ensure the game has been launched at least once.")
                    self.change_button.config(state="normal")
                    return
                self.log(f"✓ Found GameSettings.ini file")
            
            # Update server setting in all found files
            server_value = self.server_map[selected_server]
            self.log(f"\nUpdating DataCenterHint to: {server_value}")
            
            success_count = 0
            for file_path in game_settings_files:
                try:
                    if update_server_setting(file_path, server_value):
                        self.log(f"✓ Updated: {file_path}")
                        success_count += 1
                    else:
                        self.log(f"✗ Failed to update: {file_path}")
                except Exception as e:
                    self.log(f"✗ Error updating {file_path}: {str(e)}")
            
            self.log("\n" + "=" * 50)
            if success_count > 0:
                self.log(f"SUCCESS: Updated {success_count} file(s)")
                messagebox.showinfo("Success", f"Successfully updated server setting for {success_count} account(s)!")
            else:
                self.log("FAILED: No files were updated")
                messagebox.showerror("Error", "Failed to update any GameSettings.ini files.")
            self.log("=" * 50)
            
        except Exception as e:
            self.log(f"\nERROR: {str(e)}")
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
        finally:
            self.change_button.config(state="normal", text="Change Server")


def main():
    root = tk.Tk()
    
    # Try to enable dark title bar on Windows (must be done after Tk() but before mainloop)
    if sys.platform == 'win32':
        try:
            import ctypes
            # Get the window handle using update_idletasks to ensure window exists
            root.update_idletasks()
            hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
            # Enable dark mode for title bar
            DWMWA_USE_IMMERSIVE_DARK_MODE = 20
            value = ctypes.c_int(1)
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd,
                DWMWA_USE_IMMERSIVE_DARK_MODE,
                ctypes.byref(value),
                ctypes.sizeof(value)
            )
        except Exception:
            pass
    
    app = ServerChangerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

