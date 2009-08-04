import doctest
# tests follow
import bug_regex
import colors
import scenario
import step
import story
import unittest_integration
import stringio_feature
import story_pt_br
import pending
import finding_scenarios_in_module
import almost_plain_text_history

FLAGS=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS
def run_tests():
    for test in [bug_regex,
                 colors,
                 scenario,
                 step,
                 story,
                 unittest_integration,
                 stringio_feature,
                 story_pt_br,
                 pending,
                 finding_scenarios_in_module,
                 almost_plain_text_history,]:
        doctest.testmod(test, optionflags=FLAGS)

if __name__ == '__main__':
    run_tests()
