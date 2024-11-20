def split_message(message, max_length=1600):
    """
    Divide un mensaje largo en fragmentos más pequeños, asegurándose de no cortar palabras.

    :param message: El mensaje largo que deseas dividir.
    :param max_length: El tamaño máximo permitido para cada fragmento (por defecto 1600).
    :return: Una lista con los fragmentos del mensaje.
    """
    if len(message) <= max_length:
        return [message.strip()]

    words = message.split()
    parts = []
    current_part = []

    for word in words:
        potential_length = sum(len(w) + 1 for w in current_part) + len(word)

        if potential_length > max_length:
            parts.append(" ".join(current_part))
            current_part = [word]
        else:
            current_part.append(word)
    if current_part:
        parts.append(" ".join(current_part))

    return parts
