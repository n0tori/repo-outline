"""
 Full codebase:
    python repoOutline.py /path/to/directory/ /path/to/output.txt

 Partial codebase:
    python repoOutline.py /path/to/directory/ /path/to/output.txt    
    --ignore folder folder/subfolder file.txt anotherfile.md
"""

import os
import argparse

def generate_file_structure(directory_path, ignore_paths):
    file_structure = []
    for root, dirs, files in os.walk(directory_path):
        # Remove ignored directories and files from the traversal
        dirs[:] = [d for d in dirs if os.path.join(root, d) not in ignore_paths]
        files[:] = [f for f in files if os.path.join(root, f) not in ignore_paths]

        level = root.replace(directory_path, '').count(os.sep)
        indent = ' ' * 4 * level
        file_structure.append(f"{indent}{os.path.basename(root)}/")
        sub_indent = ' ' * 4 * (level + 1)
        for file in files:
            file_structure.append(f"{sub_indent}{file}")
    return "\n".join(file_structure)

def generate_text_file(directory_path, output_file, ignore_paths):
    ignore_paths = [os.path.abspath(os.path.join(directory_path, p)) for p in ignore_paths]
    excluded_extensions = {'.gif', '.png', '.jpg', '.jpeg', '.webp', '.heif', '.ico', '.flac', '.wav', '.mp3', '.mp4', '.avi', '.mov', '.mkv'}

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("File Structure:\n")
        f.write(generate_file_structure(directory_path, ignore_paths))
        f.write("\n\n")

        for root, dirs, files in os.walk(directory_path):
            # Remove ignored directories and files from traversal
            dirs[:] = [d for d in dirs if os.path.join(root, d) not in ignore_paths]
            files[:] = [f for f in files if os.path.join(root, f) not in ignore_paths]

            for file in files:
                file_path = os.path.join(root, file)
                file_extension = os.path.splitext(file)[1].lower()

                if file_extension in excluded_extensions:
                    continue

                f.write(f"### {file}\n\n")

                try:
                    with open(file_path, 'r', encoding='utf-8') as file_content:
                        f.write(file_content.read())
                except Exception as e:
                    f.write(f"Could not read file: {e}\n")
                f.write("\n\n")

def main():
    parser = argparse.ArgumentParser(description="Generate a text file with the directory structure and file contents.")
    parser.add_argument("directory", help="Path to the directory to process.")
    parser.add_argument("output", help="Path to the output text file.")
    parser.add_argument("--ignore", nargs="*", default=[], help="List of files and folders within the directory to ignore.")
    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"Error: {args.directory} is not a valid directory.")
        return

    generate_text_file(args.directory, args.output, args.ignore)
    print(f"Output written to {args.output}")

if __name__ == "__main__":
    main()
