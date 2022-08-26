from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Count
from rest_framework import status, filters
from rest_framework.response import Response
from rest_framework.decorators import api_view, APIView, action
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework import generics, viewsets

from .models import *
from .serializers import *
from .service import logic, count_ranking, count_ranking_group


class UserLISTView(APIView):
    """
    Returns a list of all users
    """
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        user_details = User.objects.all()
        serializer = UserSerializer(user_details, many=True)
        return Response(serializer.data)


class SearchByParams(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'last_name', 'telephone_number']


'''LEADERS DASHBOARD'''


class UserLISTViewTop(APIView):
    """
    Global leaders, the class returns a list of the three top users across Groups
    """
    def get(self, request):
        user_details = User.objects.alias(score=Count('total_score')).order_by('-total_score')
        serializer = UserSerializer(user_details, many=True)
        count_ranking(user_details)
        return Response(serializer.data)


class UserLISTViewTopByGroup(APIView):
    """
    Leaders by Groups, returns a list of users given name of a Group
    """
    def get(self, request, **kwargs):
        user_details = User.objects.filter(groups__name=kwargs['group_name']).order_by('-total_score')[:3]
        serializer = UserSerializer(user_details, many=True)
        count_ranking_group(request, **kwargs)
        return Response(serializer.data)


'''SEARCH FUNCTIONS'''


class UserSearchNameView(APIView):
    """
    Search by name
    """
    def get(self, request, **kwargs):
        user_details = User.objects.filter(name=kwargs['user_name'])
        serializer = UserSerializer(user_details, many=True)
        return Response(serializer.data)


class UserSearchLastNameView(APIView):
    """
    Search by last name
    """
    def get(self, request, **kwargs):
        user_details = User.objects.filter(last_name=kwargs['user_last_name'])
        serializer = UserSerializer(user_details, many=True)
        return Response(serializer.data)


class UserSearchPhoneView(APIView):
    """Search by phone number"""
    def get(self, request, **kwargs):
        user_details = User.objects.filter(telephone_number=kwargs['phone'])
        serializer = UserSerializer(user_details, many=True)
        return Response(serializer.data)


'''REGISTRATION, LOGIN, LOGOUT'''


class RegisterUserView(APIView):
    """
    Register View
    """
    @swagger_auto_schema(request_body=RegisterUserSerializer)
    def post(self, request):
        data = request.data
        serializer = RegisterUserSerializer(data=data)
        print(request.user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Successfully signed up', status=status.HTTP_201_CREATED)


class ActivateView(APIView):
    """
    Activation of a User
    """
    def get(self, request, activation_code):
        User = get_user_model()
        # the get_object_or_404 method is used to give an error message if
        # the user in subject doesn't exist
        user = get_object_or_404(User, activation_code=activation_code)
        user.is_active = True
        # once an activation code is generated and the user activates his account
        # the code will be stored in the database. In order to make sure that the user
        # won't activate himself multiple times, we need to clear the field and set it blank.
        user.activation_code = ''
        user.save()
        return Response("Your account was successfully activated", status=status.HTTP_200_OK)


class LoginView(ObtainAuthToken):
    """
    Login View
    ObtainAuthToken already has a built-in serializer and a built-in post method
    In this particular case, we'll use a customized serializer
    """
    serializer_class = LoginSerializer


class LogoutView(APIView):
    """
    Logout View
    """
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        user = request.user
        # creating tokens that allow users to visit all sites
        Token.objects.filter(user=user).delete()
        return Response('Successfully logged out', status=status.HTTP_200_OK)


""" QUIZ RELATED FUNCTIONS"""


class GroupByUserAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = GroupSerializer

    def get(self, request):
        results = Group.objects.filter(user=request.user)
        serializer = GroupSerializer(results, many=True)
        print(request.user.replied_questions_and_scores)
        return Response(serializer.data)


class QuizByUserAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        queryset = Quiz.objects.filter(group__in=request.user.groups.all())
        # queryset = Quiz.objects.none()
        # list_of_groups = Group.objects.filter(user=request.user)
        # for item in list_of_groups:
        #     queryset = queryset | Quiz.objects.filter(id=item.id)
        #     print(Quiz.objects.filter(id=item.id))
        serializer = QuizSerializer(queryset, many=True)
        print(request.user.name)
        return Response(serializer.data)


class GetValidQuestionsAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = AnswerReplySerializer

    def get_queryset(self):
        answer_id = self.request.data.get("answer_id")
        answer = Answer.objects.get(id=answer_id)
        print(answer_id, answer)
        return answer

    def post(self, request, quiz_id, question_id, **kwargs):
        answer = self.get_queryset()
        time_answer = request.data.get('answer_time')
        logic(request, answer, time_answer, question_id)
        return Response('Your answer has been submitted')





