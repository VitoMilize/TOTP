import math

import keyboard


def entropy_check(data):
    frequencies = {}
    for char in data:
        if char in frequencies:
            frequencies[char] += 1
        else:
            frequencies[char] = 1

    entropy = 0
    total_chars = len(data)
    for frequency in frequencies.values():
        probability = frequency / total_chars
        entropy -= probability * math.log2(probability)

    return entropy


def generate_entropy():
    print("Собираем энтропию... (нажмите Esc для завершения)")

    entropy = []
    def on_key_event(event):
        try:
            key = event.name
            if len(key) == 1:
                entropy.append(key)
                print("Добавлено: ", key)
        except AttributeError:
            pass

    keyboard.on_press(on_key_event)

    keyboard.wait("esc")

    keyboard.unhook_all()

    return ''.join(entropy)


if __name__ == "__main__":
    entropy = generate_entropy()
    result_entropy = entropy_check(entropy)
    print("Entropy:", result_entropy)
