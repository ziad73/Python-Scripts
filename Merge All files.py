import os

def merge_files(directory_path, output_file="merged_files.txt"):
    """
    Merges all files in the given directory into a single output file.
    Each file's content is preceded by its filename.
    
    Args:
        directory_path (str): Path to the directory containing files to merge
        output_file (str): Name of the output file (default: "merged_files.txt")
    """
    try:
        # Get all files in the directory
        files = [f for f in os.listdir(directory_path) 
                if os.path.isfile(os.path.join(directory_path, f))]
        
        if not files:
            print("No files found in the directory.")
            return
        
        with open(output_file, 'w', encoding='utf-8') as outfile:
            for filename in files:
                filepath = os.path.join(directory_path, filename)
                
                # Write the filename header
                outfile.write(f"{filename} File:\n\n")
                
                # Write the file content
                try:
                    with open(filepath, 'r', encoding='utf-8') as infile:
                        outfile.write(infile.read())
                    
                    # Add spacing between files
                    outfile.write("\n\n")
                except UnicodeDecodeError:
                    # Skip binary files
                    outfile.write(f"[Binary file - content not displayed]\n\n")
                except Exception as e:
                    outfile.write(f"[Error reading file: {str(e)}]\n\n")
        
        print(f"Successfully merged {len(files)} files into {output_file}")
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    # Get directory path from user input
    directory = input("Enter the directory path to merge files from: ")
    
    # Call the merge function
    merge_files(directory)