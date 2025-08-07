import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from tkinter.font import Font

class FileMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Merger")
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
        
        # Configure font for the output
        self.output_font = Font(family="Consolas", size=10)

    def create_input_section(self):
        """Create the input controls section"""
        input_frame = ttk.Frame(self.mainframe)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Directory Selection
        dir_frame = ttk.Frame(input_frame)
        dir_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(dir_frame, text="Source Directory:").pack(side=tk.LEFT)
        
        self.dir_entry = ttk.Entry(dir_frame, width=50)
        self.dir_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        # Set default source directory
        preferred_dir = r"E:\coding\Temp Text\Temp Files"
        default_source_path = preferred_dir if os.path.exists(preferred_dir) else os.getcwd()
        self.dir_entry.insert(0, default_source_path)
        
        browse_btn = ttk.Button(dir_frame, text="Browse...", command=self.browse_directory)
        browse_btn.pack(side=tk.LEFT)
        
        # Output File Selection
        output_frame = ttk.Frame(input_frame)
        output_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(output_frame, text="Output File:").pack(side=tk.LEFT)
        
        self.output_entry = ttk.Entry(output_frame)
        self.output_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        # Set default output path based on directory availability
        preferred_dir = r"E:\coding\Temp Text"
        filename = "merged_files.txt"

        if os.path.exists(preferred_dir):
            default_output_path = os.path.join(preferred_dir, filename)
        else:
            default_output_path = os.path.join(os.getcwd(), filename)

        self.output_entry.insert(0, default_output_path)
        
        output_browse_btn = ttk.Button(output_frame, text="Browse...", command=self.browse_output_file)
        output_browse_btn.pack(side=tk.LEFT)
        
        # Options Frame
        options_frame = ttk.Frame(input_frame)
        options_frame.pack(fill=tk.X, pady=5)
        
        self.include_binary = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            options_frame, 
            text="Attempt to include binary files", 
            variable=self.include_binary
        ).pack(side=tk.LEFT, padx=5)
        
        self.prepend_filename = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            options_frame, 
            text="Prepend filename headers", 
            variable=self.prepend_filename
        ).pack(side=tk.LEFT, padx=5)
        
        # Action Buttons
        btn_frame = ttk.Frame(input_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        merge_btn = ttk.Button(btn_frame, text="Merge Files", command=self.merge_files)
        merge_btn.pack(side=tk.LEFT, padx=2)
        
        clear_btn = ttk.Button(btn_frame, text="Clear Output", command=self.clear_output)
        clear_btn.pack(side=tk.LEFT, padx=2)
        
        open_btn = ttk.Button(btn_frame, text="Open Result", command=self.open_result)
        open_btn.pack(side=tk.LEFT, padx=2)

    def create_output_section(self):
        """Create the output display section"""
        output_frame = ttk.Frame(self.mainframe)
        output_frame.pack(fill=tk.BOTH, expand=True)
        
        # Add scrollable text area
        self.output = scrolledtext.ScrolledText(
            output_frame,
            wrap=tk.WORD,
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

    def browse_output_file(self):
        """Open save file dialog"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, file_path)

    def merge_files(self):
        """Handle file merging"""
        directory = self.dir_entry.get()
        output_file = self.output_entry.get()
        
        if not directory:
            messagebox.showerror("Error", "Please select a source directory")
            return
            
        if not output_file:
            messagebox.showerror("Error", "Please specify an output file")
            return
            
        self.output.delete(1.0, tk.END)
        self.status_var.set("Merging files...")
        self.root.update_idletasks()  # Update UI
        
        try:
            # Get all files in the directory
            files = [f for f in os.listdir(directory) 
                    if os.path.isfile(os.path.join(directory, f))]
            
            if not files:
                messagebox.showwarning("Warning", "No files found in the directory")
                self.status_var.set("No files found")
                return
            
            with open(output_file, 'w', encoding='utf-8') as outfile:
                for filename in files:
                    filepath = os.path.join(directory, filename)
                    
                    # Write the filename header if enabled
                    if self.prepend_filename.get():
                        outfile.write(f"\n{'='*50}\n")
                        outfile.write(f"FILE: {filename}\n")
                        outfile.write(f"{'='*50}\n\n")
                    
                    # Write the file content
                    try:
                        if self.include_binary.get():
                            # Try reading as binary if enabled
                            with open(filepath, 'rb') as infile:
                                content = infile.read()
                                try:
                                    outfile.write(content.decode('utf-8'))
                                except UnicodeDecodeError:
                                    outfile.write("[Binary content - displayed as text may be corrupted]\n")
                                    outfile.write(str(content))
                        else:
                            # Read as text only
                            with open(filepath, 'r', encoding='utf-8') as infile:
                                outfile.write(infile.read())
                        
                        outfile.write("\n\n")
                        
                    except Exception as e:
                        outfile.write(f"[Error reading file: {str(e)}]\n\n")
            
            # Display the merged content
            with open(output_file, 'r', encoding='utf-8') as f:
                self.output.insert(tk.END, f.read())
            
            self.status_var.set(f"Successfully merged {len(files)} files into {output_file}")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.status_var.set(f"Error: {str(e)}")
            self.output.insert(tk.END, f"Error: {str(e)}")

    def clear_output(self):
        """Clear the output window"""
        self.output.delete(1.0, tk.END)
        self.status_var.set("Output cleared")

    def open_result(self):
        """Open the result file in default editor"""
        output_file = self.output_entry.get()
        if output_file and os.path.exists(output_file):
            try:
                os.startfile(output_file)
            except Exception as e:
                messagebox.showerror("Error", f"Could not open file: {str(e)}")
        else:
            messagebox.showwarning("Warning", "Output file doesn't exist yet")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileMergerApp(root)
    root.mainloop()