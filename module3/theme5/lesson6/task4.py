class CipherMaster:
    alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

    def process_text(self, text, shift, is_encrypt):
        if not is_encrypt:
            shift *= -1
        
        if shift < 0:
            shift %= -len(CipherMaster.alphabet)
        else:
            shift %= len(CipherMaster.alphabet)
        
        new_text = ""
        for letter in text:
            if letter.lower() in CipherMaster.alphabet:
                letter_index = CipherMaster.alphabet.index(letter.lower()) + shift
                if letter_index < 0:
                    letter_index = len(CipherMaster.alphabet) + letter_index
                elif letter_index >= len(CipherMaster.alphabet):
                    letter_index %= len(CipherMaster.alphabet)
                new_text += CipherMaster.alphabet[letter_index]
            else:
                new_text += letter
        return new_text


cipher_master = CipherMaster()
print(cipher_master.process_text(
    text='Однажды ревьюер принял проект с первого раза, с тех пор я его боюсь',
    shift=2,
    is_encrypt=True
))
print(cipher_master.process_text(
    text='Олебэи яфвнэ мроплж сэжи — э пэй рдв злййвкпш лп нвящывнэ',
    shift=-3,
    is_encrypt=False
))
