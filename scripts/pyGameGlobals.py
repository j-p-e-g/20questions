from enum import IntEnum

PROGRAM_ICON_PATH = "images/questionExclamationMark.png"
TICK_ICON_PATH = "images/tickMark.png"

MAX_NUM_QUESTIONS = 10
MAX_NUM_GUESSES = 3

class KnowledgeValues(IntEnum):
    UNKNOWN = 0
    YES = 1
    NO = 2
    MAYBE = 3

