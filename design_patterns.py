# Part 1
# http://www.youtube.com/watch?v=1Sbzmz1Nxvo&feature=channel

# Wrapping to restrict
class RestrictWrapper(object):
    def __init__(self, wrapee, block):
        self._wrapee = wrapee
        self._block = block
    def __getattr__(self, attr_name):
        if n in self._block:
            raise AttributeError, attr_name
        return getattr(self._wrapee, attr_name)

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
# known-usage example from the python standard library
def __call__(cls, *a, **k):
    nu = cls.__new__(cls, *a, **k)
    if isinstance(nu, cls):
        cls.__init__(nu, *a, **k)
    return nu

# ===================
# Structural Patterns
# ===================

# - Adapter
# =========
# C requires method foobar(foo, bar)
# S supplies method barfoo(bar, foo)
class Barfooer(object):
    def barfoo(self, bar, foo):
        pass

# -- 1. Adapter per-instance with object delegation (cleaner soln)
class FoobarWrapper(object):
    def __init__(self, wrapee):
        self.wrapee = wrapee
    def foobar(self, foo, bar):
        return self.wrapee.barfoo(bar, foo)
barfooer = Barfooer()
foobarer = FoobarWrapper(barfooer)

# -- 2. Adapter per-class with subclassing and self-delegation (faster soln)
class Foobarer(Barfooer):
    def foobar(self, foo, bar):
        return self.barfoo(bar, foo)
foobarer = Foobarer()
# In real-world uses, mixin classes are a great way of help adapt to rich protocols

# - Facade
# ========
# Supplier code sigma provides rich, complex functionality in protocol S
# We need simple subset C of S
# Facade code phi implements and supplies C (by means of appropriate calls to S on sigma)
#
# Facade vs Adapter:
# Adapter is about supplying a given protocol required by client-code.
# Facade is about simplifying a rich interface when just subset is often needed.
# Facade most often "fronts" for many objects, Adapter for just one.
# Inheritance is never useful for Facade because it can only "widen" and not "restrict".

# - Bridge
# ========
# Have N1 realizations rho of abstraction A
# each using any one of N2 implementations i of functionality F
# without coding N1 x N2 boilerplate classes
# Have abstract superclass A of all rho hold a reference R to the interface F of all i
# Ensure each rho uses any functionality of F (thus, from some i) only by delegating to R
class AbstractParser(object):
    def __init__(self, scanner):
        self.scanner = scanner
    def __getattr__(self, name):
        return getattr(self.scanner, name)
class ExpressionParser(AbstractParser):
    def expr(self):
        # ...
        token = self.next_token() # no need to worry about which scanner
        self.push_back(token)
        # ...
# Another more sophisticated example:
class AbstractInterface:
    # Target interface.
    # This is the target interface, that clients use.
    def someFunctionality(self):
        raise NotImplemented()
class Bridge(AbstractInterface):
    # Bridge class.
    # This class forms a bridge between the target
    # interface and background implementation.
    def __init__(self):
        self.__implementation = None
class Linux:
    def some_functionality(self):
        print "Linux!"
class Windows:
    def some_functionality(self):
        print "Windows!"

