# LatexAbbreviationFinder
A simple python script that scrapes a .tex file to find abbreviations and their descriptions. It will output a Latex table.

It starts with a 'main.tex' file that could contain sections defined as inputs (e.g., \input{Sections/some_section.tex}). The script looks for the abbreviations with big letters in parantheses and then, searches for the definition based on the number of letters of that abbreviation.
