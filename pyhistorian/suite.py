import doctest
import unittest
import sys
from cStringIO import StringIO
from story import *
from scenario import *
from steps import *
from should_dsl import *


__all__= ['PyhistorianSuite', ]


class _Failure(object):
    '''
        >>> fail = _Failure(Exception('foo'))
        >>> fail.shortDescription()
        'foo'
        >>> fail2 = _Failure(Exception())
        >>> fail2.shortDescription()
        ''
    '''
    failureException = AssertionError

    def __init__(self, exception):
        self._exception = exception

    def shortDescription(self):
        if len(self._exception.args):
            return self._exception.args[0]
        return ''


class WrapTestCase(unittest.TestCase):
    """
    Specialization of unittest.TestCase to handle Stories + Steps
    """
    def __init__(self, func, func_name, msg, step_name):
        self._func = func
        self._func_name = func_name
        self._msg = msg
        self._step_name = step_name

    def shortDescription(self):
        doc = self._msg
        return doc and doc.split("\n")[0].strip() or None

    def id(self):
        return "%s.%s" % (unittest._strclass(self.__class__), self._func_name)

    def __str__(self):
        class_name = self._func.im_class.__module__
        step_msg = "%s %s" % (self._step_name.title(), self._msg)
        return "    %s # %s" % (step_msg.ljust(30), class_name)

    def __repr__(self):
        return "<%s testMethod=%s>" % \
               (unittest._strclass(self.__class__), self._func_name)

    def run(self, result=None):
        if result is None:
            result = self.defaultTestResult()
        result.startTest(self)
        testMethod = self._func
        try:
            try:
                self.setUp()
            except KeyboardInterrupt:
                raise
            except:
                result.addError(self, self.__exc_info())
                return

            ok = False
            try:
                testMethod()
                ok = True
            except self.failureException:
                result.addFailure(self, self.__exc_info())
            except KeyboardInterrupt:
                raise
            except:
                result.addError(self, self.__exc_info())

            try:
                self.tearDown()
            except KeyboardInterrupt:
                raise
            except:
                result.addError(self, self.__exc_info())
                ok = False
            if ok:
                result.addSuccess(self)
        finally:
            result.stopTest(self)

    def __exc_info(self):
        """Return a version of sys.exc_info() with the traceback frame
           minimised; usually the top level of the traceback frame is not
           needed.
        """
        exctype, excvalue, tb = sys.exc_info()
        return (exctype, excvalue, tb)


    def debug(self):
        """Run the test without collecting errors in a TestResult"""
        self.setUp()
        self._func()
        self.tearDown()


class FakeTestCase(unittest.TestCase):
    def __init__(self, msg):
        self._msg = msg
        # __str__ is the test method. LOL
        unittest.TestCase.__init__(self, '__str__')

    def __str__(self):
        return self._msg

    def countTestCases(self):
        return 0


class _ScenarioTestSuite(unittest.TestSuite):
    def __init__(self, scenario):
        self._scenario = scenario
        self._testcases = [FakeTestCase('  Scenario: %s' % scenario._title)]
        self._set_step_methods()

    def __iter__(self):
        return iter(self._testcases)

    def _set_step_methods(self):
        for step_name in ['given', 'when', 'then']:
            self._set_step_method(step_name)

    def _set_step_method(self, step_name):
        step = getattr(self._scenario, '_%ss' % step_name)
        for method, message, args in step:
            func = getattr(self._scenario, method.func_name)
            wrapped_testcase = WrapTestCase(func, method.func_name, message, step_name)
            self._testcases.append(wrapped_testcase)


class _StoryTestSuite(unittest.TestSuite):
    def __init__(self, story):
        header_lines = [line.strip() for line in story.__doc__.split('\n')]
        self._testcases = [FakeTestCase('Story: %s%s' % (story._title, '\n  '.join(header_lines)))]
        self._testcases += [_ScenarioTestSuite(scenario) for scenario in story._scenarios]

    def __iter__(self):
        return iter(self._testcases)
    

class PyhistorianSuite(unittest.TestSuite):
    def __init__(self, *stories):
        self._stories = [_StoryTestSuite(story) for story in stories]

    def __iter__(self):
        return iter(self._stories)


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)
