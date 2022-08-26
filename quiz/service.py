from .models import Question, Quiz, User
from django.db.models import Count


def logic(request, answer, answer_time, question_id):

    # 1) setting parameters as the maximum time given per question and the maximum score available
    question_in_subject = Question.objects.get(id=question_id)
    timer = question_in_subject.time_max
    score = question_in_subject.score_max

    # 2) computing the score for the answer
    if answer.is_right:
        if timer > answer_time:
            request.user.question_score = round(score * (1 - answer_time / timer), 1)
            request.user.save()
        else:
            request.user.question_score = 0
            request.user.save()
    else:
        request.user.question_score = 0
        request.user.save()

    # 3) updating record of answers replied and their scores
    # in a dictionary that can be stored and retrieved from the database

    record_of_scores = request.user.replied_questions_and_scores
    record_of_scores[str(question_id)] = request.user.question_score
    request.user.total_score = sum(record_of_scores.values())
    print(record_of_scores)

    # 4) Counting the number of passed tests:

    # Getting all quizzes and answers related to the user in a convenient format
    # setting a variable to work with quizzes in a dictionary format
    all_quizzes = request.user.quizzes_and_answers

    # getting all quizzes related to the user
    number_quizzes = Quiz.objects.filter(group__in=request.user.groups.all())

    # getting a string of all questions by quizzes to ease comparison with the
    # submitted answers of the user
    for item in number_quizzes:
        number_questions = []
        for element in Question.objects.filter(quiz__id=item.id):
            number_questions.append(str(element.id))
        all_quizzes[str(item.id)] = number_questions
    request.user.save()
    print(all_quizzes)

    submitted_answers_string = []
    for item in record_of_scores.keys():
        submitted_answers_string.append(item)
    print(submitted_answers_string)
    print("All quizzes are ", all_quizzes)

    # 4.2) Counting passed tests
    count_passed_tests = 0
    for item in all_quizzes:
        if set(all_quizzes[item]).issubset(submitted_answers_string):
            print(all_quizzes[item])
            count_passed_tests = count_passed_tests + 1

    print(count_passed_tests)
    request.user.count_passed_tests = count_passed_tests
    request.user.replied_questions_and_scores = record_of_scores

    request.user.save()
    return request.user.question_score


def count_ranking(user_details):
    """
    Returns global ranking of users
    # """
    # user_details = User.objects.alias(score=Count('total_score')).order_by('-total_score')
    ranking = 1
    for item in user_details:
        item.ranking = ranking
        item.save()
        print(item, ranking)
        ranking = ranking + 1


def count_ranking_group(request, **kwargs):
    """
    Returns ranking of users by groups, given inputted name of group
    """
    user_details = User.objects.filter(groups__name=kwargs['group_name']).order_by('-total_score')
    ranking = 1
    for item in user_details:
        item.ranking_group = ranking
        item.save()
        print(item, ranking)
        ranking = ranking + 1

