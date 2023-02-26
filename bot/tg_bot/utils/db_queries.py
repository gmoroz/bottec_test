from bot.models import Category
from asgiref.sync import sync_to_async
from django.db.models.query import QuerySet


async def paginate_qs(page: int, page_size: int, qs: QuerySet) -> QuerySet:
    """Разбивает кверисет на страницы."""
    offset = (page - 1) * page_size
    limit = page_size
    return qs[offset : offset + limit]


async def get_categories() -> QuerySet:
    """Получает список категорий из базы данных."""
    return await sync_to_async(Category.objects.order_by)("id")
