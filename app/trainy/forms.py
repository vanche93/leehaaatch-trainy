from django import forms
from .models import TrainingReq, TrainingTime, TrainingTopic, Training


class TrainingReqForm(forms.ModelForm):
    class Meta:
        model = TrainingReq
        fields = ["training_times", "topics"]
        widgets = {
            "training_times": forms.CheckboxSelectMultiple(),
            "topics": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, training=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["training_times"].queryset = training.training_times.all()
        self.fields["topics"].queryset = training.topics.all()
