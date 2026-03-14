from enum import Enum

class QuizStates(str, Enum):
    QUIZ_START = "quiz_start"
    ANSWERING = "answering"