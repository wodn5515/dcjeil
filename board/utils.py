from data.models import History, Community

class BoardMixin:
    def get_history(self):
        decade = 1970
        decade_list = []
        data = []
        for i in range(6):
            history_list = History.objects.filter(date__year__gte=decade, date__year__lt=decade+10).order_by('date')
            year_temp = 0
            data_temp = []
            for j in history_list:
                history = {}
                if year_temp != j.date.year:
                    year_temp = j.date.year
                    history['year'] = str(j.date.year)
                else:
                    history['year'] = ' '
                history['date'] = str(j.date.month) + ' / ' + str(j.date.day)
                history['content'] = j.content.replace('\n','<br>')
                data_temp.append(history)
            data.append(data_temp)
            decade_list.append(str(decade)+"~")
            decade += 10
        return decade_list, data
    
    def get_community(self, div):
        community = Community.objects.filter(div=div).last()
        return community
        
    def page_range(self, paginator, page):
        page_numbers_range = 10
        max_index = len(paginator.page_range)+1
        current_page = int(page)
        start_index = int((current_page-1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index
        return paginator.page_range[start_index:end_index]