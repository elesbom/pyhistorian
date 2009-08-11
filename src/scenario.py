from language import (StoryLanguage,
                      TEMPLATE_PATTERN,
                      convert_from_cammel_case_to_spaces,
                      format_traceback)
from termcolor import colored
import re
import sys
import traceback


class Scenario(object):
    _givens = []
    _whens = []
    _thens = []

    def __init__(self, story):
        self._title = self._get_title_from_class_name_or_docstring()
        self._story = story
        self._language = story._language
        self._output = story._output
        self._should_be_colored = story._colored
        self._failures = []
        self._errors = []
        self._pendings = []

    def _get_title_from_class_name_or_docstring(self):
        return self.__doc__ or\
               convert_from_cammel_case_to_spaces(self.__class__.__name__)

    def _colored(self, message, color):
        if self._should_be_colored:
            return colored(message, color)
        return message

    @property
    def title(self):
        return self._title

    def run(self):
        self.run_steps(self._givens, 'given')
        self.run_steps(self._whens, 'when')
        self.run_steps(self._thens, 'then')
        if self._failures:
            self._output_problem(self._failures, 'failure')
        if self._errors:
            self._output_problem(self._errors, 'error')
        return (self._failures, self._errors, self._pendings)
                
    def _output_problem(self, problems, problem_type):
        self._output.write(self._colored('\n%ss:\n' % 
                                self._language[problem_type], color='red'))
        for problem in problems:
            self._output.write(self._colored('%s\n' % problem,
                                                      color='red'))

    def _replace_template(self, message, args):
        for arg in args:
            message = re.sub(TEMPLATE_PATTERN, str(arg), message, 1)
        return message

    def _get_traceback_info(self):
        """this method is like traceback.format_exc,
        but it internationalizates the phrase and
        it doesn't need parameters"""
        exc, value, tb = sys.exc_info()
        return format_traceback(exc, value, tb, self._language)

    def _run_step(self, step, step_name):
        method, message, args = step
        message = self._replace_template(message, args)
        if hasattr(method, 'pending'):
            self._output.write(self._colored('  %s %s   ... %s\n' % (
                                             self._language[step_name],
                                             message,
                                             self._language['pending'].upper()),
                                             color='blue'))
            self._pendings.append(method)
            return
        try:
            method(self, *args)
            self._output.write(self._colored('  %s %s   ... OK\n' % (self._language[step_name],
                                                     message), color='green'))
        except AssertionError, e:
            self._failures.append(self._get_traceback_info())
            self._output.write(self._colored('  %s %s   ... %s\n' % (self._language[step_name],
                                             message,
                                             self._language['fail'].upper()),
                                             color='red'))
        except Exception, e:
            self._errors.append(self._get_traceback_info())
            self._output.write(self._colored('  %s %s   ... %s\n' % (self._language[step_name],
                                             message,
                                             self._language['error'].upper()),
                                             color='red'))

    def run_steps(self, steps, step_name):
        if steps == []:
            return
        self._run_step(steps[0], step_name)
        for step in steps[1:]:
            self._run_step(step, 'and_word')

class Cenario(Scenario):
    """Portuguese translation"""

