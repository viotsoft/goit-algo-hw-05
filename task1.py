class HasTable:
    def __init__(self, size):
        self.size = size
        # Ініціалізуємо список списків (кожен елемент table - це "відро" (bucket))
        self.table = [[] for _ in range(size)]

    def hash_function(self, key):
        # Повертає індекс bucket'у
        return hash(key) % self.size
    
    def insert(self, key, value):
        key_hash = self.hash_function(key)
        key_value = [key, value]

        # Якщо у bucket ще немає жодної пари, просто додаємо
        if len(self.table[key_hash]) == 0:
            self.table[key_hash].append(key_value)
            return True
        else:
            # Якщо ключ уже існує, оновлюємо його значення
            for pair in self.table[key_hash]:
                if pair[0] == key:
                    pair[1] = value
                    return True
            # Якщо ключа немає, додаємо нову пару
            self.table[key_hash].append(key_value)
            return True
        
    def get(self, key):
        key_hash = self.hash_function(key)
        # Шукаємо пару з ключем у bucket'і
        if len(self.table[key_hash]) != 0:
            for pair in self.table[key_hash]:
                if pair[0] == key:
                    return pair[1]
        return None
    
    def delete(self, key):
        key_hash = self.hash_function(key)
        # Якщо відро порожнє, видаляти нічого
        if len(self.table[key_hash]) == 0:
            return False
        
        # Шукаємо ключ і видаляємо відповідну пару
        for index, pair in enumerate(self.table[key_hash]):
            if pair[0] == key:
                self.table[key_hash].pop(index)
                return True
            
# Приклад використання
if __name__ == "__main__":
    ht = HasTable(5)
    ht.insert("apple", 10)
    ht.insert("banana", 20)
    ht.insert("orange", 30)  

    print(ht.get("apple"))  
    print(ht.get("banana")) 
    print(ht.get("orange")) 

    # Видалення ключа
    is_deleted = ht.delete("apple")  
    print(is_deleted)

# Перевіряємо, чи дійсно видалилося
print(ht.get("apple"))  
