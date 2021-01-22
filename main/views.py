from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views.generic import (
    View,
    TemplateView
)
from django.contrib.auth import get_user_model
from django.db.models import Q, Count
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


@method_decorator(login_required, name="dispatch")
class ProjectListView(TemplateView):
    template_name = 'main/projects.html'

    def get(self, request):
        num_ticketS = Count('tickets')
        liked_or_not = Count('liked',
                             filter=Q(liked__id__exact=request.user.id)
                             )
        qs = (Project.objects
              .annotate(num_tickets=num_ticketS)
              .annotate(liked_or_not=liked_or_not)
              )
        qs_json = list(qs.values())
        if request.is_ajax():
            return JsonResponse({data: qs_json}, safe=False)
        return render(request, 'main/projects.html', {'projects': qs})


@ login_required
def projectLikeUnlike(request):
    user = request.user
    if request.method == 'POST':
        project_id = request.POST.get('project_id')
        project = Project.objects.get(id=project_id)
        if user in project.liked.all():
            project.liked.remove(user)
        else:
            project.liked.add(user)
        return JsonResponse({"data": "success"}, safe=False)


class ProjectDetailTicketListView(View):
    def get(self, request):
        context = {}
        return render(request, 'main/project-detail.html', context)


class ProjectMemberManage(View):
    def get(self, request):
        pass

        # PROJECT_LIST_PER_PAGE = 2
        # def get_project_queryset(query=None):
        #     queryset = []
        #     queries = query.split(" ")
        #     for q in queries:
        #         posts = Project.objects.filter(
        #             Q(title__icontains=q) | Q(description__icontains=q)).distinct()
        #         for post in posts:
        #             queryset.append(post)
        #         # create unique set and then convert to list
        #         return list(set(queryset))

        # def projectListView(request):
        #     context = {}
        #     query = ""
        #     if request.method == 'GET':
        #         query = request.GET.get('q', '')
        #         context['query'] = str(query)

        #     project_list = sorted(get_project_queryset(
        #         query), key=attrgetter('date_created'), reverse=True)

        #     # Pagination
        #     page = request.GET.get('page', 1)
        #     project_list_paginator = Paginator(project_list, PROJECT_LIST_PER_PAGE)
        #     try:
        #         project_list = project_list_paginator.page(page)
        #     except PageNotAnInteger:
        #         project_list = project_list_paginator.page(PROJECT_LIST_PER_PAGE)
        #     except EmptyPage:
        #         project_list = project_list_paginator.page(
        #             project_list_paginator.num_pages)

        #     context['projects'] = project_list

        #     return render(request, "main/projects.html", context)
        #
        #
        # def projectDetailView(request, id):
        #     pass
