def decorator_func(say_hello_func):
  def wrapper_func(hello_var, world_var):
    hello = "Hello, "
    world = "World"
    
    if not hello_var:
      hello_var = hello
    
    if not world_var:
      world_var = world
      
    return say_hello_func(hello_var, world_var)
  
  return wrapper_func

@decorator_func
def say_hello(hello_var, world_var):
  print(hello_var + " " + world_var)

say_hello("", "")  
say_hello("Hi", "")
say_hello("", "There")

###

def my_decorator(some_function):

    def wrapper():
        print("\nSomething is happening before {}() is called.".
          format(some_function.__name__))
        some_function()
        print("Something is happening after {}() is called.\n".
          format(some_function.__name__))

    return wrapper

###

def just_some_function():
    print("Wheee!")

just_some_function = my_decorator(just_some_function)

just_some_function()

###

@my_decorator
def just_another_function():
  print("Whoosh!")

just_another_function()

###

def a_decorator(func):

  def wrapper(*args):
    print("\nI am doing some boring work before executing {}()".format(func.__name__))

    l = len(args)
    if l == 0:
      func()
    elif l == 1:
      func(args[0])
    else:
      func(*args)
          
    print("I am doing some boring work after executing {}()\n".format(func.__name__))

  return wrapper

@a_decorator
def hi(name):
  print("Hi, " + name)

@a_decorator
def hello():
  print("Hello")

@a_decorator
def greetings(fname, lname):
  print("Greetings {} {}".format(fname, lname))

hi("truman")
hello()
greetings("Truman", "Smith")
