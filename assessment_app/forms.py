from django import forms
from .models import SportAssessment

class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = SportAssessment
        fields = ['sport_type', 'video']
    
    def clean_video(self):
        video = self.cleaned_data.get('video')
        if video:
            if not video.name.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
                raise forms.ValidationError("Unsupported file format. Please upload MP4, AVI, MOV, or MKV.")
            if video.size > 100 * 1024 * 1024:  # 100MB limit
                raise forms.ValidationError("File too large. Maximum size is 100MB.")
        return video