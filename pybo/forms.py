from django import forms

from .models import Question, Answer

# code line


class QuestionForm(forms.ModelForm):
    # django에서는 모델폼에 대해서 반드시 모델 폼이 사용할 모델들과 모델의 필드들을 적어야한다.
    class Meta:
        model = Question
        # views에서 끌어와 쓸때 이 fields값에 대해서 전달이 되며, as_p로 파싱된다.
        # 물론 선행적으로 바로 위에 연결된 model, 더위의 ModelForm은 선행으로 있어야하며
        # model에 연결된 클라스가 비롯된 models에서 fields의 내용은 정의되어있어야 한다.
        fields = ['subject', 'content']

        # .as_p는 css적용이 안되기때문에 css적용을 위한 수식을 여기에 써준다.
        # 하지만 as_p의 경우. 사용엔 문제가 없지만 해당 as_p로 긁어지는 내용이 많아질수록
        # 에러가 발생할 가능성이 커지니 가급적 사용하지는 않는다.
        # widgets = {
        #     'subject': forms.TextInput(attrs={'class': 'form-control'}),
        #     'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10})
        # }

        # 사용하는 태그와 화면에 노출되는 이름이 다를 경우에 정의
        labels = {
            'subject': 'title'
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {
            'content': 'answer content'
        }
