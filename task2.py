def binary_search_upper_bound(arr, x):
    """
    Пошук верхньої межі (upper bound):
    Повертає (кількість_ітерацій, найменший_елемент_>=_x) або None, якщо такого немає.
    """

    left, right = 0, len(arr) - 1
    iteration_count = 0
    result = None # Найменший елемент >= x

    while left <= right:
        iteration_count +=1
        mid = (left + right) // 2

        # Якщо середній елемент >= x,
        # це потенційно шуканий елемент (upper bound),
        # але перевіримо, чи немає ще меншого зліва.

        if arr[mid] >= x:
            result = arr[mid]
            right = mid - 1
        else:
            # Якщо arr[mid] < x — шукаємо далі справа
            left = mid + 1

    return iteration_count, result

# Приклад використання:
if __name__ == "__main__":
   # Відсортований масив із дробових чисел
    data = [0.1, 1.5, 2.0, 2.7, 3.14, 5.5, 5.5, 6.1]

    # Пошук верхньої межі для числа 2.7
    iters, ub = binary_search_upper_bound(data, 2.7)
    print(f"Кількість ітерацій: {iters}, upper bound: {ub}")    

    # Пошук верхньої межі для числа 3.0
    iters, ub = binary_search_upper_bound(data, 3.0)
    print(f"Кількість ітерацій: {iters}, upper bound: {ub}")    

    # Пошук верхньої межі для числа 10.0
    iters, ub = binary_search_upper_bound(data, 10.0)
    print(f"Кількість ітерацій: {iters}, upper bound: {ub}")

