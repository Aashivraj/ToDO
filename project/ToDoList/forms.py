from django import forms
from .models import *
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import password_validation


class TeamForm(forms.ModelForm):
    team_department = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Team Department",
                "id": "user_team_department",
            }
        ),
    )

    class Meta:
        model = Team
        fields = "__all__"


class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = "__all__"


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ["title", "description", "note", "status", "user", "team"]

        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter title"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter description",
                    "rows": 4,
                }
            ),
            "note": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter note",
                    "rows": 2,
                }
            ),
            "status": forms.HiddenInput(),
            "user": forms.HiddenInput(),
            "team": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(TodoForm, self).__init__(*args, **kwargs)
        if user:
            self.fields["user"].initial = user
            self.fields["team"].initial = user.team if user.team else None


class TodoForm_Comment(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ["title", "description", "note", "status", "updated_by"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "readonly": True,
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "readonly": True,
                    "rows": 4,
                }
            ),
            "note": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter note",
                    "rows": 2,
                    "label": "comment",
                }
            ),
            "status": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "readonly": True,
                }
            ),
            "updated_by": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "readonly": True,
                }
            ),
        }
        labels = {
            "note": "Comment",  # Change label from 'note' to 'Comment'
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)  # Store user
        super(TodoForm_Comment, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        note = cleaned_data.get("note")
        initial_note = self.instance.note if self.instance else None
        current_status = cleaned_data.get("status")

        # Check if note has changed and update status accordingly
        if note != initial_note and current_status == 1:
            cleaned_data["status"] = 0

        return cleaned_data

    def save(self, commit=True):
        todo = super().save(commit=False)
        new_note = self.cleaned_data.get("note")

        if new_note:
            Notes.objects.create(
                todo=todo,
                user=self.user,
                team=todo.team,
                description=new_note,
                updated_by=self.user.get_username(),
            )

            Notification.objects.create(
                sender=self.user,
                receiver=todo.user,  # Assuming the task owner should be notified
                todo=todo,
                message=f"{self.user.get_username()} added/edited a comment: {new_note}",
            )

        todo.updated_by = self.user.get_username()  # Set updated_by here

        if commit:
            todo.save()

        return todo


class UserForm(forms.ModelForm):
    user_name = forms.CharField(
        required=False,  # Remove HTML5 required
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "User Name",
                "id": "customuser_username",
            }
        ),
    )
    email = forms.EmailField(
        required=False,  # Remove HTML5 required
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Email Address",
                "id": "customuser_email",
            }
        ),
    )
    mobile_number = forms.CharField(
        required=False,  # Remove HTML5 required
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Mobile Number",
                "id": "customuser_mobile_number",
            }
        ),
    )
    team = forms.ModelChoiceField(
        queryset=Team.objects.all(),
        required=False,  # Remove HTML5 required
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "id": "customuser_team",
            }
        ),
    )
    role = forms.ChoiceField(
        required=False,  # Remove HTML5 required
        choices=[
            ("3", "Developer"),  # Default choices
        ],
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "id": "customuser_role",
            }
        ),
    )

    class Meta:
        model = CustomUser
        fields = ("user_name", "email", "mobile_number", "team", "role")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            if user.role == "1":  # Admin
                self.fields["role"].choices = [("2", "TeamLeader")]
            elif user.role == "2":
                self.fields["team"].widget.attrs["style"] = "display:none;"
                self.fields["team"].label = ""
                self.fields["role"].choices = [("3", "Developer")]


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Username", "class": "form-control"}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password", "class": "form-control"}
        )
    )


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=("Old password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "autofocus": True,
                "class": "form-control",
            }
        ),
    )
    new_password1 = forms.CharField(
        label=("New password"),
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "class": "form-control"}
        ),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),  # type: ignore
    )
    new_password2 = forms.CharField(
        label=("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "class": "form-control"}
        ),
    )


class UserForm_Update(forms.ModelForm):
    user_name = forms.CharField(
        required=False,  # Remove HTML5 required
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "User Name",
                "id": "customuser_username",
            }
        ),
    )
    email = forms.EmailField(
        required=False,  # Remove HTML5 required
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Email Address",
                "id": "customuser_email",
            }
        ),
    )
    mobile_number = forms.CharField(
        required=False,  # Remove HTML5 required
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Mobile Number",
                "id": "customuser_mobile_number",
            }
        ),
    )
    team = forms.ModelChoiceField(
        queryset=Team.objects.all(),
        required=False,  # Remove HTML5 required
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "id": "customuser_team",
            }
        ),
    )
    role = forms.ChoiceField(
        required=False,  # Remove HTML5 required
        choices=[
            ("3", "Developer"),  # Default choices
        ],
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "id": "customuser_role",
            }
        ),
    )

    class Meta:
        model = CustomUser
        fields = ("user_name", "email", "mobile_number", "team", "role")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            if user.role == "1":  # Admin
                self.fields["role"].choices = [("1", "Admin")]
            elif user.role == "2":

                self.fields["role"].choices = [("2", "Teamlead")]
            elif user.role == "3":

                self.fields["role"].choices = [("3", "Developer")]
