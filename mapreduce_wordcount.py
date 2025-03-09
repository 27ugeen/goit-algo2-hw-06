import string
import requests
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict

def get_text(url):
    """Завантажує текст за URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException:
        print("❌ Помилка: Не вдалося отримати вхідний текст.")
        return None

def remove_punctuation(text):
    """Видаляє знаки пунктуації з тексту."""
    return text.translate(str.maketrans("", "", string.punctuation))

def map_function(word):
    """Функція Map: повертає пару (слово, 1)."""
    return word.lower(), 1  # Переводимо слова в нижній регістр

def shuffle_function(mapped_values):
    """Функція Shuffle: групує значення за словами."""
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()

def reduce_function(key_values):
    """Функція Reduce: підраховує кількість входжень слова."""
    key, values = key_values
    return key, sum(values)

def map_reduce(text, search_words=None):
    """Виконує MapReduce для підрахунку частоти слів у тексті."""
    text = remove_punctuation(text)
    words = text.split()

    if search_words:
        words = [word for word in words if word.lower() in search_words]

    with ThreadPoolExecutor() as executor:
        mapped_values = list(executor.map(map_function, words))

    shuffled_values = shuffle_function(mapped_values)

    with ThreadPoolExecutor() as executor:
        reduced_values = list(executor.map(reduce_function, shuffled_values))

    return dict(reduced_values)

def visualize_top_words(word_counts, top_n=10):
    """Візуалізує топ N слів за частотою використання."""
    sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:top_n]

    words, counts = zip(*sorted_words)
    
    plt.figure(figsize=(10, 5))
    plt.bar(words, counts, color='skyblue')
    plt.xlabel("Слова")
    plt.ylabel("Кількість входжень")
    plt.title(f"Топ-{top_n} найбільш уживаних слів")
    plt.xticks(rotation=45)
    plt.show()

if __name__ == '__main__':
    url = "https://gutenberg.net.au/ebooks01/0100021.txt"
    text = get_text(url)

    if text:
        result = map_reduce(text)

        print("🔢 Топ-10 слів з найбільшою частотою:")
        sorted_result = sorted(result.items(), key=lambda x: x[1], reverse=True)[:10]
        for word, count in sorted_result:
            print(f"{word}: {count}")

        visualize_top_words(result, top_n=10)