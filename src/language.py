# coding: utf-8

TEMPLATE_PATTERN = r'\$[a-zA-Z]\w*'

def convert_from_cammel_case_to_spaces(text):
    """
        >>> convert_from_cammel_case_to_spaces('HelloWorld')
        'Hello world'
        >>> convert_from_cammel_case_to_spaces('helloMotto')
        'hello motto'
    """
    spaced_text = text[0]
    for char in text[1:]:
        if char == char.capitalize():
            spaced_text += ' ' + char.lower()
        else:
            spaced_text += char
    return spaced_text
 

_english = dict(story='Story',
                as_a='As a',
                i_want_to='I want to',
                so_that='So that',
                scenario='Scenario',
                given='Given',
                when='When',
                then='Then',
                fail='Fail',
                failure='Failure',
                error='Error',
                and_word='And',
                empty_story_title='Empty Story',
                empty_scenario_title='Empty Sceario',
                exception_thrown='Exception %s was thrown!',
                undefined_step='Undefined Step',
                ran='Ran',
                with_word='with',
                pending='pending',
                step='step',
                )

_portuguese = dict(story='História',
                as_a='Como um',
                i_want_to='Eu quero',
                so_that='Para que',
                scenario='Cenário',
                given='Dado que',
                when='Quando',
                then='Então',
                fail='Falha',
                failure='Falha',
                error='Erro', 
                and_word='E',
                empty_story_title='História Vazia',
                empty_scenario_title='Cenário Vazio',
                exception_thrown='A Exceção %s foi levantada!',
                undefined_step='Passo não definido',
                ran='Rodou',
                with_word='com',
                pending='pendente',
                step='passo',
                )

_LANGUAGES = {'en-us': _english,
              'pt-br' : _portuguese}

class StoryLanguageError(Exception):
    '''raised when the user wants a non-existent language or
    some non-existent term
    '''


class StoryLanguage(object):
    '''
        >>> en_us = StoryLanguage('en-us')
        >>> print en_us['story']
        Story
        >>> pt_br = StoryLanguage('pt-br')
        >>> print pt_br['story']
        História
    '''
    def __init__(self, language):
        if language not in _LANGUAGES:
            raise StoryLanguageError('There is no language %s' % language)
        self._language = _LANGUAGES[language]

    def __getitem__(self, term):
        if term not in self._language:
            raise StoryLanguageError('There is no term %s' % term)
        return self._language[term]

if __name__ == '__main__':
    import doctest
    doctest.testmod()
