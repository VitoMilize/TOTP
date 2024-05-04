import math

def entropy_collector(data):
    frequencies = {}
    for char in data:
        if char in frequencies:
            frequencies[char] += 1
        else:
            frequencies[char] = 1

    # Рассчитываем энтропию
    entropy = 0
    total_chars = len(data)
    for frequency in frequencies.values():
        probability = frequency / total_chars
        entropy -= probability * math.log2(probability)

    return entropy

data = "aSAAAAda"
result_entropy = entropy_collector(data)
print("Entropy:", result_entropy)