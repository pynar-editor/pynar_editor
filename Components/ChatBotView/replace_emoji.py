import emoji
import ast
translation_emoticons = {
    'o/': ['👋', 'waving_hand'],
    '</3': ['💔', 'broken_heart'],
    '<3': ['💗', 'growing_heart'],
    '8-D': ['😁', 'beaming_face_with_smiling_eyes'],
    '8D': ['😁', 'beaming_face_with_smiling_eyes'],
    ':-D': ['😁', 'beaming_face_with_smiling_eyes'],
    '=-3': ['😁', 'beaming_face_with_smiling_eyes'],
    '=-D': ['😁', 'beaming_face_with_smiling_eyes'],
    '=3': ['😁', 'beaming_face_with_smiling_eyes'],
    '=D': ['😁', 'beaming_face_with_smiling_eyes'],
    'B^D': ['😁', 'beaming_face_with_smiling_eyes'],
    'X-D': ['😁', 'beaming_face_with_smiling_eyes'],
    'XD': ['😁', 'beaming_face_with_smiling_eyes'],
    'x-D': ['😁', 'beaming_face_with_smiling_eyes'],
    'xD': ['😁', 'beaming_face_with_smiling_eyes'],
    ':\')': ['😂', 'face_with_tears_of_joy'],
    ':\'-)': ['😂', 'face_with_tears_of_joy'],
    ':-))': ['😃', 'grinning_face_with_big_eyes'],
    '8)': ['😄', 'grinning_face_with_smiling_eyes'],
    ':)': ['😄', 'grinning_face_with_smiling_eyes'],
    ':-)': ['😄', 'grinning_face_with_smiling_eyes'],
    ':3': ['😄', 'grinning_face_with_smiling_eyes'],
    ':D': ['😄', 'grinning_face_with_smiling_eyes'],
    ':],': ['😄', 'grinning_face_with_smiling_eyes'],
    ':^)': ['😄', 'grinning_face_with_smiling_eyes'],
    ':c)': ['😄', 'grinning_face_with_smiling_eyes'],
    ':o)': ['😄', 'grinning_face_with_smiling_eyes'],
    ':}': ['😄', 'grinning_face_with_smiling_eyes'],
    ':っ)': ['😄', 'grinning_face_with_smiling_eyes'],
    '=)': ['😄', 'grinning_face_with_smiling_eyes'],
    '=]': ['😄', 'grinning_face_with_smiling_eyes'],
    '0:)': ['😇', 'smiling_face_with_halo'],
    '0:-)': ['😇', 'smiling_face_with_halo'],
    '0:-3': ['😇', 'smiling_face_with_halo'],
    '0:3': ['😇', 'smiling_face_with_halo'],
    '0;^)': ['😇', 'smiling_face_with_halo'],
    'O:-)': ['😇', 'smiling_face_with_halo'],
    '3:)': ['😈', 'smiling_face_with_horns'],
    '3:-)': ['😈', 'smiling_face_with_horns'],
    '}:)': ['😈', 'smiling_face_with_horns'],
    '}:-)': ['😈', 'smiling_face_with_horns'],
    '*)': ['😉', 'winking_face'],
    '*-)': ['😉', 'winking_face'],
    ':-,': ['😉', 'winking_face'],
    ';)': ['😉', 'winking_face'],
    ';-)': ['😉', 'winking_face'],
    ';-],': ['😉', 'winking_face'],
    ';D': ['😉', 'winking_face'],
    ';],': ['😉', 'winking_face'],
    ';^)': ['😉', 'winking_face'],
    ':-|': ['😐', 'neutral_face'],
    ':|': ['😐', 'neutral_face'],
    ':(': ['😒', 'unamused_face'],
    ':-(': ['😒', 'unamused_face'],
    ':-<': ['😒', 'unamused_face'],
    ':-[': ['😒', 'unamused_face'],
    ':-c': ['😒', 'unamused_face'],
    ':<': ['😒', 'unamused_face'],
    ':[': ['😒', 'unamused_face'],
    ':c': ['😒', 'unamused_face'],
    ':{': ['😒', 'unamused_face'],
    ':っC': ['😒', 'unamused_face'],
    '%)': ['😖', 'confounded_face'],
    '%-)': ['😖', 'confounded_face'],
    ':-P': ['😜', 'winking_face_with_tongue'],
    ':-b': ['😜', 'winking_face_with_tongue'],
    ':-p': ['😜', 'winking_face_with_tongue'],
    ':-Þ': ['😜', 'winking_face_with_tongue'],
    ':-þ': ['😜', 'winking_face_with_tongue'],
    ':P': ['😜', 'winking_face_with_tongue'],
    ':b': ['😜', 'winking_face_with_tongue'],
    ':p': ['😜', 'winking_face_with_tongue'],
    ':Þ': ['😜', 'winking_face_with_tongue'],
    ':þ': ['😜', 'winking_face_with_tongue'],
    ';(': ['😜', 'winking_face_with_tongue'],
    '=p': ['😜', 'winking_face_with_tongue'],
    'X-P': ['😜', 'winking_face_with_tongue'],
    'XP': ['😜', 'winking_face_with_tongue'],
    'd:': ['😜', 'winking_face_with_tongue'],
    'x-p': ['😜', 'winking_face_with_tongue'],
    'xp': ['😜', 'winking_face_with_tongue'],
    ':-||': ['😠', 'angry_face'],
    ':@': ['😠', 'angry_face'],
    ':-.': ['😡', 'pouting_face'],
    ':-/': ['😡', 'pouting_face'],
    ':/': ['😡', 'pouting_face'],
    ':L': ['😡', 'pouting_face'],
    ':S': ['😡', 'pouting_face'],
    ':\\': ['😡', 'pouting_face'],
    '=/': ['😡', 'pouting_face'],
    '=L': ['😡', 'pouting_face'],
    '=\\': ['😡', 'pouting_face'],
    ':\'(': ['😢', 'crying_face'],
    ':\'-(': ['😢', 'crying_face'],
    '^5': ['😤', 'face_with_steam_from_nose'],
    '^<_<': ['😤', 'face_with_steam_from_nose'],
    'o/\\o': ['😤', 'face_with_steam_from_nose'],
    '|-O': ['😫', 'tired_face'],
    '|;-)': ['😫', 'tired_face'],
    ':###..': ['😰', 'anxious_face_with_sweat'],
    ':-###..': ['😰', 'anxious_face_with_sweat'],
    'D-\':': ['😱', 'face_screaming_in_fear'],
    'D8': ['😱', 'face_screaming_in_fear'],
    'D:': ['😱', 'face_screaming_in_fear'],
    'D:<': ['😱', 'face_screaming_in_fear'],
    'D;': ['😱', 'face_screaming_in_fear'],
    'D=': ['😱', 'face_screaming_in_fear'],
    'DX': ['😱', 'face_screaming_in_fear'],
    'v.v': ['😱', 'face_screaming_in_fear'],
    '8-0': ['😲', 'astonished_face'],
    ':-O': ['😲', 'astonished_face'],
    ':-o': ['😲', 'astonished_face'],
    ':O': ['😲', 'astonished_face'],
    ':o': ['😲', 'astonished_face'],
    'O-O': ['😲', 'astonished_face'],
    'O_O': ['😲', 'astonished_face'],
    'O_o': ['😲', 'astonished_face'],
    'o-o': ['😲', 'astonished_face'],
    'o_O': ['😲', 'astonished_face'],
    'o_o': ['😲', 'astonished_face'],
    ':$': ['😳', 'flushed_face'],
    '#-)': ['😵', 'knocked-out_face'],
    ':#': ['😶', 'face_without_mouth'],
    ':&': ['😶', 'face_without_mouth'],
    ':-#': ['😶', 'face_without_mouth'],
    ':-&': ['😶', 'face_without_mouth'],
    ':-X': ['😶', 'face_without_mouth'],
    ':X': ['😶', 'face_without_mouth'],
    ':-J': ['😼', 'cat_with_wry_smile'],
    ':*': ['😽', 'kissing_cat'],
    ':^*': ['😽', 'kissing_cat'],
    'ಠ_ಠ': ['🙅', 'person_gesturing_NO'],
    '*\\0/*': ['🙆', 'person_gesturing_OK'],
    '\\o/': ['🙆', 'person_gesturing_OK'],
    ':>': ['😄', 'grinning_face_with_smiling_eyes'],
    '>.<': ['😡', 'pouting_face'],
    '>:(': ['😠', 'angry_face'],
    '>:)': ['😈', 'smiling_face_with_horns'],
    '>:-)': ['😈', 'smiling_face_with_horns'],
    '>:/': ['😡', 'pouting_face'],
    '>:O': ['😲', 'astonished_face'],
    '>:P': ['😜', 'winking_face_with_tongue'],
    '>:[': ['😒', 'unamused_face'],
    '>:\\': ['😡', 'pouting_face'],
    '>;)': ['😈', 'smiling_face_with_horns'],
    '>_>^': ['😤', 'face_with_steam_from_nose']
    }

