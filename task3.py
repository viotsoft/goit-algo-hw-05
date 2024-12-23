def boyer_moore_search(text:str, pattern:str) -> int:
    """
    Повертає індекс першого входження pattern у text 
    або -1, якщо підрядка не знайдено.
    
    Ідея Боєра-Мура:
    - Перебираємо текст зліва направо, але зі стрибками.
    - При порівнянні зразка з фрагментом тексту порівнюємо символи з кінця зразка.
    - Використовуємо таблицю поганих символів (bad character rule), 
      а за бажанням і таблицю хороших суфіксів (good suffix rule) 
      для оптимізації стрибків.
    """
    # Побудова таблиці зсувів (bad character table)
    # Ключ: символ, Значення: відстань до кінця pattern
    # При відсутності символа в pattern зсув = довжина pattern
    bad_char_shift = {}
    m = len(pattern)
    n = len(text)

    for i in range(m-1):
        bad_char_shift[pattern[i]] = m - i - 1

    # Пошук
    index = 0
    while index <= n - m:
        # Порівняння зразка з текстом зправа наліво
        j = m - 1 
        while j >= 0 and text[index + j] == pattern[j]:
            j -= 1

        if j < 0:
        # Зразок знайдено
            return index 
        else:
            # Дізнаємося, наскільки посунути вікно
            # Якщо символ не знайдено в таблиці, зсув = m (довжина pattern)
            shift = bad_char_shift.get(text[index + j], m)
            #  Зсув може бути мінімум 1
            index += max(1, shift - (m - 1 - j))
    
    return -1


def kmp_search(text: str, pattern: str) -> int:
    
    """
    Ідея KMP:
    - Попередньо будуємо масив "найдовшого суфікса, що дорівнює префіксу" (lps).
    - З його допомогою уникаємо повторного порівняння символів.
    """
# Побудова lps-масиву (longest proper prefix which is also suffix)
def build_lps(p: str):
    lps = [0] * len(p)
    prefix_len = 0 # довжина поточного префікса
    i = 1

    while i < len(p):
        if p[i] == p[prefix_len]:
            prefix_len += 1
            lps[i] = prefix_len
            i += 1
        else:
            if prefix_len != 0:
                prefix_len = lps[prefix_len -1]
            else:
                lps[i] = 0
                i += 1
    return lps  

    lps = build_lps(pattern)
    i = 0
    j = 0

    while i < len(text):
        if text[i] == pattern[j]:
            i += 1
            j += 1
        if j == len(pattern):
            return i - j
        elif i < len(text) and text[i] != pattern[j]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return -1


def rabin_karp_search(text: str, pattern: str, base: int = 256, q: int = 101) -> int:
    """
    Повертає індекс першого входження pattern у text 
    або -1, якщо підрядка не знайдено.

    Ідея алгоритму:
    - Обчислювати хеш текстового вікна та хеш pattern і порівнювати їх.
    - Якщо хеші збігаються, додатково перевірити символи (через колізії).
    - Використовуємо rolling hash для просування вікна.
    
    Параметри:
    - base: основа (зазвичай беруть 256 для ASCII)
    - q: просте число, що використовується як модуль для унеможливлення великих значень хешу
    """
    m = len(pattern)
    n = len(text)
    if m > n:
        return -1

    # Попередні обчислення: (base^(m-1)) % q
    h = 1
    for _ in range(m - 1):
        h = (h * base) % q

    # Обчислюємо хеш першого вікна text і хеш pattern
    pattern_hash = 0
    window_hash = 0

    for i in range(m):
        pattern_hash = (base * pattern_hash + ord(pattern[i])) % q
        window_hash = (base * window_hash + ord(text[i])) % q

    # Прокручуємо вікно по text
    for i in range(n - m + 1):
        # Якщо хеші збігаються — перевіряємо символи (потрібно для уникнення колізій)
        if pattern_hash == window_hash:
            # Перевірка посимвольно
            if text[i:i+m] == pattern:
                return i

        # Якщо не останнє вікно, "зсуваємо" хеш
        if i < n - m:
            window_hash = (window_hash - ord(text[i]) * h) % q
            window_hash = (window_hash * base + ord(text[i + m])) % q
            window_hash = (window_hash + q) % q  # щоб уникнути від'ємних значень

    return -1


import timeit

def benchmark_algorithms(text_file_path, pattern_exists, pattern_absent):
    """
    Вимірює час пошуку 2-х підрядків (один існує, інший - ні)
    у вказаному файлі. Повертає результати вимірювань у вигляді словника.
    """

    # 1. Зчитаємо текст
    with open(text_file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # 2. Підготуємо лямбда-функції для timeit
    setup_code = (
        "from __main__ import boyer_moore_search, kmp_search, rabin_karp_search, text, pattern_exists, pattern_absent"
    )

    # Для тексту, де підрядок ІСНУЄ
    boyer_moore_exists = timeit.timeit(
        stmt="boyer_moore_search(text, pattern_exists)",
        setup=setup_code,
        number=1  # кількість повторів, можна збільшити для точнішої оцінки
    )

    kmp_exists = timeit.timeit(
        stmt="kmp_search(text, pattern_exists)",
        setup=setup_code,
        number=1
    )

    rabin_karp_exists = timeit.timeit(
        stmt="rabin_karp_search(text, pattern_exists)",
        setup=setup_code,
        number=1
    )

    # Для тексту, де підрядок НЕ ІСНУЄ
    boyer_moore_absent = timeit.timeit(
        stmt="boyer_moore_search(text, pattern_absent)",
        setup=setup_code,
        number=1
    )

    kmp_absent = timeit.timeit(
        stmt="kmp_search(text, pattern_absent)",
        setup=setup_code,
        number=1
    )

    rabin_karp_absent = timeit.timeit(
        stmt="rabin_karp_search(text, pattern_absent)",
        setup=setup_code,
        number=1
    )

    return {
        'file': text_file_path,
        'exists_pattern': pattern_exists,
        'absent_pattern': pattern_absent,
        'boyer_moore_exists': boyer_moore_exists,
        'kmp_exists': kmp_exists,
        'rabin_karp_exists': rabin_karp_exists,
        'boyer_moore_absent': boyer_moore_absent,
        'kmp_absent': kmp_absent,
        'rabin_karp_absent': rabin_karp_absent
    }


if __name__ == "__main__":
    # Задайте свої підрядки, що існують/не існують у тексті
    pattern_exists_text1 = "Hello"        # Наприклад, знаємо, що в text1.txt точно є "Hello"
    pattern_absent_text1 = "QwertyXYZ"    # Вигаданий підрядок, якого немає в text1.txt

    pattern_exists_text2 = "function"     # Для text2.txt, припустимо, там є слово "function"
    pattern_absent_text2 = "NoMatchHere"  # Підрядок, якого немає

    # Глобальні змінні, які потрібні у setup_code
    global text, pattern_exists, pattern_absent

    # Виконуємо для першого файлу
    text_file1 = "text1.txt"
    text = ""
    pattern_exists = pattern_exists_text1
    pattern_absent = pattern_absent_text1

    results1 = benchmark_algorithms(text_file1, pattern_exists, pattern_absent)

    # Виконуємо для другого файлу
    text_file2 = "text2.txt"
    text = ""
    pattern_exists = pattern_exists_text2
    pattern_absent = pattern_absent_text2

    results2 = benchmark_algorithms(text_file2, pattern_exists, pattern_absent)

    # Друкуємо результати
    print("Результати для text1.txt:")
    print(results1, "\n")
    print("Результати для text2.txt:")
    print(results2, "\n")

    
