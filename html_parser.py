import os
import re
import pandas as pd
from pathlib import Path
from datetime import datetime

def parse_html_metadata(file_path):
    """
    Extract metadata from HTML comment block in a single file
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Look for metadata comment block
        metadata_pattern = r'<!-- METADATA\s*\n(.*?)\n-->'
        match = re.search(metadata_pattern, content, re.DOTALL)
        
        if not match:
            # Fallback: try to get title from <title> tag if no metadata block
            title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
            title = title_match.group(1).strip() if title_match else "Untitled"
            
            return {
                'filename': file_path.name,
                'title': title,
                'author': 'Unknown',
                'date': datetime.fromtimestamp(file_path.stat().st_mtime).strftime('%Y-%m-%d'),
                'issue': 'n/a',
                'tags': '',
                'file_path': str(file_path)
            }
        
        # Parse the metadata block
        metadata_text = match.group(1)
        metadata = {}
        
        for line in metadata_text.strip().split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                metadata[key.strip().lower()] = value.strip()
        
        return {
            'filename': file_path.name,
            'title': metadata.get('title', 'Untitled'),
            'author': metadata.get('author', 'Unknown'),
            'date': metadata.get('date', datetime.fromtimestamp(file_path.stat().st_mtime).strftime('%Y-%m-%d')),
            'issue': metadata.get('issue', ''),
            'tags': metadata.get('tags', ''),
            'file_path': str(file_path)
        }
        
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        return None

def scan_pages_folder(pages_folder="m"):
    """
    Scan all HTML files in the pages folder and extract metadata
    """
    pages_path = Path(pages_folder)
    
    if not pages_path.exists():
        print(f"Error: {pages_folder} folder not found!")
        return pd.DataFrame()
    
    html_files = list(pages_path.glob("*.html"))
    
    if not html_files:
        print(f"No HTML files found in {pages_folder} folder")
        return pd.DataFrame()
    
    print(f"Found {len(html_files)} HTML files")
    
    # Parse metadata from all files
    metadata_list = []
    for file_path in html_files:
        metadata = parse_html_metadata(file_path)
        if metadata:
            metadata_list.append(metadata)
    
    # Create DataFrame
    df = pd.DataFrame(metadata_list)
    
    # Sort by date (newest first)
    if not df.empty:
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date', ascending=False)
        df['date'] = df['date'].dt.strftime('%Y-%m-%d')  # Convert back to string for display
    
    return df

def generate_html_table(df, output_file="content.html"):
    """
    Generate HTML table and insert it into content.html file
    """
    if df.empty:
        print("No data to generate table")
        return
    
    # Create HTML table
    table_html = '<table class="blog-summary">\n'
    table_html += '  <thead>\n'
    table_html += '    <tr>\n'
    table_html += '      <th>Title</th>\n'
    table_html += '      <th>Author</th>\n'
    table_html += '      <th>Date</th>\n'
    table_html += '      <th>Issue</th>\n'
    table_html += '      <th>Tags</th>\n'
    table_html += '    </tr>\n'
    table_html += '  </thead>\n'
    table_html += '  <tbody>\n'
    
    for _, row in df.iterrows():
        # Create relative link to the page
        link_path = f"m/{row['filename']}"
        table_html += '    <tr>\n'
        table_html += f'      <td><a href="{link_path}">{row["title"]}</a></td>\n'
        table_html += f'      <td>{row["author"]}</td>\n'
        table_html += f'      <td>{row["date"]}</td>\n'
        table_html += f'      <td>{row["issue"]}</td>\n'
        table_html += f'      <td>{row["tags"]}</td>\n'
        table_html += '    </tr>\n'
    
    table_html += '  </tbody>\n'
    table_html += '</table>\n'
    
    # Read existing content.html or create template
    content_file = Path(output_file)
    
    if content_file.exists():
        with open(content_file, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Look for existing table and replace it
        # This assumes you have a placeholder like <!-- TABLE_PLACEHOLDER -->
        if '<!-- TABLE_PLACEHOLDER -->' in content:
            content = re.sub(
                r'<!-- TABLE_PLACEHOLDER -->.*?<!-- /TABLE_PLACEHOLDER -->',
                f'<!-- TABLE_PLACEHOLDER -->\n{table_html}<!-- /TABLE_PLACEHOLDER -->',
                content,
                flags=re.DOTALL
            )
        else:
            # If no placeholder, append to body
            content = content.replace('</body>', f'{table_html}\n</body>')
    else:
        # Create basic HTML template
        content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Blog Summary</title>
    <style>
        .blog-summary {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        .blog-summary th, .blog-summary td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        .blog-summary th {{
            background-color: #f2f2f2;
            font-weight: bold;
        }}
        .blog-summary tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        .blog-summary a {{
            color: #0066cc;
            text-decoration: none;
        }}
        .blog-summary a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <h1>Blog Posts</h1>
    <!-- TABLE_PLACEHOLDER -->
{table_html}<!-- /TABLE_PLACEHOLDER -->
</body>
</html>"""
    
    # Write the updated content
    with open(content_file, 'w', encoding='utf-8') as file:
        file.write(content)
    
    print(f"Generated HTML table in {output_file}")

def main():
    """
    Main function to run the table builder
    """
    print("Building blog summary table...")
    
    # Scan pages folder
    df = scan_pages_folder("m")
    
    if df.empty:
        print("No pages found to process")
        return
    
    # Display DataFrame for verification
    print("\nFound pages:")
    print(df[['filename', 'title', 'author', 'date']].to_string(index=False))
    
    # Generate HTML table
    generate_html_table(df, "content.html")
    
    print("\nTable builder complete!")

if __name__ == "__main__":
    main()