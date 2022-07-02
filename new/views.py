from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import New, Like, Dislike
from .forms import NewForm, NewFormMine, CommentForm


class News(ListView):
    queryset = New.objects.all().order_by('-created')
    template_name = 'new/news_list.html'
    paginate_by: int = 6

    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)


news_list = News.as_view()


def news_detail(request, id):
    new = get_object_or_404(New, id=id)
    # bitta newni olayapmiz New degan modelning barcha objectlari ichidan
    # shu narsa OBJECT deyiladi.
    # model metodlari faqat object uchun ishlaydi 

    form = CommentForm()

    if request.method == "POST":
        # comment formaga postda kelayotgan malumotlarni 
        # berib validatsiyadan o'tkazamiz
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = new
            if request.user.is_authenticated:
                comment.author = request.user
            comment.save()
            return redirect("new:detail", id=id)

    return render(request, 'new/news_detail.html', {'new': new, "form": form})


class NewCreate(CreateView):
    model = New
    form_class = NewForm

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["hello"] = "Hello World"
        # context
        return context


create = NewCreate.as_view()


class RemoveView(DeleteView):
    model = New
    success_url: str = "/news/my-news/"

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


remove = RemoveView.as_view()


class MyNews(LoginRequiredMixin, ListView):
    model = New
    template_name: str = "new/my_news.html"

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user).order_by('-created')


my_news = MyNews.as_view()


def my_create(request):
    form = NewFormMine()
    if request.method == 'POST':
        form = NewFormMine(request.POST, request.FILES)
        if form.is_valid():
            new = form.save(commit=False)
            new.author = request.user
            new.save()
            return redirect("new:my_news")

    return render(request, 'new/create.html', {"form": form})


def my_update(request, id):
    new = get_object_or_404(New, id=id)
    form = NewFormMine(instance=new)
    if request.method == 'POST':
        form = NewFormMine(request.POST, request.FILES, instance=new)
        if form.is_valid():
            form.save()
            return redirect("new:my_news")

    return render(request, 'new/create.html', {"form": form})

def my_detail(request, id):
    new = get_object_or_404(New, id=id)
    return render(request, 'new/my_detail.html', {'new': new})


def like(request, id):
    new = get_object_or_404(New, id=id)
  
    if request.user.is_authenticated:
        if new.dislikes.filter(user=request.user).exists():
            new.dislikes.get(user=request.user).delete()

        if new.likes.filter(user=request.user).exists():
            new.likes.get(user=request.user).delete()
            return JsonResponse({
                "success": True,
                "message": "Siz reaksiyangizni qaytarib oldingiz!",
                "likes": new.like_count(),
                "dislikes": new.dislike_count()
                }
            )

        Like.objects.create(user=request.user, post=new)
        return JsonResponse({
                "success": True,
                "message": "Sizga yoqgan postlar safiga qo'shildi!",
                "likes": new.like_count(),
                "dislikes": new.dislike_count()
                }
            )

    return JsonResponse({
            "success": False,
            "message": "Postga reaksiya bildirish uchun iltimos ro'yhatdan o'ting!",
            }
        )

# request -> so'rov -> zapros
def dislike(request, id):
    new = get_object_or_404(New, id=id)
    if request.user.is_authenticated:
        if new.likes.filter(user=request.user).exists():
            new.likes.get(user=request.user).delete()

        if new.dislikes.filter(user=request.user).exists():
            new.dislikes.get(user=request.user).delete()
            return JsonResponse({
                "success": True,
                "message": "Siz reaksiyangizni qaytarib oldingiz!",
                "likes": new.like_count(),
                "dislikes": new.dislike_count()
                }
            )

        Dislike.objects.create(user=request.user, post=new)
        return JsonResponse({
                "success": True,
                "message": "Sizga yoqmagan postlar safiga qo'shildi!",
                "likes": new.like_count(),
                "dislikes": new.dislike_count()
                }
            )

    return JsonResponse({
            "success": False,
            "message": "Postga reaksiya bildirish uchun iltimos ro'yhatdan o'ting!",
            }
        )
