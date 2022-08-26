from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin, Group
from django.core.validators import FileExtensionValidator


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if email is None:
            raise TypeError("User must have an email")
        user = self.model(email=self.normalize_email(email))
        user.is_active = False
        user.set_password(password)
        user.create_activation_code()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        if email is None:
            raise TypeError("Superuser must have a username")
        if password is None:
            raise TypeError("Superuser must have a password")
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
        )
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Creating User attributes
    """
    name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, default="", blank=True)
    email = models.EmailField(unique=True, primary_key=True)
    telephone_number = models.IntegerField(null=True, blank=True)
    question_score = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
    replied_questions_and_scores = models.JSONField(default=dict, null=True, blank=True)
    total_score = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
    ranking = models.PositiveSmallIntegerField(editable=False, null=True, blank=True)
    ranking_group = models.PositiveSmallIntegerField(editable=False, null=True, blank=True)
    count_passed_tests = models.PositiveSmallIntegerField(default=0, blank=True)
    is_staff = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=50, blank=True)
    quizzes_and_answers = models.JSONField(default=dict, null=True, blank=True)


    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["email"]

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.email

    def list_of_groups(self):
        print(self.groups.all(), type(self.groups.all()))
        return ', '.join(map(str, self.groups.all()))

    def create_activation_code(self):
        """
        encoding, possible ways:
        1) hashlib.md5(self.email + str(self.id)).encode() --> hexdigest()
        example: email = test@test.com, id = 155 --> activation code: jqdnreqjvb14trf8071g35bc9
        2) get_random_string(50, allowed_char=[0fh15570ch1- q9aecu130])
        3) UUID
        4) datetime.activate.now() or time.time() + timestamp() 01.01.1970
        """
        import hashlib
        string = str(self.email) + str(self.groups)
        encode_string = string.encode()
        md5_object = hashlib.md5(encode_string)
        activation_code = md5_object.hexdigest()
        self.activation_code = activation_code


class Quiz(models.Model):
    """
    Creating attributes for Quizzes
    """

    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizzes"

    title = models.CharField(max_length=255, default="New Quiz",
                             verbose_name="Quiz Title", unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    group = models.ManyToManyField(Group, related_name="group_quizzes")

    def list_of_groups_quizzes(self):
        return ', '.join(map(str, self.group.all()))

    def __str__(self):
        return self.title


class Updated(models.Model):
    date_updated = models.DateTimeField(
        verbose_name="Last updated", auto_now=True)

    # abstract = True makes Updated class abstract, which allows to put some common
    # information into a number of other models.
    class Meta:
        abstract = True


class Question(Updated):
    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    quiz = models.ManyToManyField(Quiz, related_name='question')
    title = models.CharField(max_length=255, verbose_name="Title")
    question_image = models.ImageField(upload_to='media', null=True, blank=True, validators=[FileExtensionValidator(
        allowed_extensions=['png', 'jpg'])], help_text="Only .png and .jpg formats are allowed",
                                       error_messages={'invalid': 'Only jpg and png formats'})
    date_created = models.DateTimeField(
        auto_now_add=True, verbose_name="Date Created")
    time_max = models.FloatField(default=20.0, help_text="Maximum allowed time for question")
    answer_score = models.FloatField(default=0, help_text="Score for the answer")
    score_max = models.FloatField(default=100.0, help_text="Maximum score", blank=True)
    is_active = models.BooleanField(default=False, verbose_name="Active Status")

    def get_quizzes(self):
        return "\n".join([q.title for q in self.quiz.all()])

    def __str__(self):
        return self.title


class Answer(Updated):
    class Meta:
        verbose_name = "Answer"
        verbose_name_plural = "Answers"
        ordering = ["id"]

    question = models.ForeignKey(Question, related_name="answer", on_delete=models.DO_NOTHING)
    answer_text = models.CharField(max_length=255, verbose_name="Answer Text")
    time_taken_to_answer = models.FloatField(default=20.0, help_text="Time take to answer")
    answer_score = models.PositiveSmallIntegerField(default=100, help_text="Score for the answer")
    is_right = models.BooleanField(default=False)

    def __str__(self):
        return self.answer_text


class Leader(User):
    class Meta:
        verbose_name = "Leader"
        verbose_name_plural = "Leaders"
        proxy = True



