"""Eliza engine.

Pattern-matching chatbot engine based on the original ELIZA / DOCTOR program
described by Joseph Weizenbaum in his 1966 paper "ELIZA -- A Computer Program
For the Study of Natural Language Communication Between Man And Machine".

This implementation is adapted from Wade Brainerd's MIT-licensed Python port
(https://github.com/wadetb/eliza). It uses exactly the same technique as the
original ELIZA: keyword ranking, decomposition rules and reassembly rules,
plus pre-/post-substitution and a simple "memory".

Changes vs. the original port:
  * `load_string()` so a script can be loaded from a string or a file.
  * Question marks and exclamation marks are normalised like other punctuation
    so keywords at the end of a question are still recognised.
  * The engine is fully reusable/stateless-friendly: create a fresh instance
    and replay the conversation to reproduce ELIZA's non-repeating behaviour
    (useful for serverless deployments).
"""

import logging
import random
import re

log = logging.getLogger(__name__)


class Key:
    def __init__(self, word, weight, decomps):
        self.word = word
        self.weight = weight
        self.decomps = decomps


class Decomp:
    def __init__(self, parts, save, reasmbs):
        self.parts = parts
        self.save = save
        self.reasmbs = reasmbs
        self.next_reasmb_index = 0


class Eliza:
    def __init__(self):
        self.initials = []
        self.finals = []
        self.quits = []
        self.pres = {}
        self.posts = {}
        self.synons = {}
        self.keys = {}
        self.memory = []

    # ------------------------------------------------------------------ load
    def load(self, path):
        with open(path, encoding="utf-8") as file:
            self.load_string(file.read())

    def load_string(self, text):
        key = None
        decomp = None
        for line in text.splitlines():
            if not line.strip():
                continue
            tag, content = [part.strip() for part in line.split(':', 1)]
            if tag == 'initial':
                self.initials.append(content)
            elif tag == 'final':
                self.finals.append(content)
            elif tag == 'quit':
                self.quits.append(content)
            elif tag == 'pre':
                parts = content.split(' ')
                self.pres[parts[0].lower()] = parts[1:]
            elif tag == 'post':
                parts = content.split(' ')
                self.posts[parts[0].lower()] = parts[1:]
            elif tag == 'synon':
                parts = content.split(' ')
                self.synons[parts[0]] = parts
            elif tag == 'key':
                parts = content.split(' ')
                word = parts[0].lower()
                weight = int(parts[1]) if len(parts) > 1 else 1
                key = Key(word, weight, [])
                self.keys[word] = key
            elif tag == 'decomp':
                parts = content.split(' ')
                save = False
                if parts[0] == '$':
                    save = True
                    parts = parts[1:]
                decomp = Decomp(parts, save, [])
                key.decomps.append(decomp)
            elif tag == 'reasmb':
                parts = content.split(' ')
                decomp.reasmbs.append(parts)

    # --------------------------------------------------------------- matching
    def _match_decomp_r(self, parts, words, results):
        if not parts and not words:
            return True
        if not parts or (not words and parts != ['*']):
            return False
        if parts[0] == '*':
            for index in range(len(words), -1, -1):
                results.append(words[:index])
                if self._match_decomp_r(parts[1:], words[index:], results):
                    return True
                results.pop()
            return False
        elif parts[0].startswith('@'):
            root = parts[0][1:]
            if root not in self.synons:
                raise ValueError("Unknown synonym root {}".format(root))
            if not words or words[0].lower() not in self.synons[root]:
                return False
            results.append([words[0]])
            return self._match_decomp_r(parts[1:], words[1:], results)
        elif parts[0].lower() != words[0].lower():
            return False
        else:
            return self._match_decomp_r(parts[1:], words[1:], results)

    def _match_decomp(self, parts, words):
        results = []
        if self._match_decomp_r(parts, words, results):
            return results
        return None

    def _next_reasmb(self, decomp):
        index = decomp.next_reasmb_index
        result = decomp.reasmbs[index % len(decomp.reasmbs)]
        decomp.next_reasmb_index = index + 1
        return result

    def _reassemble(self, reasmb, results):
        output = []
        for reword in reasmb:
            if not reword:
                continue
            # A reassembly token may reference a captured group, optionally with
            # trailing punctuation attached, e.g. "(2)", "(3)?", "(2)."
            match = re.match(r'^\((\d+)\)([.,;:!?]*)$', reword)
            if match:
                index = int(match.group(1))
                if index < 1 or index > len(results):
                    raise ValueError("Invalid result index {}".format(index))
                insert = results[index - 1]
                # ELIZA only reflects up to the first clause boundary.
                for punct in [',', '.', ';', ':', '?', '!']:
                    if punct in insert:
                        insert = insert[:insert.index(punct)]
                output.extend(insert)
                if match.group(2):
                    if output:
                        output[-1] = output[-1] + match.group(2)
                    else:
                        output.append(match.group(2))
            else:
                output.append(reword)
        return output

    def _sub(self, words, sub):
        output = []
        for word in words:
            word_lower = word.lower()
            if word_lower in sub:
                output.extend(sub[word_lower])
            else:
                output.append(word)
        return output

    def _match_key(self, words, key):
        for decomp in key.decomps:
            results = self._match_decomp(decomp.parts, words)
            if results is None:
                continue
            results = [self._sub(w, self.posts) for w in results]
            reasmb = self._next_reasmb(decomp)
            if reasmb[0] == 'goto':
                goto_key = reasmb[1]
                if goto_key not in self.keys:
                    raise ValueError("Invalid goto key {}".format(goto_key))
                return self._match_key(words, self.keys[goto_key])
            output = self._reassemble(reasmb, results)
            if decomp.save:
                self.memory.append(output)
                continue
            return output
        return None

    # ---------------------------------------------------------------- respond
    def respond(self, text):
        if text.lower().strip() in self.quits:
            return None

        text = re.sub(r'\s*\.+\s*', ' . ', text)
        text = re.sub(r'\s*,+\s*', ' , ', text)
        text = re.sub(r'\s*;+\s*', ' ; ', text)
        text = re.sub(r'\s*\?+\s*', ' ? ', text)
        text = re.sub(r'\s*!+\s*', ' ! ', text)

        words = [w for w in text.split(' ') if w]
        words = self._sub(words, self.pres)

        keys = [self.keys[w.lower()] for w in words if w.lower() in self.keys]
        keys = sorted(keys, key=lambda k: -k.weight)

        output = None
        for key in keys:
            output = self._match_key(words, key)
            if output:
                break
        if not output:
            if self.memory:
                index = random.randrange(len(self.memory))
                output = self.memory.pop(index)
            else:
                output = self._next_reasmb(self.keys['xnone'].decomps[0])

        return " ".join(output)

    def initial(self):
        return random.choice(self.initials)

    def final(self):
        return random.choice(self.finals)

    def run(self):
        print(self.initial())
        while True:
            try:
                sent = input('> ')
            except (EOFError, KeyboardInterrupt):
                break
            output = self.respond(sent)
            if output is None:
                break
            print(output)
        print(self.final())


def load_doctor(language='de'):
    """Return a fresh Eliza instance loaded with the requested DOCTOR script.

    Scripts are embedded as Python strings (see `eliza/scripts.py`) so the
    serverless deployment never depends on bundling external data files.
    """
    try:
        from .scripts import SCRIPTS
    except ImportError:  # allow running this file directly
        from scripts import SCRIPTS
    eliza = Eliza()
    eliza.load_string(SCRIPTS.get(language, SCRIPTS['de']))
    return eliza


if __name__ == '__main__':
    logging.basicConfig()
    load_doctor('de').run()
