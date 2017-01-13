# Generates index.html by reading a .txt of games and substituting in
# some html corresponding to each game.

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
sections = []
sectionIndex = -1

def htmlFromGame(game):
    return htmlTemplate.format(
            name=game[0], tagline=game[1],
            image=game[2], link=game[3])

# Read input file line by line
with open(inputFile) as f:
    for line in f:

        line = line[:-1] # strip newline
        
        if line == sectionMarker:
            # %%% line moves to new section
            sections.append([])
            sectionIndex += 1
            game = []
        elif line == '':
            # blank line stores the game and starts a new one
            # (if the game is not empty)
            if len(game) > 0:
                sections[sectionIndex].append(htmlFromGame(game))
                game = []
        else:
            # any other non-comment line adds to current game
            if line[0] != '#':
                game.append(line)

# Get template data as one string
with open(templateFile) as f:
    data = f.read()

# Substitute all sections into the template data
for section in sections:
    data = str.replace(data, sectionMarker, ''.join(section), 1)

# Write substituted data out
with open(outputFile, 'w') as f:
    f.write(data)

