from django.shortcuts import render, get_object_or_404, redirect

from .models import Question, Choice
from .forms import ChoiceForm

# Create your views here.
def savollar(request):
    # bu yerda question modelidagi barcha objectlar olinadi
    savollar = Question.objects.all()
    return render(
        request, 'questions/savollar.html', {
            'savollar': savollar,
            "form": ChoiceForm(),
            "choices": Choice.object.all()
            }
        )





def savol_detail(request, id):
    # bu yerda Question modelidan id si parameterda kelayotgan
    # id ga teng bo'lgan object olinadi
    savol = get_object_or_404(Question, id=id)
    return render(request, 'questions/savol.html', {"savol": savol})


def check_answer(request, variant_id):
    # bu yerda Choice modelidan id si parameterda kelayotgan
    # variant_id ga teng bo'lgan object olinadi
    javob = get_object_or_404(Choice, id=variant_id)
    correct = javob.is_correct
    return render(request, 'questions/checked.html', {'correct': correct})


def create_question(request):
    if request.method == "POST":
        question = request.POST.get('question')
        if Question.objects.filter(question=question.strip()).exists():
            return render(
                request,
                'questions/create_question.html',
                {
                    "message": "Bu savol mavjud!",
                    "question": question
                }
            )

        Question.objects.create(question=question.strip())
        return redirect('poll:savollar')
    return render(request, 'questions/create_question.html')


# CRUD - Create Read Update Delete

def c_choice(request, savol_id):
    # savol qaysiligini bilvolamiz
    savol = get_object_or_404(Question, id=savol_id)
    # variant yaratamiz
    if request.method == "POST":
        choice_text = request.POST.get('choice')
        correct = True if request.POST.get('is_correct') else False

        Choice.objects.create(question=savol, choice=choice_text, is_correct=correct)
        return redirect("poll:savol", id=savol.id)
    return render(request, 'questions/create_choice.html', {"savol": savol})


def create_choice(request):
    form = ChoiceForm()
    if request.method == "POST":
        form = ChoiceForm(data=request.POST)
        if form.is_valid():
            choice = form.save()
            return redirect("poll:savollar")
    return render(request, 'questions/create_choice.html', {"form": form})
