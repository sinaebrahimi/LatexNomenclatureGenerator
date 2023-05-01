import re
from pathlib import Path
from typing import List, Dict

def read_file(file: Path) -> str:
    with open(file, 'r', encoding='utf-8') as f:
        return f.read()

def find_section_files(main_tex_file: Path) -> List[Path]:
    main_text = read_file(main_tex_file)
    section_files = re.findall(r'\\input\{(.+?)\}', main_text)
    return [main_tex_file.parent / section_file for section_file in section_files]

def read_sections_text(section_files: List[Path]) -> str:
    sections_text = ''
    for section_file in section_files:
        sections_text += read_file(section_file)
    return sections_text

def find_acronyms(sections_text: str) -> List[str]:
    return re.findall(r'\(([A-Z]+)\)', sections_text)

def find_full_descriptions(acronyms: List[str], sections_text: str) -> Dict[str, str]:
    full_descriptions = {}
    for acronym in acronyms:
        words = [f'([A-Z][a-z]*)' for _ in acronym]
        pattern = rf'{" ".join(words)} \({acronym}\)'
        match = re.search(pattern, sections_text)
        if match:
            full_descriptions[acronym] = ' '.join(match.groups())
    return full_descriptions

def generate_latex_table(full_descriptions: Dict[str, str]) -> str:
    table = '\\begin{table}\n\\begin{tabular}{l|l}\n'
    table += 'Acronym & Full Description\\\\ \\hline\n'
    for acronym, desc in sorted(full_descriptions.items()):
        table += f'{acronym} & {desc}\\\\\n'
    table += '\\hline\n\\end{tabular}\n\\end{table}'
    return table

def generate_acronyms_table(main_tex_file: str) -> str:
    main_tex_file = Path(main_tex_file)
    section_files = find_section_files(main_tex_file)
    sections_text = read_sections_text(section_files)
    acronyms = find_acronyms(sections_text)
    full_descriptions = find_full_descriptions(acronyms, sections_text)
    return generate_latex_table(full_descriptions)


if __name__ == '__main__':
    main_tex_file = r"C:\TV\tek\main.tex"
    table = generate_acronyms_table(main_tex_file)
    print(table)
