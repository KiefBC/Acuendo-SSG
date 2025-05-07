import os
import sys

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

# Import the necessary functions
from src.main import process_markdown_files

def test_paths():
    root_dir = os.path.abspath(os.path.join(os.getcwd()))
    dest_dir = os.path.join(root_dir, "public")
    content_dir = os.path.join(root_dir, "content")
    template_path = os.path.join(root_dir, "template.html")
    
    # Define a mock generate_page function that just prints the paths
    def mock_generate_page(from_path, template_path, dest_path):
        print(f"Would generate: {from_path} -> {dest_path}")
    
    # Define a recursive function to simulate process_markdown_files
    def simulate_process_markdown_files(content_dir, template_path, dest_dir):
        for item in os.listdir(content_dir):
            content_path = os.path.join(content_dir, item)
            
            if os.path.isdir(content_path):
                # Create corresponding directory in public (just print, don't actually create)
                relative_path = os.path.relpath(content_path, content_dir)
                dest_subdir = os.path.join(dest_dir, relative_path)
                print(f"Would create directory: {dest_subdir}")
                
                # Process markdown files in subdirectory
                simulate_process_markdown_files(content_path, template_path, dest_dir)
            elif item.endswith(".md"):
                # Process markdown file
                file_name = os.path.splitext(item)[0]
                
                # Calculate the relative directory path
                relative_dir = os.path.relpath(os.path.dirname(content_path), content_dir)
                
                if file_name == "index":
                    # For index.md, output to the directory's index.html
                    if relative_dir == ".":
                        # Root index.md
                        dest_path = os.path.join(dest_dir, "index.html")
                    else:
                        # Subdirectory index.md
                        dest_path = os.path.join(dest_dir, relative_dir, "index.html")
                else:
                    # For other markdown files, create a corresponding HTML file
                    if relative_dir == ".":
                        # Files in the root content directory
                        dest_path = os.path.join(dest_dir, f"{file_name}.html")
                    else:
                        # Files in subdirectories
                        dest_path = os.path.join(dest_dir, relative_dir, f"{file_name}.html")
                
                # Print the paths
                mock_generate_page(content_path, template_path, dest_path)
    
    # Simulate processing markdown files
    print("Simulating processing markdown files...")
    simulate_process_markdown_files(content_dir, template_path, dest_dir)

if __name__ == "__main__":
    test_paths()