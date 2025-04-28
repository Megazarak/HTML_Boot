import os
import shutil

from markdown_blocks import generate_pages_recursive

def main():
    
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)

    # Delete "public" directory if it exists, then recreate it
    public_dir = os.path.join(project_root, "public")
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)
    os.makedirs(public_dir)

    # Copy static files from "static" to "public"
    source_dir = os.path.join(project_root, "static")
    dest_dir = public_dir
    copy_static_files(source_dir, dest_dir)

    # Process all markdown files in the content directory
    content_dir = os.path.join(project_root, "content")
    template_path = os.path.join(project_root, "template.html")
    
    # Process all markdown files
    process_markdown_files(content_dir, public_dir, template_path)

def copy_static_files(source_dir, dest_dir):
    # First, check if destination exists and remove it
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    
    # Then create the destination directory fresh
    os.mkdir(dest_dir)
    
    _copy_recursive(source_dir, dest_dir)

def _copy_recursive(source_dir, dest_dir):
    # This is where the recursive copying logic goes
    # Loop through all items in the source directory
    for item in os.listdir(source_dir):
        source_path = os.path.join(source_dir, item)
        dest_path = os.path.join(dest_dir, item)
        
        if os.path.isfile(source_path):
            # If it's a file, copy it
            shutil.copy(source_path, dest_path)
            print(f"Copied file: {source_path} to {dest_path}")
        else:
            # If it's a directory, create it and recurse
            if not os.path.exists(dest_path):
                os.mkdir(dest_path)
            _copy_recursive(source_path, dest_path)

def process_markdown_files(content_dir, public_dir, template_path):
    for root, dirs, files in os.walk(content_dir):
        # Calculate the relative path from content_dir to the current directory
        rel_path = os.path.relpath(root, content_dir)
        
        # Create the corresponding directory in public_dir
        if rel_path != '.':  # Skip the root directory itself
            dest_dir = os.path.join(public_dir, rel_path)
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
        
        # Process each markdown file
        for file in files:
            if file.endswith('.md'):
                md_path = os.path.join(root, file)
                
                # Determine the destination path
                if file == 'index.md':
                    # For index.md files, generate index.html in the same directory structure
                    if rel_path == '.':
                        html_path = os.path.join(public_dir, 'index.html')
                    else:
                        html_path = os.path.join(public_dir, rel_path, 'index.html')
                else:
                    # For non-index.md files, use the file name without .md extension
                    html_name = file[:-3] + '.html'
                    if rel_path == '.':
                        html_path = os.path.join(public_dir, html_name)
                    else:
                        html_path = os.path.join(public_dir, rel_path, html_name)
                
                # Ensure the directory exists
                os.makedirs(os.path.dirname(html_path), exist_ok=True)
                
                # Generate the HTML page
                generate_pages_recursive(md_path, template_path, html_path)
                print(f"Generated: {html_path} from {md_path}")

if __name__ == "__main__":
    main()