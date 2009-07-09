'''
>>> story.run()
>>> print output.getvalue()
Story: Faked Story
As a fake
I want to run a simple story
So that it runs sucessfully and give me a good output
<BLANKLINE>
Scenario 1: Fake Title
  Given I run it   ... OK
  When I type X   ... OK
  Then it shows me X   ... OK
<BLANKLINE>
'''

from pyhistorian import Story
from cStringIO import StringIO
output = StringIO()

class FakeScenario(object):
    _givens = _whens = _thens = []
    title = 'Fake Title'

    def set_story(self, story):
        """default interface (should do nothing)"""

    def run(self):
        output.write('  Given I run it   ... OK\n')
        output.write('  When I type X   ... OK\n')
        output.write('  Then it shows me X   ... OK\n')
fake_scenario = FakeScenario()

story = Story(title='Faked Story',
              as_a='fake',
              i_want_to='run a simple story',
              so_that='it runs sucessfully and give me a good output',
              output=output)
story.add_scenario(fake_scenario)

