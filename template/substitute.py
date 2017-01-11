# Reads game info from a txt file, and substitutes proper html into
# a template HTML file.

import sys
import os

inputFile = os.path.join(sys.path[0], 'games.txt')
templateFile = os.path.join(sys.path[0], 'template.html')
outputFile = os.path.join(sys.path[0], '../index.html')
sectionMarker = '%%%'
htmlTemplate = '''
          <div class="game">
            <a href="{link}" target="_blank">
              <img src="{image}"/>
              <h3>{name}</h3>
              <h4>{tagline}</h4>
            </a>
          </div>'''

# Read input file to construct sections data structure
with open(inputFile) as f:
    sections = [[]]
    sectionIndex = 0
    newgame = []
    i = 0

    for line in f:
        line = line[:-1] # strip newline
        
        # %%% line moves to new section
        if line[0:3] == sectionMarker:
            sectionIndex += 1
            sections.append([])
        # blank line moves to new game
        elif line == '':
            sections[sectionIndex].append(newgame)
            newgame = []
        # any other line adds to current game
        else:
            newgame.append(line)

# Replace all game data arrays with html strings
for i, section in enumerate(sections):
    for i, game in enumerate(section):
        section[i] = htmlTemplate.format(
                name=game[0], tagline=game[1],
                image=game[2], link=game[3])

# Subsitute game html strings into target html
with open(templateFile) as f:
    data = f.read()

for section in sections[1:]:
    data = str.replace(data, sectionMarker, ''.join(section), 1)

with open(outputFile, 'w') as f:
    f.write(data)

