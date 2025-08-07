# -*- coding: utf-8 -*-
import os
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from tkinter.font import Font

class DirectoryTreeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Directory Tree Generator")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # Configure styles
        self.setup_styles()
        
        # Create main container
        self.mainframe = ttk.Frame(root, padding="10")
        self.mainframe.pack(fill=tk.BOTH, expand=True)
        
        # Input Section
        self.create_input_section()
        
        # Output Section
        self.create_output_section()
        
        # Status Bar
        self.create_status_bar()
        
        # Set focus to directory entry
        self.dir_entry.focus()

    def setup_styles(self):
        """Configure custom styles for the application"""
        style = ttk.Style()
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Segoe UI', 10))
        style.configure('TButton', font=('Segoe UI', 10))
        style.configure('Status.TLabel', background='#e0e0e0', relief=tk.SUNKEN)
        
        # Configure font for the tree output
        self.output_font = Font(family="Consolas", size=10)

    def create_input_section(self):
        """Create the input controls section"""
        input_frame = ttk.Frame(self.mainframe)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Directory Selection
        dir_frame = ttk.Frame(input_frame)
        dir_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(dir_frame, text="Directory Path:").pack(side=tk.LEFT)
        
        self.dir_entry = ttk.Entry(dir_frame, width=50)
        self.dir_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        
        browse_btn = ttk.Button(dir_frame, text="Browse...", command=self.browse_directory)
        browse_btn.pack(side=tk.LEFT)
        
        # Ignore List
        ignore_frame = ttk.Frame(input_frame)
        ignore_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(ignore_frame, text="Ignore (comma separated):").pack(side=tk.LEFT)
        
        self.ignore_entry = ttk.Entry(ignore_frame)
        self.ignore_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        self.ignore_entry.insert(0, ".vs, .git, .idea, bin, obj, Migrations")
        
        # Action Buttons
        btn_frame = ttk.Frame(input_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        generate_btn = ttk.Button(btn_frame, text="Generate Tree", command=self.generate_tree)
        generate_btn.pack(side=tk.LEFT, padx=2)
        
        clear_btn = ttk.Button(btn_frame, text="Clear Output", command=self.clear_output)
        clear_btn.pack(side=tk.LEFT, padx=2)
        
        save_btn = ttk.Button(btn_frame, text="Save As...", command=self.save_output)
        save_btn.pack(side=tk.LEFT, padx=2)

    def create_output_section(self):
        """Create the output display section"""
        output_frame = ttk.Frame(self.mainframe)
        output_frame.pack(fill=tk.BOTH, expand=True)
        
        # Add scrollable text area with line numbers
        self.output = scrolledtext.ScrolledText(
            output_frame,
            wrap=tk.NONE,
            font=self.output_font,
            bg='white',
            padx=5,
            pady=5
        )
        self.output.pack(fill=tk.BOTH, expand=True)

    def create_status_bar(self):
        """Create the status bar at bottom"""
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        
        status_bar = ttk.Label(
            self.root,
            textvariable=self.status_var,
            style='Status.TLabel',
            padding=5
        )
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)

    def browse_directory(self):
        """Open directory dialog"""
        directory = filedialog.askdirectory()
        if directory:
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, directory)
            self.status_var.set(f"Selected directory: {directory}")

    def generate_directory_tree(self, directory_path, ignore_list=None, output_file=None):
        """Generate directory tree structure"""
        try:
            path = Path(directory_path)
            if not path.exists():
                return f"Error: Directory '{directory_path}' does not exist."
            
            preferred_dir = r"E:\coding\Temp Text"

            if ignore_list is None:
                ignore_list = []

            if output_file is None:
                if os.path.exists(preferred_dir):
                    output_file = os.path.join(preferred_dir, "directory_tree.txt")
                    output_file = os.path.join(os.getcwd(), "directory_tree.txt")
                else:
                    output_file = os.path.join(os.getcwd(), "directory_tree.txt")

            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"{path.name}/\n")
                self._generate_tree(path, f, ignore_list)
            
            return f"Success! Tree saved to {output_file}"
        
        except Exception as e:
            return f"Error: {str(e)}"

    def _generate_tree(self, directory, file_handler, ignore_list, prefix='', is_last=False):
        """Recursive helper to generate tree structure"""
        try:
            contents = sorted(os.listdir(directory))
        except PermissionError:
            file_handler.write(f"{prefix}\u2514\u2500\u2500 [Permission Denied]\n")
            return

        contents = [item for item in contents if item not in ignore_list]

        for i, item in enumerate(contents):
            path = directory / item
            current_is_last = i == len(contents) - 1
            
            if prefix == '':
                current_indent = '\u2514\u2500\u2500 ' if current_is_last else '\u251c\u2500\u2500 '
            else:
                current_indent = '    ' if is_last else '\u2502   '

            file_handler.write(f"{prefix}{current_indent}{item}")
            
            if path.is_dir():
                file_handler.write("/\n")
                new_prefix = prefix + ('    ' if is_last else '\u2502   ')
                self._generate_tree(path, file_handler, ignore_list, new_prefix, current_is_last)
            else:
                file_handler.write("\n")

    def generate_tree(self):
        """Handle tree generation"""
        directory = self.dir_entry.get()
        ignore_text = self.ignore_entry.get()
        ignore_list = [item.strip() for item in ignore_text.split(',')] if ignore_text else []
        
        if not directory:
            messagebox.showerror("Error", "Please select a directory")
            return
            
        self.output.delete(1.0, tk.END)
        self.status_var.set("Generating directory tree...")
        self.root.update_idletasks()  # Update UI
        
        result = self.generate_directory_tree(directory, ignore_list)
        
        # Display the generated tree
        try:
            with open("directory_tree.txt", 'r', encoding='utf-8') as f:
                tree_content = f.read()
                self.output.insert(tk.END, tree_content)
        except Exception as e:
            self.output.insert(tk.END, f"Error reading output file: {str(e)}")
        
        self.output.insert(tk.END, "\n\n" + result)
        self.status_var.set(result)
        
        # Auto-scroll to top
        self.output.see(1.0)

    def clear_output(self):
        """Clear the output window"""
        self.output.delete(1.0, tk.END)
        self.status_var.set("Output cleared")

    def save_output(self):
        """Save the current output to a file"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.output.get(1.0, tk.END))
                self.status_var.set(f"Output saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DirectoryTreeApp(root)
    root.mainloop()