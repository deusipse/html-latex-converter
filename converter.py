# converts HTML to LaTeX with advanced support for configuration
# last modified 12/2/2024
from bs4 import BeautifulSoup, NavigableString
import re

def html_to_latex(html):
    soup = BeautifulSoup(html, 'html.parser')
    latex_code = convert_to_latex(soup)
    return latex_code

def convert_to_latex(element):
    latex_code = ""

    if isinstance(element, NavigableString):
        latex_code += str(element)
    elif element.name == 'div':
        latex_code += ''.join(convert_to_latex(child) for child in element.contents)
    elif element.name == 'tr':
        # \nextline
        latex_code += ''.join(convert_to_latex(child) for child in element.contents) + ' \\nextline'
    elif element.name == 'td':
        latex_code += ''.join(convert_to_latex(child) for child in element.contents)
    elif element.name == 'span':
        style = element.get('style', '')
        # check colours, handle bold cases differently
        color_command = get_latex_format_command(style)
        color_command_bold = get_latex_format_command_bold(style)
        color_command_italics = get_latex_format_command_italics(style)

        # check if any child within the span is a strong element
        contains_strong = any(child.name == 'strong' for child in element.contents)
        # check for italics
        contains_italics = any(child.name == 'em' for child in element.contents)

        if contains_strong:
            latex_code += color_command_bold + ''.join(convert_to_latex(child) for child in element.contents) + '}'
        elif contains_italics:
            latex_code += color_command_italics + ''.join(convert_to_latex(child) for child in element.contents) + '}'
        else:
            latex_code += color_command + ''.join(convert_to_latex(child) for child in element.contents) + '}'
    else:
        latex_code += ''.join(convert_to_latex(child) for child in element.contents)
    return latex_code

def get_latex_format_command(style): # handles colours
    color_mapping = {
        'color:rgb(0, 0, 255);': '\\ts{',
        'color:rgb(255, 0, 0);text-decoration:underline;': '\\textcolor{red}{\\underline{',
    }
    for color_style, latex_command in color_mapping.items():
        if color_style in style:
            return latex_command
    return ''

def get_latex_format_command_bold(style): # bold colours
    color_mapping = {
        'color:rgb(56, 118, 29);': '\\fb{',
        'color:rgb(17, 138, 15);': '\\fb{',
        'color:rgb(0, 0, 255);': '\\tsbold{',
        'color:rgb(255, 0, 0);text-decoration:underline;': '\\ssunderline{',
        'color:rgb(255, 0, 0);': '\\ss{',
    }
    for color_style, latex_command in color_mapping.items():
        if color_style in style:
            return latex_command
    return ''
def get_latex_format_command_italics(style): # bold colours
    color_mapping = {
        'color:rgb(0, 0, 255);': '\\tsitalics{',
    }
    for color_style, latex_command in color_mapping.items():
        if color_style in style:
            return latex_command
    return ''

with open('test.html', 'r') as file:
    html_content = file.read()

latex_output = html_to_latex(html_content)

# regex change stuff
patterns_to_replace = {
    r'\(Check\)': r'\\check',
    r'\(Signal\)': r'\\signal',
    r'\(Pause\)': r'\\pause',
    r'Watch.': r'\\watching',
    r'Watching.': r'\\watching',
    r'\(Repeat until confident\)': r'\\repeatuntilconfident',
    r'\(Model\)': r'\\model',
    r'\(Tap for each number\)': r'\\tap',
    r'Listen.': r'\\listening',
    r'Watch and Listen.': r'\\watchandlisten',
    r'Pencils up.': r'\\pencilsup',
    r'\d+\.': r'\\nextstep',
    r'\\nextline\n\n\|': r'\\nextrepline',
    r'\\nextstep \|': r'\\nextrepstep',
    r'\s+(?=(\n|$))': r'',
    r' {2,}': r'',
    r'\\nextline\n\\nextstep': r'\\nextstep',
    r'\\nextline}': r'\\nextline',
    r'\\nextline\n': r'\n\\nextline\n',
    r'\\nextrepline}': r'\\nextrepline'
}

for pattern, replacement in patterns_to_replace.items():
    latex_output = re.sub(pattern, replacement, latex_output)

with open('output.txt', 'w') as file:
    file. write(latex_output)

print("Conversion complete. LaTeX output saved to 'output.txt'.")
