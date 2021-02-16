

class Rule:
    def __init__(self, expression: str, tag: str = "", id: str = ""):
        self.__expression = expression
        self.__tag = tag
        self.__id = id

    def __str__(self) -> str:
        return f'Rule [id {self.__id}, expression {self.__expression}, tag {self.__tag}]'

    def __repr__(self) -> str:
        return f'Rule [id {self.__id}, expression {self.__expression}, tag {self.__tag}]'

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, new_id):
        self.__id = new_id

    @property
    def tag(self):
        return self.__tag

    @tag.setter
    def tag(self, new_tag):
        self.__tag = new_tag

    @property
    def expression(self):
        return self.__expression

    @expression.setter
    def expression(self, new_expression):
        self.__expression = new_expression