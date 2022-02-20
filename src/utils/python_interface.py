class Singleton:
    instances = {}

    def __new__(cls, classname, parents, attributes):
        created_type = type(classname, parents, attributes)
        if classname not in Singleton.instances:
            instance = created_type()
            Singleton.instances[classname] = instance

        def __new__(self):
            return Singleton.instances[classname]

        created_type.__new__ = __new__
        return created_type()
