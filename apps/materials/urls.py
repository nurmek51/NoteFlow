from django.urls import path
from .views import (
    subject_list, subject_detail,
    material_list, material_detail,
    vote_material, comment_list, MaterialUploadView, MaterialDeleteView
)

urlpatterns = [
    # ✅ Эндпоинты для предметов (Subjects)
    path('subjects/', subject_list, name='subject-list'),  # Получить все предметы
    path('subjects/<int:pk>/', subject_detail, name='subject-detail'),  # Детали конкретного предмета

    path('material/', material_list, name='material-list'), # Список всех материалов/Добавить новый
    path('material/<int:pk>/', material_detail, name = 'material-detail'), # Детали конкретного материала/Изменить и удалить материал

    path('material/vote/<int:material_id>/', vote_material, name='vote-material'), #Поставить лайк(1)/дизлайк(-1)
    path('material/comment/<int:material_id>/', comment_list, name = 'comment-list'), #Получить все комменты/Написать комм

    path('material/upload/', MaterialUploadView.as_view(), name='material-upload' ), #UPLOAD MATERUIAL and update
    path('material/delete/<int:pk>/', MaterialDeleteView.as_view(), name='vote-material'), #DELETE MATERUIAL
    ]