from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Exists, OuterRef, Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ReviewForm
from .models import SCORE_LABELS, Review, Teacher


def _reviews(user):
    return Review.objects.select_related("author__team").annotate(
        likes=Count("liked_users", distinct=True),
        dislikes=Count("disliked_users", distinct=True),
        liked_by_me=Exists(Review.liked_users.through.objects.filter(review_id=OuterRef("pk"), user_id=user.pk)),
        disliked_by_me=Exists(Review.disliked_users.through.objects.filter(review_id=OuterRef("pk"), user_id=user.pk)),
    )


def _hx_refresh():
    # после действий, меняющих статистику в сайдбаре, перезагружаем страницу целиком
    response = HttpResponse()
    response["HX-Refresh"] = "true"
    return response


def teacher_list(request):
    q = request.GET.get("q", "").strip()
    teachers = Teacher.objects.with_ratings().prefetch_related("subjects")
    if q:
        teachers = teachers.filter(Q(surname__icontains=q) | Q(name__icontains=q) | Q(patronymic__icontains=q))

    # Живой поиск: HTMX перерисовывает только список
    if request.headers.get("HX-Request"):
        return render(request, "teachers/_teacher_list.html", {"teachers": teachers, "q": q})

    rated = [t for t in Teacher.objects.with_ratings().prefetch_related("subjects") if t.overall_rating()]
    top = sorted(rated, key=lambda t: (t.overall_rating(), t.reviews_count), reverse=True)[:3]
    return render(request, "teachers/teacher_list.html", {"teachers": teachers, "q": q, "top": top})


def teacher_detail(request, pk):
    teacher = get_object_or_404(Teacher.objects.with_ratings().prefetch_related("subjects"), pk=pk)
    user_review = teacher.reviews.filter(author=request.user).first()

    form = ReviewForm(request.POST or None, instance=user_review)
    if request.method == "POST" and form.is_valid():
        review = form.save(commit=False)
        review.teacher = teacher
        review.author = request.user
        review.save()
        messages.success(request, "Отзыв сохранён")
        return redirect("teacher_detail", pk=pk)

    # лента: все отзывы; чужие без текста по умолчанию свёрнуты (Alpine showAll)
    reviews = (
        _reviews(request.user)
        .filter(teacher=teacher)
        .order_by("-created")  # annotate с GROUP BY отбрасывает Meta.ordering
    )
    hidden_count = sum(1 for r in reviews if not r.text and r.author_id != request.user.pk)
    scales = [
        (SCORE_LABELS["score_knowledge"], teacher.avg_knowledge),
        (SCORE_LABELS["score_skill"], teacher.avg_skill),
        (SCORE_LABELS["score_communication"], teacher.avg_communication),
        (SCORE_LABELS["score_freeloading"], teacher.avg_freeloading),
    ]
    return render(request, "teachers/teacher_detail.html", {
        "teacher": teacher,
        "reviews": reviews,
        "user_review": user_review,
        "scales": scales,
        "hidden_count": hidden_count,
        "form": form,
    })


def review_card(request, pk):
    review = get_object_or_404(_reviews(request.user), pk=pk)
    return render(request, "teachers/_review.html", {"r": review})


def review_edit(request, pk):
    review = get_object_or_404(_reviews(request.user), pk=pk)
    if review.author_id != request.user.pk and not request.user.has_perm("teachers.change_review"):
        raise PermissionDenied
    form = ReviewForm(request.POST or None, instance=review)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Отзыв сохранён")
        return _hx_refresh()
    return render(request, "teachers/_review_form.html", {"form": form, "r": review})


@require_POST
def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if review.author_id != request.user.pk and not request.user.has_perm("teachers.delete_review"):
        raise PermissionDenied
    review.delete()
    messages.success(request, "Отзыв удалён")
    return _hx_refresh()


@require_POST
def review_vote(request, pk, vote):
    review = get_object_or_404(Review, pk=pk)
    mine, other = (review.liked_users, review.disliked_users) if vote == "like" else (review.disliked_users, review.liked_users)
    if mine.filter(pk=request.user.pk).exists():
        mine.remove(request.user)
    else:
        mine.add(request.user)
        other.remove(request.user)
    return review_card(request, pk)
