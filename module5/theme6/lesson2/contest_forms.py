from django import forms


class ContestForm(forms.Form):

	title = forms.CharField(label='Название', max_length=20)
	description = forms.CharField(
		label='Описание',
		help_text='',
		widget=forms.Textarea(),
	)
	price = forms.IntegerField(
		label='Цена',
		max_value=100,
		min_value=10,
		help_text='Рекомендованная розничная цена',
	)
	comment = forms.CharField(
		label='Комментарий',
		help_text='',
		widget=forms.Textarea(),
		required=False,
	)
