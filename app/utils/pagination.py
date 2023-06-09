from flask import request
from flask_sqlalchemy.pagination import QueryPagination


def get_pagination(collection: QueryPagination) -> dict:
    base_url = request.base_url
    pagination_data = {
        "prev_url": base_url + f"?page={collection.prev_num}" if collection.has_prev else None,
        "current_url": base_url + f"?page={collection.page}",
        "next_url": base_url + f"?page={collection.next_num}" if collection.has_next else None,
        "per_page": collection.per_page,
        "total_pages": collection.pages,
        "total_items": collection.total,
    }
    return pagination_data