#Butona tıklaranak gelen emojilerin karşılığı
onlyIcon = {
    '🤡': 'clown_face',
    '😀': 'grinning_face',
    '😁': 'beaming_face_with_smiling_eyes',
    '😂': 'face_with_tears_of_joy',
    '🤣': 'rolling_on_the_floor_laughing',
    '😃': 'grinning_face_with_big_eyes',
    '😄': 'grinning_face_with_smiling_eyes',
    '😅': 'grinning_face_with_sweat',
    '😆': 'grinning_squinting_face',
    '😉': 'winking_face',
    '😊': 'smiling_face_with_smiling_eyes',
    '😋': 'face_savoring_food',
    '😎': 'smiling_face_with_sunglasses',
    '😍': 'smiling_face_with_heart-eyes',
    '😘': 'face_blowing_a_kiss',
    '😗': 'kissing_face',
    '😙': 'kissing_face_with_smiling_eyes',
    '😚': 'kissing_face_with_closed_eyes',
    '🙂': 'slightly_smiling_face',
    '🤗': 'hugging_face',
    '🤩': 'star-struck',
    '🤔': 'thinking_face',
    '🤨': 'face_with_raised_eyebrow',
    '😐': 'neutral_face',
    '😑': 'expressionless_face',
    '😶': 'face_without_mouth',
    '🙄': 'face_with_rolling_eyes',
    '😏': 'smirking_face',
    '😣': 'persevering_face',
    '😥': 'sad_but_relieved_face',
    '😮': 'face_with_open_mouth',
    '🤐': 'zipper-mouth_face',
    '😯': 'hushed_face',
    '😪': 'sleepy_face',
    '😫': 'tired_face',
    '😴': 'sleeping_face',
    '😌': 'relieved_face',
    '😛': 'face_with_tongue',
    '😜': 'winking_face_with_tongue',
    '😝': 'squinting_face_with_tongue',
    '🤤': 'drooling_face',
    '😒': 'unamused_face',
    '😓': 'downcast_face_with_sweat',
    '😔': 'pensive_face',
    '😕': 'confused_face',
    '🙃': 'upside-down_face',
    '🤑': 'money-mouth_face',
    '😲': 'astonished_face',
    '🙁': 'slightly_frowning_face',
    '😖': 'confounded_face',
    '😞': 'disappointed_face',
    '😟': 'worried_face',
    '😤': 'face_with_steam_from_nose',
    '😢': 'crying_face',
    '😭': 'loudly_crying_face',
    '😦': 'frowning_face_with_open_mouth',
    '😧': 'anguished_face',
    '😨': 'fearful_face',
    '😩': 'weary_face',
    '🤯': 'exploding_head',
    '😬': 'grimacing_face',
    '😰': 'anxious_face_with_sweat',
    '😱': 'face_screaming_in_fear',
    '😳': 'flushed_face',
    '🤪': 'zany_face',
    '😵': 'knocked-out_face',
    '😡': 'pouting_face',
    '😠': 'angry_face',
    '🤬': 'face_with_symbols_on_mouth',
    '😷': 'face_with_medical_mask',
    '🤒': 'face_with_thermometer',
    '🤕': 'face_with_head-bandage',
    '🤢': 'nauseated_face',
    '🤮': 'face_vomiting',
    '🤧': 'sneezing_face',
    '😇': 'smiling_face_with_halo',
    '🤠': 'cowboy_hat_face',
    '🤥': 'lying_face',
    '🤫': 'shushing_face',
    '🤭': 'face_with_hand_over_mouth',
    '🧐': 'face_with_monocle',
    '🤓': 'nerd_face'
}


