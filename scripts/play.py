import os
import re
from typing import List
import nltk
nltk.download('punkt_tab')
from nltk.tokenize import sent_tokenize

class Sentence:
    def __init__(self, text: str):
        self.text = text

    def __repr__(self):
        return f'Sentence("{self.text}")'


class Scene:
    def __init__(self, scene_number: int, lines: List[str]):
        self.scene_number = scene_number
        self.text = " ".join(lines)
        self.sentences = [Sentence(sent) for sent in sent_tokenize(self.text)]

    def __repr__(self):
        return f'Scene {self.scene_number}: {self.text}'


class Act:
    def __init__(self, act_number: int, scenes: List[Scene]):
        self.act_number = act_number
        self.scenes = scenes

    def __repr__(self):
        return f'Act {self.act_number}: {self.scenes}'


class Play:
    def __init__(self, title: str, acts: List[Act]):
        self.title = title
        self.acts = acts

    def __repr__(self):
        return f'Play "{self.title}": {self.acts}'
    
def create_play(filepath):

    play = None

    with open(filepath, 'r') as file:
        title = ""
        
        content_begun = False

        open_scene = False
        
        acts = []
        scenes = []
        lines = []

        for line in file:
            line = line.strip()
            
            # for every Scene, gather its lines

            if title == "":
                title = line
                continue

            match line:
                case "=====": # new Act
                    if not content_begun:
                        content_begun = True
                    else:
                        # I have gathered all lines for the scene, and all scenes for the current act.
                        scenes.append(Scene(len(scenes) + 1, lines[:-1])) # don't include the last line: it is an act number annotation
                        lines = []
                        acts.append(Act(len(acts) + 1, scenes))
                        scenes = []
                        open_scene = False
                case "=======": # new Scene
                    if not open_scene:
                        open_scene = True
                    else:
                        # I have gathered all lines for the current Scene.
                        scenes.append(Scene(len(scenes) + 1, lines[:-1])) # don't include the last line: it is a scene number annotation
                        lines = []
                case _:
                    # treat this as a content line.
                    if content_begun and open_scene:
                        lines.append(line)

        # last scene, act:
        # I have gathered all lines for the scene, then all scenes for the current act.
        scenes.append(Scene(len(scenes) + 1, lines)) # include all lines: no structural annotation
        lines = []
        acts.append(Act(len(acts) + 1, scenes))
        scenes = []

        play = Play(title, acts)

    return play