# 定义一个装饰器函数
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("执行装饰器")
        return func(*args, **kwargs)
    return wrapper

# 使用type()函数动态创建一个类，并将装饰器函数作为类的属性
MyClass = type("MyClass", (object,), {"my_method": my_decorator(lambda self: "Hello, World!")})

# 创建类的实例并调用方法
obj = MyClass()
print(obj.my_method())
