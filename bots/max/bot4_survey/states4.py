from enum import Enum

class SurveyStates(str, Enum):
    SURVEY_START = "survey_start"
    ANSWERING = "answering"