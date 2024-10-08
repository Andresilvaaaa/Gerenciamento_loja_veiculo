import json as j


class Locales:

    def __init__(self, file=None):
        self.file_name = file
        self.lang = None
        self.messages = None
        self.languages = None

        if self.file_name:
            self.open_doc(file)

    @staticmethod
    def example(file_name=None):
        if not file_name:
            file_name = "example.json"

        with open(file_name, 'w', encoding='utf-8') as f:
            data = {
                "languages": {
                    "ru": "Русский", "eng": "English", "sp": "Español"
                },

                "messages": {
                    "welcome": {
                        "ru": "Добро пожаловать!",
                        "eng": "Welcome!"
                    },
                    "goodbye": {
                        "ru": "Пока",
                        "eng": "Goodbye",
                        "sp": "Adiós"
                    }
                }

            }

            j.dump(data, f, indent=2, ensure_ascii=False)

    def open_doc(self, file):
        with open(file, 'r', encoding='utf-8') as f:
            d = j.load(f)

        if "languages" not in d:
            raise KeyError("You need to initialize languages in json body")

        self.languages = d["languages"]
        self.lang = list(self.languages.keys())[0]

        if "messages" not in d:
            raise KeyError("You need to initialize messages in json body")

        self.messages = d["messages"]

        m_l = set()
        [[m_l.add(l) for l in [*x.keys()]] for x in [*d["messages"].values()]]

        for key in m_l:
            if key not in d["languages"]:
                raise ValueError('Key "{}" should be in "languages"'.format(key))

    def get(self, message, language=None):
        if message not in self.messages:
            raise KeyError('"{}" not found in "messages"'.format(message))

        if language:
            if language not in self.languages:
                raise KeyError('"{}" not found in "languages"'.format(language))
            return self.messages[message][language]
        else:
            return self.messages[message][self.lang]

    def get_all(self, message):
        if message not in self.messages:
            raise KeyError('"{}" not found in "messages"'.format(message))

        return self.messages[message]

    def get_by_name(self, name):
        n = [*self.languages.keys()]
        d_n = [*self.languages.values()]

        if name not in d_n:
            raise ValueError('"{}" not found as Value in "languages"'.format(name))

        i = d_n.index(name)

        return n[i]

    def set_default_lang(self, language):
        if language not in self.languages:
            raise KeyError('"{}" not found in "languages"'.format(language))

        self.lang = language
