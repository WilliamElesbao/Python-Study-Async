from django.shortcuts import render, redirect
from .models import Category, Flashcard, Challenge, FlashcardChallenge
from django.http import HttpResponse, Http404
from django.contrib.messages import constants
from django.contrib import messages

def new_flashcard(request):
    if not request.user.is_authenticated:
        return redirect('/users/login')
    
    if request.method == "GET":
        categories = Category.objects.all()
        difficulties = Flashcard.DIFFICULTY_CHOICES
        flashcards = Flashcard.objects.filter(user = request.user)
        category_filter = request.GET.get('category')
        difficulty_filter = request.GET.get('difficulty')

        if (category_filter):
            flashcards = flashcards.filter(category__id = category_filter)

        if (difficulty_filter):
            flashcards = flashcards.filter(difficulty = difficulty_filter)

        return render(request, 'new_flashcard.html', {'categories': categories, 'difficulties': difficulties, 'flashcards': flashcards})

    elif request.method == 'POST':
        question = request.POST.get('question')
        answer = request.POST.get('answer')
        category = request.POST.get('category')
        difficulty = request.POST.get('difficulty')

        if len(question.strip()) == 0 or len(answer.strip()) == 0:
            messages.add_message(request, constants.ERROR, "Fill in the question and answer fields")
            return redirect('/flashcard/new_flashcard/')

        flashcard = Flashcard(
            user = request.user,
            question = question,
            answer = answer,
            category_id = category,
            difficulty = difficulty
        )

        flashcard.save()

        messages.add_message(request, constants.SUCCESS, "Flashcard successfully registered")
        return redirect ('/flashcard/new_flashcard')

def delete_flashcard(request, id):
    
    flashcard = Flashcard.objects.get(id = id)
    flashcard.delete()
    messages.add_message(request, constants.SUCCESS, "Flashcard successfully deleted!")
    return redirect('/flashcard/new_flashcard/')

def start_challenge(request):
    if request.method == "GET":
        categories = Category.objects.all()
        difficulties = Flashcard.DIFFICULTY_CHOICES
        return render(request, 'start_challenge.html',{'categories': categories, 'difficulties': difficulties})
    elif request.method == "POST":
        title = request.POST.get('title')
        category = request.POST.getlist('category')
        difficulty = request.POST.get('difficulty')
        qnt_questions = request.POST.get('qnt_questions')

        challenge = Challenge(
            user = request.user,
            title = title,
            quantity_questions = qnt_questions,
            difficulty = difficulty,
        )

        challenge.save()

        # são equivalentes:
        challenge.category.add(*category) # "for inline"

        # for category in categories:         # for "normal"
        #     challenge.category.add(category)

        flashcards = (
            Flashcard.objects.filter(user = request.user)
            .filter(difficulty = difficulty)
            .filter(category_id__in = category)
            .order_by('?') # id (id de forma crescente) / -id(id de forma descrescente) - ?(traz os dados de forma aleatória)
        )

        if flashcards.count() < int(qnt_questions):

            messages.add_message(request, constants.ERROR,(f"You requested {qnt_questions} flashcard. However, there are only {flashcards.count()} flashcards registrations.!"))
            return redirect ('/flashcard/start_challenge/')

        flashcards = flashcards[: int(qnt_questions)]

        for f in flashcards:
            flashcard_challenge =  FlashcardChallenge(
                flashcard = f
            )
            flashcard_challenge.save()
            challenge.flashcards.add(flashcard_challenge)

        challenge.save()

        return redirect('/flashcard/list_challenge')

def list_challenge(request):
    challenge = Challenge.objects.filter(user=request.user)

    categories = Category.objects.all()
    difficulties = Flashcard.DIFFICULTY_CHOICES

    category = request.GET.get('category')
    difficulty = request.GET.get('difficulty')

    if category:
        challenge = challenge.filter(category__id=category)
    if difficulty:
        challenge = challenge.filter(difficulty=difficulty)

    return render(request, 'list_challenge.html', {'challenges': challenge, 'categories': categories, 'difficulties':difficulties})

def challenge(request, id):
    challenge = Challenge.objects.get(id=id)
    
    if not challenge.user == request.user:
        raise Http404()
    
    if request.method == "GET":
        hits = challenge.flashcards.filter(answered = True).filter(gotItRight = True).count()
        errors = challenge.flashcards.filter(answered = True).filter(gotItRight = False).count()
        missing = challenge.flashcards.filter(answered = False).count()
        return render (request, 'challenge.html', {'challenge':challenge, 'hits':hits, 'errors':errors, 'missing':missing})
    
    return HttpResponse(id)

def toRespond_flashcard(request, id):

    flashcard_challenge = FlashcardChallenge.objects.get(id=id)
    right = request.GET.get('right')
    challenge_id = request.GET.get('challenge_id')

    if not flashcard_challenge.flashcard.user == request.user:
        raise Http404()


    flashcard_challenge.answered = True

    flashcard_challenge.gotItRight = True if right == '1' else False
    flashcard_challenge.save()

    return redirect(f'/flashcard/challenge/{challenge_id}')

def report(request, id):
    challenge = Challenge.objects.get(id=id)

    hits = challenge.flashcards.filter(gotItRight = True).count()
    errors = challenge.flashcards.filter(gotItRight = False).count()

    datas = [hits,errors]

    categories = challenge.category.all()

    name_category = [i.name for i in categories]

    data2 = []

    for category in categories:
        data2.append(challenge.flashcards.filter(flashcard__category = category).filter(gotItRight=True).count())

    print(name_category)
    print(data2)

    return render(request, 'report.html', {'challenge':challenge, 'datas': datas, 'name_category':name_category, 'data2':data2})