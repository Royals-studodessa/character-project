# конструктор предметов

class Item:

    def __init__(self, name, weight, value):
        
        self.name = name
        self.weight = weight
        self.value = value

    
    def  display(self):
        
        print(f"Персонаж подобрал предмет {self.name}, вес предмета {self.weight}, цена предмета {self.value}")
        
        
    def to_dict(self):

        return {
            "name": self.name,
            "weight": self.weight,
            "value": self.value,
        }


    def apply_discount(self, percent):
        
        old_value = self.value
        new_value = old_value * (percent / 100)
        
        print(f" цена со скидкой будет {old_value -new_value}")
        


# Тест:
if __name__ == "__main__":
    sword = Item("Меч", 5, 100)
    sword.display()
    sword.apply_discount(10)