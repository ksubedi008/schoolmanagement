import glob
import os

files = glob.glob('templates/dashboard/partials/*_table.html') + glob.glob('templates/dashboard/modules/*.html')
for filepath in files:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        if '--card-bg' in content:
            content = content.replace('--card-bg', '--surface-color')
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'Fixed {filepath}')
    except Exception as e:
        print(f"Error {filepath}: {e}")
