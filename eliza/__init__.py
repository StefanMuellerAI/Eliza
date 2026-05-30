"""ELIZA — pattern-matching chatbot in the style of Weizenbaum's DOCTOR (1966)."""

from .engine import Eliza, load_doctor

__all__ = ["Eliza", "load_doctor"]
