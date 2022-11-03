# 객체들의 집합
# ==
world = [[], [], []]



def add_object(o, depth):
    world[depth].append(o)

def add_objects(ol, depth):
    world[depth] += ol

def all_object():
    for layer in world:
        for o in layer:
            yield o # generater로 취급

def clear():
    for o in all_object():
        del o
    for layer in world:
        layer.clear()

def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            del o
            return
    raise ValueError('Trying destroy non existing object')