#UNICODE_EMOJI ile ilgili işlemler yeni versiyonlarda olmadığından statik olarak eklendi.
from emoji.unicode_codes.data_dict import *
def get_emoji_unicode_dict(lang):
    """ Get the EMOJI_UNICODE_{language} dict containing all fully-qualified and component emoji"""
    return {data[lang]: emj for emj, data in EMOJI_DATA.items() if lang in data and data['status'] <= STATUS['fully_qualified']}


def get_unicode_emoji_dict(lang):
    """ Get the UNICODE_EMOJI_{language} dict containing all emoji that have a name in {lang}"""
    return {emj: data[lang] for emj, data in EMOJI_DATA.items() if lang in data}

EMOJI_UNICODE_ENGLISH = get_emoji_unicode_dict('en')
UNICODE_EMOJI_ENGLISH = get_unicode_emoji_dict('en')

EMOJI_ALIAS_UNICODE_ENGLISH = dict(EMOJI_UNICODE_ENGLISH.items())
for emj, data in EMOJI_DATA.items():
    if 'alias' in data and data['status'] <= STATUS['fully_qualified']:
        for alias in data['alias']:
            EMOJI_ALIAS_UNICODE_ENGLISH[alias] = emj
UNICODE_EMOJI_ALIAS_ENGLISH = {v: k for k, v in EMOJI_ALIAS_UNICODE_ENGLISH.items()}

