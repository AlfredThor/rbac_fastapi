import math


class Page:
    def iPagination(self, data):
        total = int(data['total'])
        page_size = int(data['page_size'])
        current = int(data['current'])
        total_pages = int(math.ceil(total / page_size))
        total_pages = total_pages if total_pages > 0 else 1

        ret = {
            "start": page_size * (current - 1) if current > 1 else 0,
            "current": current,  # 当前页
            "total_pages": total_pages,  # 总页数
            "page_size": page_size,  # 每页多少数据
            "total": total  # 总数据数
        }
        return ret


pages = Page()
