from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import (
    ListView,
)
from django.views import View
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.core.paginator import (
    EmptyPage,
    PageNotAnInteger,
    Paginator
)
from operator import attrgetter, or_, and_
from functools import reduce
from itertools import chain
from .models import (
    Project,
    Ticket,
    Comment,
    Attachment,
)
from django.http import JsonResponse


# def filter(qs, request):
#     query_fields = request.GET.getlist('query_fields',[])
#     query_arguments = request.GET.getlist('query_arguments',[])
#     queries = request.GET.getlist('query',[])
#     operator = request.GET.get('operator','')
#     order_by = request.GET.getlist('order_by',[])
#     reverse_or_not = request.GET.getlist('reverse_or_not',[])
#
#     key_list = []
#     q_obj_list = []
#     if query_fields:
#         for index, field in enumerate(query_fields):
#             if query_arguments[index] == 'contains':
#                key_list.append(f'{field}__icontains')
#             elif query_arguments[index] == 'exact':
#                 key_list.append(f'{field}__iexact')
#             elif query_arguments[index] == 'gte':
#                 key_list.append(f'{field}__gte')
#             else:
#                 key_list.append(f'{field}__lt')
#
#     for index, key in key_list:
#         q_obj = Q(**{key:queries[index]})
#         q_obj_list.append(q_obj)
#
#     if operator == 'or':
#         qs = qs.filter(reduce(or_, q_obj_list))
#     elif operator == 'and':
#         qs = qs.filter(reduce(and_, q_obj_list))
#     else:
#         qs = qs.filter(q_obj_list[0])
#     queryset = []
#     for project in qs:
#         queryset.append(project)
#         queryset = list(set(queryset))
#
#     for i in range(len(order_by)-1, -1, -1):
#         if reverse_or_not[i] == 'on':
#             queryset = sorted(queryset, key=attrgetter(order_by[i]), reverse=True)
#         else:
#             queryset = sorted(queryset, key=attrgetter(order_by[i]))
#     return queryset
#
#
# class ProjectListView(ListView):
#     model = Project
#     template_name = 'main/projects.html'
#     context_object_name = 'projects'
#     paginate_by = 10
#     paginate_orphans = 3
#
#     def get_queryset(self):
#         qs = super().get_queryset()
#         queryset = filter(qs=qs, request=self.request)
#         return queryset


PROJECT_LIST_PER_PAGE = 2

def get_project_queryset(query=None):
    queryset = []
    queries = query.split(" ")
    for q in queries:
        posts = Project.objects.filter(
            Q(title__icontains=q) | Q(description__icontains=q)).distinct()
        for post in posts:
            queryset.append(post)
        # create unique set and then convert to list
        return list(set(queryset))


def projectListView(request):
    context = {}
    query = ""
    if request.method == 'GET':
        query = request.GET.get('q', '')
        context['query'] = str(query)

    project_list = sorted(get_project_queryset(
        query), key=attrgetter('date_created'), reverse=True)

    # Pagination
    page = request.GET.get('page', 1)
    project_list_paginator = Paginator(project_list, PROJECT_LIST_PER_PAGE)
    try:
        project_list = project_list_paginator.page(page)
    except PageNotAnInteger:
        project_list = project_list_paginator.page(PROJECT_LIST_PER_PAGE)
    except EmptyPage:
        project_list = project_list_paginator.page(
            project_list_paginator.num_pages)

    context['projects'] = project_list

    return render(request, "main/projects.html", context)
#
#
# def projectDetailView(request, id):
#     pass
