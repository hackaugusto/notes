pynotes
-------

Dark things that I want to remember myself about python

Meta classes
------------

- Do not forget that a metaclass must subclass `type` not `object`
- `__metaclass__` can be either a function (with the same signature as `type`) or a `type` subclass

ABC and meta classes doesn't seem to go quite well together, for instance:

    class Meta(type):
        def __new__(metaclass, name, bases, attributes):
            print(metaclass)
            type.__new__(metaclass, name, bases, attributes)
        
    class MyList(UserList):
        # this will work fine and will print "MyList" into the screen
        __metaclass__ = Meta
      
    class SubList(MyList):
        # On the other hand, this will _not_ work
        pass
        
To solve this case is just a matter of making `Meta` a subclass of `UserList`

Decorators
----------

- Take care while decorating methods (because the wrapper function will be the method and not the decorated function) [Read about the descriptor protocol to know what is going on]

super
-----

It is a class

descriptors
-----------
