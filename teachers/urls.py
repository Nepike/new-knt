from django.urls import path

from . import views

urlpatterns = [
    path("teachers/", views.teacher_list, name="teacher_list"),
    path("teachers/<int:pk>/", views.teacher_detail, name="teacher_detail"),
    path("teachers/reviews/<int:pk>/", views.review_card, name="review_card"),
    path("teachers/reviews/<int:pk>/edit/", views.review_edit, name="review_edit"),
    path("teachers/reviews/<int:pk>/delete/", views.review_delete, name="review_delete"),
    path("teachers/reviews/<int:pk>/like/", views.review_vote, {"vote": "like"}, name="review_like"),
    path("teachers/reviews/<int:pk>/dislike/", views.review_vote, {"vote": "dislike"}, name="review_dislike"),
]
