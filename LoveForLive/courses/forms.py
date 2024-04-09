from django import forms
from .models import LessonProgress


LessonProgressFormSet = forms.modelformset_factory(
    LessonProgress,
    fields=('status', 'feedback'),
    max_num=1,
    widgets={
        'status': forms.CheckboxInput(attrs={'class': 'checkbox_tasks'}),
        'feedback': forms.Textarea(attrs={'class': 'feedback_tasks'})},
    labels={'status': 'Отметка о выполнении задания', 'feedback': 'Обратная связь по результатам выполнения задания'}
)
