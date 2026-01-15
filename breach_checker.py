"""
Data Breach Checker Tool
========================
A modern GUI application to check if an email address has been exposed in data breaches.
Uses the XposedOrNot API for breach detection.

Author: Security Tools Collection
License: MIT
"""

import customtkinter as ctk
import requests
import threading
import re
from tkinter import messagebox


class DataBreachChecker:
    """Main application class for the Data Breach Checker GUI."""
    
    def __init__(self):
        """Initialize the application window and UI components."""
        # Configure appearance
        ctk.set_appearance_mode("dark")  # Dark mode for modern look
        ctk.set_default_color_theme("blue")  # Blue accent color
        
        # Create main window
        self.root = ctk.CTk()
        self.root.title("🔒 Data Breach Checker")
        self.root.geometry("700x600")  # Window size
        self.root.minsize(600, 500)  # Minimum window size
        
        # Configure grid for expansion
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(2, weight=1)  # Results section expands
        
        # Build the UI
        self._create_header()
        self._create_input_section()
        self._create_result_section()
        self._create_footer()
        
    def _create_header(self):
        """Create the header section with title and description."""
        # Header frame
        header_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)
        
        # Title label
        title_label = ctk.CTkLabel(
            header_frame,
            text="🔒 Data Breach Checker",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.grid(row=0, column=0, pady=(0, 5))
        
        # Description label
        desc_label = ctk.CTkLabel(
            header_frame,
            text="Check if your email has been exposed in data breaches",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        desc_label.grid(row=1, column=0)
        
    def _create_input_section(self):
        """Create the email input section with entry field and button."""
        # Input frame
        input_frame = ctk.CTkFrame(self.root)
        input_frame.grid(row=1, column=0, padx=20, pady=15, sticky="ew")
        input_frame.grid_columnconfigure(0, weight=1)
        
        # Email label
        email_label = ctk.CTkLabel(
            input_frame,
            text="Enter your email address:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        email_label.grid(row=0, column=0, padx=20, pady=(15, 5), sticky="w")
        
        # Email entry field
        self.email_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="example@email.com",
            width=450,
            height=45,
            font=ctk.CTkFont(size=14)
        )
        self.email_entry.grid(row=1, column=0, padx=20, pady=10)
        
        # Bind Enter key to check function
        self.email_entry.bind("<Return>", lambda e: self._check_breach())
        
        # Check button
        self.check_button = ctk.CTkButton(
            input_frame,
            text="🔍 Check for Leaks",
            font=ctk.CTkFont(size=15, weight="bold"),
            width=220,
            height=45,
            command=self._check_breach
        )
        self.check_button.grid(row=2, column=0, padx=20, pady=(10, 20))
        
    def _create_result_section(self):
        """Create the results display section."""
        # Result frame - expands to fill available space
        self.result_frame = ctk.CTkFrame(self.root)
        self.result_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        self.result_frame.grid_columnconfigure(0, weight=1)
        self.result_frame.grid_rowconfigure(2, weight=1)  # Breach list expands
        
        # Status label (shows safe/breach status)
        self.status_label = ctk.CTkLabel(
            self.result_frame,
            text="Enter an email address and click 'Check for Leaks'",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="gray"
        )
        self.status_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # Breach count label
        self.count_label = ctk.CTkLabel(
            self.result_frame,
            text="",
            font=ctk.CTkFont(size=13)
        )
        self.count_label.grid(row=1, column=0, padx=20, pady=(0, 10))
        
        # Large scrollable frame for breach list - expands to fill space
        self.breach_list_frame = ctk.CTkScrollableFrame(
            self.result_frame,
            label_text="Breached Sites",
            label_font=ctk.CTkFont(size=14, weight="bold")
        )
        self.breach_list_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.breach_list_frame.grid_columnconfigure(0, weight=1)
        # Initially hide the breach list
        self.breach_list_frame.grid_remove()
        
        # Progress bar (initially hidden)
        self.progress_bar = ctk.CTkProgressBar(self.result_frame, width=450)
        self.progress_bar.grid(row=3, column=0, padx=20, pady=10)
        self.progress_bar.grid_remove()
        
    def _create_footer(self):
        """Create the footer section with credits."""
        footer_label = ctk.CTkLabel(
            self.root,
            text="Powered by XposedOrNot API • For educational purposes only",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        footer_label.grid(row=3, column=0, padx=20, pady=(5, 15))
        
    def _validate_email(self, email: str) -> bool:
        """
        Validate email format using regex.
        
        Args:
            email: The email address to validate
            
        Returns:
            bool: True if valid email format, False otherwise
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def _clear_results(self):
        """Clear all previous results from the display."""
        self.status_label.configure(text="", text_color="white")
        self.count_label.configure(text="")
        
        # Clear breach list
        for widget in self.breach_list_frame.winfo_children():
            widget.destroy()
        self.breach_list_frame.grid_remove()
        
    def _show_loading(self, show: bool):
        """
        Show or hide the loading indicator.
        
        Args:
            show: True to show loading, False to hide
        """
        if show:
            self.progress_bar.grid()
            self.progress_bar.configure(mode="indeterminate")
            self.progress_bar.start()
            self.check_button.configure(state="disabled", text="Checking...")
        else:
            self.progress_bar.stop()
            self.progress_bar.grid_remove()
            self.check_button.configure(state="normal", text="🔍 Check for Leaks")
            
    def _check_breach(self):
        """
        Initiate the breach check process.
        Validates input and starts the API request in a separate thread.
        """
        # Get and clean email input
        email = self.email_entry.get().strip().lower()
        
        # Validate email
        if not email:
            messagebox.showwarning("Warning", "Please enter an email address!")
            return
            
        if not self._validate_email(email):
            messagebox.showwarning("Warning", "Please enter a valid email address!")
            return
        
        # Clear previous results
        self._clear_results()
        
        # Show loading indicator
        self._show_loading(True)
        
        # Start API request in separate thread to prevent GUI freeze
        thread = threading.Thread(target=self._api_request, args=(email,))
        thread.daemon = True
        thread.start()
        
    def _api_request(self, email: str):
        """
        Make the API request to XposedOrNot.
        
        Args:
            email: The email address to check
        """
        # XposedOrNot API endpoint
        api_url = f"https://api.xposedornot.com/v1/check-email/{email}"
        
        # Headers with User-Agent to avoid being blocked
        headers = {
            "User-Agent": "DataBreachChecker/1.0 (Security Tool)",
            "Accept": "application/json"
        }
        
        try:
            # Make the GET request with timeout and headers
            response = requests.get(api_url, headers=headers, timeout=15)
            
            # Process based on status code
            if response.status_code == 200:
                # Status 200 - check if there are actual breaches
                data = response.json()
                self.root.after(0, lambda: self._display_breach_results(data))
                
            elif response.status_code == 404:
                # Email not found in any breaches - it's safe!
                self.root.after(0, self._display_safe_result)
                
            else:
                # Unexpected status code
                self.root.after(0, lambda: self._display_error(
                    f"Unexpected response from server (Status: {response.status_code})"
                ))
                
        except requests.exceptions.ConnectionError:
            # No internet connection
            self.root.after(0, lambda: self._display_error(
                "No internet connection!\nPlease check your network and try again."
            ))
            
        except requests.exceptions.Timeout:
            # Request timed out
            self.root.after(0, lambda: self._display_error(
                "Request timed out!\nThe server took too long to respond."
            ))
            
        except requests.exceptions.RequestException as e:
            # Other request errors
            self.root.after(0, lambda: self._display_error(
                f"Network error occurred:\n{str(e)}"
            ))
            
        except Exception as e:
            # Catch-all for unexpected errors
            self.root.after(0, lambda: self._display_error(
                f"An unexpected error occurred:\n{str(e)}"
            ))
            
        finally:
            # Hide loading indicator
            self.root.after(0, lambda: self._show_loading(False))
            
    def _display_safe_result(self):
        """Display the result when email is not found in any breaches."""
        self.status_label.configure(
            text="✅ Safe! No breaches found.",
            text_color="#2ECC71"  # Green color
        )
        self.count_label.configure(
            text="Your email was not found in any known data breaches.",
            text_color="#2ECC71"
        )
        
    def _flatten_list(self, data) -> list:
        """
        Recursively flatten nested lists and extract all string items.
        Handles: simple lists, nested lists (list of lists), deeply nested structures.
        
        Example: [['Site1', 'Site2', 'Site3']] -> ['Site1', 'Site2', 'Site3']
        Example: ['Site1', ['Site2', 'Site3']] -> ['Site1', 'Site2', 'Site3']
        
        Args:
            data: The data to flatten (can be list, string, dict, or other)
            
        Returns:
            list: Flattened list of string items
        """
        result = []
        
        if isinstance(data, str):
            result.append(data)
            
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, str):
                    result.append(item)
                elif isinstance(item, list):
                    result.extend(self._flatten_list(item))
                elif isinstance(item, dict):
                    name = (item.get("breach") or 
                            item.get("name") or 
                            item.get("domain") or 
                            item.get("site") or
                            item.get("Name") or
                            item.get("Breach") or
                            item.get("title") or
                            None)
                    if name:
                        result.append(str(name))
                    else:
                        result.append(str(item))
                else:
                    if item is not None:
                        result.append(str(item))
                        
        elif isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, list):
                    result.extend(self._flatten_list(value))
                elif isinstance(value, str):
                    result.append(value)
                    
        return result
        
    def _display_breach_results(self, data: dict):
        """
        Display the results when email is found in breaches.
        Shows RED warning if breaches found, GREEN safe if no breaches.
        
        Args:
            data: The API response data containing breach information
        """
        breach_list = []
        
        try:
            # Check for common keys (case variations)
            possible_keys = [
                "breaches", "Breaches", "BREACHES",
                "breaches_details", "BreachesDetails",
                "ExposedBreaches", "exposed_breaches",
                "data", "Data", "results", "Results"
            ]
            
            breaches_data = None
            
            # First, check if data itself is a list
            if isinstance(data, list):
                breaches_data = data
            else:
                # Search for breach data in dictionary
                for key in possible_keys:
                    if key in data:
                        breaches_data = data[key]
                        break
                
                # If still not found, check for nested structures
                if breaches_data is None:
                    if "ExposedBreaches" in data:
                        exposed = data["ExposedBreaches"]
                        if isinstance(exposed, dict):
                            for key in ["breaches_details", "breaches", "Breaches"]:
                                if key in exposed:
                                    breaches_data = exposed[key]
                                    break
                        elif isinstance(exposed, list):
                            breaches_data = exposed
                
                # Last resort: find any list in the response
                if breaches_data is None:
                    for key, value in data.items():
                        if isinstance(value, list):
                            breaches_data = value
                            break
            
            # Flatten the data to extract all breach names
            if breaches_data is not None:
                breach_list = self._flatten_list(breaches_data)
            
        except Exception:
            pass  # If parsing fails, breach_list remains empty
        
        # Calculate breach count
        breach_count = len(breach_list)
        
        # Show appropriate result based on breach count
        if breach_count > 0:
            # Breaches found - show RED warning
            self.status_label.configure(
                text="⚠️ Warning! Breaches Found!",
                text_color="#E74C3C"
            )
            
            self.count_label.configure(
                text=f"Your email was found in {breach_count} data breach(es):",
                text_color="#E74C3C"
            )
            
            # Show the breach list frame
            self.breach_list_frame.grid()
            
            # Clear any existing items
            for widget in self.breach_list_frame.winfo_children():
                widget.destroy()
            
            # Add each breach to the list
            for i, breach in enumerate(breach_list):
                item_frame = ctk.CTkFrame(
                    self.breach_list_frame,
                    fg_color="transparent"
                )
                item_frame.grid(row=i, column=0, padx=5, pady=4, sticky="ew")
                item_frame.grid_columnconfigure(1, weight=1)
                
                num_label = ctk.CTkLabel(
                    item_frame,
                    text=f"{i+1}.",
                    font=ctk.CTkFont(size=13),
                    text_color="#E74C3C",
                    width=40
                )
                num_label.grid(row=0, column=0, padx=(10, 5), sticky="w")
                
                breach_label = ctk.CTkLabel(
                    item_frame,
                    text=f"🔴 {breach}",
                    font=ctk.CTkFont(size=14),
                    text_color="#E74C3C",
                    anchor="w"
                )
                breach_label.grid(row=0, column=1, padx=(5, 10), sticky="w")
        else:
            # No breaches found - show GREEN safe message
            self._display_safe_result()
            
    def _display_error(self, message: str):
        """
        Display an error message.
        
        Args:
            message: The error message to display
        """
        self.status_label.configure(
            text="❌ Error",
            text_color="#F39C12"
        )
        self.count_label.configure(
            text=message,
            text_color="#F39C12"
        )
        
    def run(self):
        """Start the application main loop."""
        self.root.mainloop()


# Entry point
if __name__ == "__main__":
    app = DataBreachChecker()
    app.run()