EMOJI_UNICODE_GERMAN = get_emoji_unicode_dict('de')
UNICODE_EMOJI_GERMAN = get_unicode_emoji_dict('de')

EMOJI_UNICODE_SPANISH = get_emoji_unicode_dict('es')
UNICODE_EMOJI_SPANISH = get_unicode_emoji_dict('es')

EMOJI_UNICODE_FRENCH = get_emoji_unicode_dict('fr')
UNICODE_EMOJI_FRENCH = get_unicode_emoji_dict('fr')

EMOJI_UNICODE_ITALIAN = get_emoji_unicode_dict('it')
UNICODE_EMOJI_ITALIAN = get_unicode_emoji_dict('it')

EMOJI_UNICODE_PORTUGUESE = get_emoji_unicode_dict('pt')
UNICODE_EMOJI_PORTUGUESE = get_unicode_emoji_dict('pt')


UNICODE_EMOJI = UNICODE_EMOJI = {
    'en': UNICODE_EMOJI_ENGLISH,
    'es': UNICODE_EMOJI_SPANISH,
    'pt': UNICODE_EMOJI_PORTUGUESE,
    'it': UNICODE_EMOJI_ITALIAN,
    'fr': UNICODE_EMOJI_FRENCH,
    'de': UNICODE_EMOJI_GERMAN,
}



translation_total = dict(UNICODE_EMOJI)
translation_total.update(translation_emoticons)

def replaceToEmoji(text):
    emoji_list = ((key, value) for (key, value) in translation_total.items())
    for (key, value) in emoji_list:
        if key is not None and key in text:
            if key == 'en' or key == 'es' or key == 'pt' or key == 'it' or key == 'de' or key == 'fr':
                pass
            else:
                text = text.replace(key, value[0])
    return text


def getEmojiText(textOrIcon):
    textOrIcon = textOrIcon.replace(' ', '')

    emojiText = next((value[1] for key, value in translation_emoticons.items() if key == textOrIcon), None)
    if emojiText is None:
        emojiText = next((value for key, value in onlyIcon.items() if key == textOrIcon), None)
    return emojiText


def areAllEmojis(text):
    text = text.replace(' ', '')
    emoji_list = ((key, value) for (key, value) in translation_total.items())
    for (key, value) in emoji_list:
        if key is not None and key in text:
            if key == 'en' or key == 'es' or key == 'pt' or key == 'it' or key == 'de' or key == 'fr':
                pass
            else:
                text = text.replace(key, '')

    if len(text) == 0:
        return True
    return False























































































































  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
