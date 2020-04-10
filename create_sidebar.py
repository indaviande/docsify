"""
This script generates a sidebar structure for Docsify (https://docsify.js.org/)
projects. It's intended as a way to make the sidebar a little more
straight-forward but the result will probably need some re-arranging.
Usage:
- Download this file to your project's directory
- "cd" into that directory
- Run "python3 generate_sidebar.py"
The script will:
- Generate a sidebar with links to all files, recursively
- Generate an index file (prefix _i_) for each sub-folder, also accessible via
  sidebar
Credits: Based on indaviande's script
(https://github.com/docsifyjs/docsify/issues/610)
"""

import os

# Erase sidebar's content
open('_sidebar.md', 'w').close()


def scan_dir(dir_path='.', level=0):
    """
    Look inside each directory in the project to see if there's anything good to
    add to the sidebar
    """
    def make_display_name_from_path(path):
        parts = path.split('/')
        name = parts[-1]
        name = name.split(".md")[0]  # Remove .md extension
        name = name.replace('-', ' ')  # Add space instead of -
        name = name.replace('_i_', '')  # Always remove _i_ index flag
        name = name.lower().capitalize()  # Capitalize first word
        return name

    def create_dir_index_file(dir_path):
        # Create index file name
        dir_name = dir_path.split('/')[-1]
        dir_index_file_path = dir_path.replace(
            dir_name, '_i_' + dir_name) + '.md'

        if (os.path.isfile(dir_index_file_path)):
            # Clear existing file
            open(dir_index_file_path, 'w').close()

        # Compose the index file
        index_file = open(dir_index_file_path, 'w')

        # Write a title
        dir_display_name = make_display_name_from_path(dir_path)
        index_file.write(f"# {dir_display_name}\n")

        # Write a link for each entry in this directory
        entries = [entry for entry in os.listdir(dir_path)]
        for entry_file_name in entries:
            # Ignore entries starting with _ (so also _i_ for indexes) or .
            if (any(i in entry_file_name[0] for i in ['_', '.'])):
                continue

            entry_path = dir_path + '/' + entry_file_name
            entry_display_name = make_display_name_from_path(entry_path)

            if os.path.isdir(entry_path):
                entry_path = dir_path + '/_i_' + entry_file_name

            index_file.write(
                f"- [{entry_display_name}]({entry_path})\n")

        index_file.close()

    def write_entry_in_sidebar(entry_path, index=False):
        """
        Write the sidebar entry, on the right level
        """
        # Add prefix for index files
        if index:
            entry_file_name = entry_path.split('/')[-1]
            entry_path = entry_path.replace(
                entry_file_name, '_i_' + entry_file_name) + '.md'

        # Write entry in the sidebar file
        sidebar_file = open('_sidebar.md', 'a')
        entry_display_name = make_display_name_from_path(entry_path)
        sidebar_file.write(
            f"{'  ' * level}* [{entry_display_name}]({entry_path})\n")
        sidebar_file.close()

    def execute():
        entries = [entry for entry in os.listdir(dir_path)]
        sublevel = level + 1

        if level > 0:
            # Create folder index (skip root directory)
            create_dir_index_file(dir_path)

        for entry_file_name in entries:
            # Ignore entries starting with _ (so also _i_ for indexes) or .
            if (any(i in entry_file_name[0] for i in ['_', '.'])):
                continue

            # Compose full path for this entry
            entry_path = dir_path + '/' + entry_file_name

            if os.path.isfile(entry_path):
                # Ignore files that are not markdown files
                if '.md' not in entry_file_name:
                    continue

                # Found suitable sidebar item, write it down
                write_entry_in_sidebar(entry_path)

            if os.path.isdir(entry_path):
                # Create a higher lever entry for this directory
                write_entry_in_sidebar(entry_path, index=True)

                # Scan this directory to add the entries it contains
                scan_dir(entry_path, sublevel)

    execute()


# Start process
scan_dir()

print('✅ All done, cheers!')