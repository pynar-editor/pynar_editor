import os
import re
import random
import sqlite3
from Components.ChatBotView.replace_emoji import replaceToEmoji, getEmojiText
pairs = []
reflections = {}
generalAnswer = "Ne dediğinizi anlayamadım."


class ChatbotEngine:
    def __init__(self, pUserMessage):
        self.user_message = pUserMessage

    def robotBalloonMessage(self):
        chat = Chat(pairs)
        if self.user_message != "" and self.user_message is not None:
            robot_message = chat.respond(self.user_message)
            if robot_message is None:
                emoji_res = getEmojiText(self.user_message)
                if emoji_res is not None:
                    robot_message = chat.respond(emoji_res)
                    if robot_message is not None:
                        robot_message = replaceToEmoji(robot_message)
                        return robot_message
                    else:
                        return generalAnswer
                else:
                    return generalAnswer
            else:
                return robot_message
        else:
            emoji_res = getEmojiText(self.user_message)
            if emoji_res is not None:
                robot_message = chat.respond(emoji_res)
                if robot_message is not None:
                    robot_message = replaceToEmoji(robot_message)
                    return robot_message
                else:
                    return generalAnswer
            else:
                return generalAnswer

    def robotButtonOptions(self):
        return None



class Chat(object):
    def __init__(self, pairs):
        self.keys = list(map(lambda x: re.compile(x[0], re.IGNORECASE), pairs))
        self.values = list(map(lambda x: x[1], pairs))

    def translate(self, str, dict):
        words = str.lower().split()
        keys = dict.keys();
        for i in range(0, len(words)):
            if words[i] in keys:
                words[i] = dict[words[i]]
        return ' '.join(words)

    def respond(self, str):
        for i in range(0, len(self.keys)):
            match = self.keys[i].match(str)
            if match:
                resp = random.choice(self.values[i])
                pos = resp.find('%')
                while pos > -1:
                    num = int(resp[pos + 1:pos + 2])
                    resp = resp[:pos] + \
                           self.translate(match.group(num), reflections) + \
                           resp[pos + 2:]
                    pos = resp.find('%')
                if resp[-2:] == '?.': resp = resp[:-2] + '.'
                if resp[-2:] == '??': resp = resp[:-2] + '?'
                return resp


def Search(sentence):
    index = 0
    for i in pairs:
        if sentence in i[0]:
            return index
        index += 1
    return False


def LoadChatbotPairs_Reflection():
    try:
        parentdir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
        conn = sqlite3.connect(parentdir + '/Config/' + 'chatbot-database.db')
        c = conn.cursor()
        LoadPairs(c)
        LoadReflections(c)
    except Exception as err:
        print("Error: {0}".format(err))


def LoadPairs(c):
    for row in c.execute('SELECT Q.Question, A.Answer FROM Questions Q INNER JOIN Answers A ON A.QuestionId = Q.Id'):
        if not Search(row[0]):
            pairs.append([row[0], [row[1]]])
        else:
            pairs[Search(row[0])][1].append(row[1])


def LoadReflections(c):
    for row in c.execute('SELECT  ReflectionKey, ReflectionValue FROM Reflections'):
        reflections[row[0]] = row[1]
