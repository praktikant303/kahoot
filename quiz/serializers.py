import django.contrib.auth.models
from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import User, Quiz, Question, Answer
from .utils import send_activation_code


class GroupSerializer(serializers.ModelSerializer):
    """
    Serializer to received users and their detailed information
    Part 1:
    """

    class Meta:
        model = django.contrib.auth.models.Group
        fields = ('name','id')


class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)

    class Meta:
        model = User
        fields = ['name', 'last_name', 'email', 'telephone_number',
                  'total_score', 'ranking', 'ranking_group', 'count_passed_tests', 'groups']


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ['answer_text', 'is_right', 'id']


class QuestionSerializer(serializers.ModelSerializer):
    answer = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'title', 'answer']
        depth = 1


class QuizSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(many=True)

    class Meta:
        model = Quiz
        fields = ['id', 'group', 'title', 'question']


class RegisterUserSerializer(serializers.ModelSerializer):
    """
    Serializer to register new users
    """
    # write_only=True allows only writing passwords
    email = serializers.EmailField()
    password = serializers.CharField(min_length=1, write_only=True, help_text="Minimum length of a password is 1")
    password_confirmation = serializers.CharField(min_length=1, write_only=True)

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("This email already exists")
        return email

    class Meta:
        model = User
        fields = ['email', 'password', 'password_confirmation']

    # writing a validator function, def validators = def clean and validated_data = cleaned_data
    def validate(self, validated_data):
        # the argument can be in query dict {} like {'password':'', 'password_confirm':'', 'email':''}
        print(validated_data)
        password = validated_data.get('password')
        password_confirmation = validated_data.get('password_confirmation')
        if password != password_confirmation:
            raise serializers.ValidationError("Passwords don't match")
        return validated_data

    def create(self, validated_data):
        """This function is called when an object is saved self.save() method is called"""
        email = validated_data.get("email")
        password = validated_data.get("password")
        user = User.objects.create_user(email=email, password=password)
        send_activation_code(email=user.email, activation_code=user.activation_code)
        return user


class LoginSerializer(serializers.Serializer):
    """
    Serializer to login. The serializer inherits from an ordinary serializer (not ModelSerializer),
    because there is no model for login
    """

    email = serializers.EmailField()
    # argument label is analogous to help_text
    # argument trim_whitespace excludes spaces in a CharField
    password = serializers.CharField(
        label='Password',
        style={"input_type": "password"},
        trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            # the authenticate method will check the correctness of email and password
            user = authenticate(request=self.context.get('request'), email=email,
                                password=password)
            if not user:
                message = 'Unable to log in with the provided credentials'
                raise serializers.ValidationError(message, code="authorization")
        else:
            message = 'Must include "email" and "password".'
            raise serializers.ValidationError(message, code="authorization")
        attrs['user'] = user
        return attrs


class AnswerReplySerializer(serializers.Serializer):
    answer_id = serializers.IntegerField(required=True)
    answer_time = serializers.IntegerField(required=True)





