from django.urls import path
from .views import (
    subject_list, subject_detail,
    material_list, material_detail,
    vote_material, comment_list
)

urlpatterns = [
    # ✅ Эндпоинты для предметов (Subjects)
    path('subjects/', subject_list, name='subject-list'),  # Получить все предметы
    path('subjects/<int:pk>/', subject_detail, name='subject-detail'),  # Детали конкретного предмета

    path('materials/', material_list, name='material-list'), # Список всех материалов/Добавить новый
    path('materials/<int:pk>/', material_detail, name = 'material-detail'), # Детали конкретного материала/Изменить и удалить материал

    path('material/vote/<int:material_id>/', vote_material, name='vote-material'), #Поставить лайк(1)/дизлайк(-1)
    path('material/comment/<int:material_id>/>', comment_list, name = 'comment-list') #Получить все комменты/Написать комм
    ]