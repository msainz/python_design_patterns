# Part 1
# http://www.youtube.com/watch?v=1Sbzmz1Nxvo&feature=channel

# Wrapping to restrict
class RestrictWrapper(object):
    def __init__(self, wrapped, block):
        self._wrapped = wrapped
        self._block = block
    def __getattr__(self, attr_name):
        if n in self._block:
            raise AttributeError, attr_name
        return getattr(self._wrapped, attr_name)

# ===================
# Creational Patterns
# ===================

# - We want just 1 instance to exist
# ==================================

# -- 1. Just use a module
# problems: no subclassing, no special methods

# -- 2. Just make 1 instance (no enforcement)

# -- 3. Singleton ("Highlander")
class Singleton(object):
    def __new__(cls, *a, **k):
        if not hasattr(cls, '_instance'):
            cls._instance = super(Singleton, cls).__new__(cls, *a, **k)
        return cls._instance

# problem: doesn't conceptually work well with subclassing
class Foo(Singleton): pass
class Bar(Foo): pass
f = Foo(); b = Bar() # should this create 1 Singleton instance or 2??

# -- 4. Monostate ("Borg")
class Borg(object):
    _shared_state = {}
    def __new__(cls, *a, **k):
        obj = super(Borg, cls).__new__(cls, *a, **k)
        obj.__dict__ = cls._shared_state
        return obj

# subclassing is no problem
class Foo(Borg): pass
class Bar(Foo): pass
class Baz(Foo): _shared_state = {}

# - We don't want to commit to instantiating a specific concrete class
# ====================================================================
        
# -- 1. Dependency Injection a.k.a. Inversion of Control (IoC)
# no creation except from the outside
# problem: what if multiple creations are needed?

# -- 2. Factory
# may create whatever or reuse existing
# factory functions
def load(pkg, obj):
    m = __import__(pkg, {}, {}, [obj])
    return getattr(m, obj)
# example use
# cls = load('p1.p2.p3', 'c4')
# equivalent to
# from p1.p2.p3 import c4 as cls

# factory methods
# abstract factory classes
# in python each type/class is essentially a factory

# - Two-phase construction
# ========================
# very common in GUI realms
def __call__(cls, *a, **k):
    nu = cls.__new__(cls, *a, **k)
    if isinstance(nu, cls):
        cls.__init__(nu, *a, **k)
    return nu

# ===================
# Structural Patterns
# ===================


