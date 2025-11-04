import pyperclip


def main():
    prefix = input("Please enter default file name: ")
    default_title = prefix.replace('_', ' ').capitalize()
    title = input(f"Please enter Title: {default_title} ") or default_title
    png_file = input(f"Please enter png file name: default: {prefix}.png " ) or f"{prefix}.png"
    python_file = input(f"Please enter python file name: default: {prefix}.py " ) or f"{prefix}.py"
    html_file = input(f"Please enter html file name: default: {prefix}.html ") or f"{prefix}.html"
    
    with open('template.html', 'r') as template:
        content = template.read()
    
    content = content.replace('$PNG_FILE', png_file)
    content = content.replace('$PYTHON_FILE', python_file)
    content = content.replace('$TITLE', title)
    
    with open(html_file, 'w') as output_file:
        output_file.write(content)
    
    with open('li_template.html', 'r') as template:
        content = template.read()
    content = content.replace('$PNG_FILE', png_file)
    content = content.replace('$HTML_FILE', html_file)
    content = content.replace('$TITLE', title)
    print(content)
    
    pyperclip.copy(content)
if __name__ == "__main__":
    main()