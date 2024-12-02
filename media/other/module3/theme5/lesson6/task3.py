class CipherMaster:
    alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

    def cipher(self, original_text, shift):
        if shift < 0:
            shift %= -len(CipherMaster.alphabet)
        else:
            shift %= len(CipherMaster.alphabet)
        cipher_text = ""
        for letter in original_text:
            if letter.lower() in CipherMaster.alphabet:
                letter_index = CipherMaster.alphabet.index(letter.lower()) + shift
                if letter_index >= len(CipherMaster.alphabet):
                    letter_index = letter_index % len(CipherMaster.alphabet)
                cipher_text += CipherMaster.alphabet[letter_index]
            else:
                cipher_text += letter
        return cipher_text

    def decipher(self, cipher_text, shift):
        shift *= -1
        if shift < 0:
            shift %= -len(CipherMaster.alphabet)
        else:
            shift %= len(CipherMaster.alphabet)
        original_text = ""
        for letter in cipher_text:
            if letter.lower() in CipherMaster.alphabet:
                letter_index = CipherMaster.alphabet.index(letter.lower()) + shift
                if letter_index < 0:
                    letter_index = len(CipherMaster.alphabet) + letter_index
                elif letter_index >= len(CipherMaster.alphabet):
                    letter_index %= len(CipherMaster.alphabet)
                original_text += CipherMaster.alphabet[letter_index]
            else:
                original_text += letter
        return original_text


cipher_master = CipherMaster()
print(cipher_master.decipher(
    cipher_text='яяя',
    shift=-32
))
