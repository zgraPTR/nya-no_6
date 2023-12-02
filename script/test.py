class TestClass:
    test_list = []

    def __init__(self) -> None:
        pass

    def add(self, a):
        self.test_list.append(a)
    
    @property
    def show(self):
        return self.test_list
    
a1 = TestClass()
a2 = TestClass()

a1.add("bbb")
a2.add("ccc")
print(a2.show)
