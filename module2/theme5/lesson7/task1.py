a = 'Роботы стали важны'
b = 'в период'
c = 'эмиграции с Терры'

first_word = a[4:7]
second_word = b[2:8:2] + c[3: 6] + c[1] * 2 + c[2] + a[7:9]
print(first_word + second_word)