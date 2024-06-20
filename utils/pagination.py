import math

def make_range_pagination(current_page, qty_pages, page_range):
    middle_range = math.ceil(qty_pages / 2)
    start_range = current_page - middle_range
    end_range = current_page + middle_range
    total_pages = len(page_range)

    start_range_offset = abs(start_range) if start_range < 0 else 0

    if start_range < 0:
        start_range = 0
        end_range += start_range_offset

    if end_range >= total_pages:
        start_range = start_range - abs(end_range - total_pages) 

    pagination = page_range[start_range:end_range]
    return {
        'pagination': pagination,
        'qty_pages': qty_pages,
        'current_page': current_page,
        'total_pages': total_pages,
        'start_range': start_range,
        'end_range': end_range,
        'first_page_out_of_range': current_page > middle_range,
        'last_page_out_of_range': end_range < total_pages,
    }