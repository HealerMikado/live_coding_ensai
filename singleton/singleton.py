

class Singleton(object):
    __instance = None

    def __init__(self):
        if Singleton.__instance is not None :
            raise Exception("Il ne faut pas utiliser le constructeur")

    @staticmethod
    def get_instance() :
        if Singleton.__instance is None:
            Singleton.__instance = Singleton()
        return Singleton.__instance


class Test(type):
    def __call__(cls, *args, **kwargs):
        print("toto")


class PasSingleton(Test):
    pass

class SingletonMeta(type):
    __instances = {}
    def __call__(cls, *args, **kwargs):
        print("Appel à la méthode __call__")
        if cls not in cls.__instances:
            instance = super().__call__(*args, **kwargs)
            cls.__instances[cls] = instance
            print(cls.__instances)
        return cls.__instances[cls]


class Singleton1(metaclass=SingletonMeta):
    def some_business_logic(self):
        pass

if __name__ == '__main__':
    s1 = Singleton1()
