import unittest
try:
    # FIXME: it should not be here
    # it is here because we need pyhistorian tests passing
    # and pyhistorian_plone needs to work too :)
    from Products.PloneTestCase.PloneTestCase import PloneTestCase as TestCase
except ImportError:
    from unittest import TestCase

__all__= ['PyhistorianSuite', ]


class _StepTestCase(TestCase):
    """
    Specialization of TestCase to handle Steps
    """
    def __init__(self, func, func_name, msg, step_name):
        self._func = func
        self._func_name = func_name
        self._msg = msg
        self._step_name = step_name
        TestCase.__init__(self, '_func')

    def setUp(self):
        """
        setUp should do NOTHING
        because if it does anything, every step - given/when/then - sharing vars would break
        """

    def tearDown(self):
        """
        tearDown should do NOTHING
        because if it does anything, every step - given/when/then - sharing vars would break
        """

    def shortDescription(self):
        return str(self)

    def __str__(self):
        step_msg = "\n    %s %s" % (self._step_name.title(), self._msg)
        return step_msg
#        class_name = self._func.im_class.__module__
#        return "    %s # %s" % (step_msg.ljust(30), class_name)

    def __repr__(self):
        return "<%s testMethod=%s>" % \
               (unittest._strclass(self.__class__), self._func_name)



class _FakeTestCase(unittest.TestCase):
    """
    Fake TestCase for Stories and Scenarios
    It does not count as a test and has a custom message
    """
    def __init__(self, msg):
        self._msg = msg
        TestCase.__init__(self, 'fake_test')

    def fake_test(self):
        pass

    def run(self, result):
        """
        patch the test runner to not include the fake in the output
        """
        result.showAll = False
        result.testsRun -= 1
        result.startTest(self)
        if hasattr(result, 'stream'):
            result.stream.write(self._msg)
        result.stopTest(self)
        result.showAll = True
        
    def __str__(self):
        return self._msg

    def countTestCases(self):
        return 0


class _ScenarioTestSuite(unittest.TestSuite):
    def __init__(self, scenario):
        self._scenario = scenario
        self._tests = [_FakeTestCase('  Scenario 1: %s' % scenario._title)]
        self._set_step_methods()

    def _set_step_methods(self):
        for step_name in ['given', 'when', 'then']:
            self._set_step_method(step_name)

    def _set_step_method(self, step_name):
        step = getattr(self._scenario, '_%ss' % step_name)
        for method, message, args in step:
            func = getattr(self._scenario, method.func_name)
            step_testcase = _StepTestCase(func, method.func_name, message, step_name)
            self._tests.append(step_testcase)


class _StoryTestSuite(unittest.TestSuite):
    def __init__(self, story):
        header_lines = [line.strip() for line in story.__doc__.split('\n')]
        story_header = 'Story: %s\n  %s\n' % (story._title, '\n  '.join(header_lines))
        self._tests = [_FakeTestCase(story_header)]
        self._tests += [_ScenarioTestSuite(scenario) for scenario in story._scenarios]


class PyhistorianSuite(unittest.TestSuite):
    def __init__(self, *stories):
        self._tests = [_StoryTestSuite(story) for story in stories]
