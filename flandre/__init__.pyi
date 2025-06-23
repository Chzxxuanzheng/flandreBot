from matcher.sender import Finish as Finish
from matcher.commandMatcher import commandMatcher as commandMatcher
from matcher.messageMatcher import messageMatcher as messageMatcher
from matcher.connectMatcher import connectMatcher as connectMatcher
from matcher.timerMatcher import cronMatcher as cronMatcher, intervalMatcher as intervalMatcher
from matcher.errorMatcher import matcherErrorMatcher as matcherErrorMatcher
from matcher.regexMatcher import regexMatcher as regexMatcher
from matcher.matchers import target as target
from .config import baseConfig as baseConfig

def init(**kwargs):...

def run(*args, **kwargs):...