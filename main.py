import re
from pathlib import Path


def generate_acronyms_table(main_tex_file: str) -> str:
    main_tex_file = Path(main_tex_file)
    with open(main_tex_file, 'r') as f:
        main_text = f.read()

    # Find all section files included in the main file
    section_files = re.findall(r'\\input\{(.+?)\}', main_text)

    # Read the content of all section files
    sections_text = ''
    for section_file in section_files:
        section_file = main_tex_file.parent / section_file
        with open(section_file, 'r', encoding='utf-8') as f: #with open(section_file, 'r') as f:
            sections_text += f.read()

    # Find all acronyms in the text
    acronyms = re.findall(r'\(([A-Z]+)\)', sections_text)

    # Find the full description for each acronym
    full_descriptions = {}
    for acronym in acronyms:
        # Search for the full description before the acronym
        words = [f'([A-Z][a-z]*)' for _ in acronym]
        pattern = rf'{" ".join(words)} \({acronym}\)'
        match = re.search(pattern, sections_text)
        if match:
            full_descriptions[acronym] = ' '.join(match.groups())

    # Generate the LaTeX table
    table = '\\begin{table}\n\\begin{tabular}{l|l}\n'
    table += 'Acronym & Full Description\\\\ \\hline\n'
    for acronym, desc in sorted(full_descriptions.items()):
        table += f'{acronym} & {desc}\\\\\n'
    table += '\\hline\n\\end{tabular}\n\\end{table}'

    return table


if __name__ == '__main__':
    main_tex_file = r"C:\TV\tek\main.tex"
    table = generate_acronyms_table(main_tex_file)
    print(table)
