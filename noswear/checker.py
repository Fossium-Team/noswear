# Copyright (c) 2021 FOSS-Devs
# See LICENSE in the project root for license information.
import os
import difflib

class Noswear():
    path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'data\\wordlist.txt'))

    def __init__(self):
        pass

    def check(self, string, similarity: float = 0.76, path = path):
        with open(f"{path}", "r") as words:
            badwords = words.read().splitlines()
        spec_char = {"@": "a", "1": "i", "!": "i", "0": "o", "1": "l", "3": "e", "$": "s", "5": "s", "4": "a"}
        string = string.lower()
        for attr, value in spec_char.items():
            string = string.replace(attr, value)
        if ' ' in string:
            string = ' '.join(string.split())
            for word in string.split(' '):
                word = ''.join(filter(str.isalpha, word))
                for badword in badwords:
                    if self._checker(word, badword, similarity):
                        return True
        else:
            for badword in badwords:
                if self._checker(string, badword, similarity):
                    return True
        return False

    def _diffcheck(self, word, badword, similarity: float):
        score = difflib.SequenceMatcher(None, word, badword, autojunk=False).ratio()
        if score >= similarity:
            #print(f"Word: '{word}' Badword: '{badword}' Score: '{score}'")
            return True
        return False

    def _checker(self, string, badword, similarity: float):
        if badword == string:
            #print(f"Word: '{badword}' Badword: '{badword}' 'location 1'")
            return True 
        elif len(string) == len(badword) and self._diffcheck(string, badword, similarity):
            #print("'location 2'")
            return True
        elif len(string) >= 6 and len(badword) > 3:
            if badword in string or string in badword:
                #print(f"Word: '{string}' Badword: '{badword}' 'location 3'")
                return True
        return False