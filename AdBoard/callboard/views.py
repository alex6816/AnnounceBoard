from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from callboard.forms import AnnouncementForm, RespondForm
from callboard.models import Announcement, Category, Respond

menu = [{'title': 'Главная', 'url_name': 'ann_list'},
        {'title': 'Добавить объявление', 'url_name': 'ann_create'},
        {'title': 'Мои объявления', 'url_name': 'my_anns'},
        ]


def about_us(request):
    return render(request, 'about.html', {'menu': menu, 'title': 'О сайте'})


class AnnouncementList(ListView):
    model = Announcement
    template_name = 'ann_list.html'
    context_object_name = 'ann'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['cat_selected'] = 0
        context['title'] = 'Главная страница'
        context['cats'] = Category.objects.all()
        return context


class AnnouncementDetail(DetailView):
    model = Announcement
    form_class = RespondForm
    template_name = 'ann_detail.html'
    context_object_name = 'ann_one'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = RespondForm
        context['menu'] = menu
        context['title'] = 'Объявление'
        context['cat_selected'] = 0
        context['cats'] = Category.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        form = RespondForm(request.POST)
        if form.is_valid():
            form.instance.respond_ann_id = self.kwargs.get('pk')
            form.instance.respond_user = self.request.user
            form.save()

            return redirect(request.META.get('HTTP_REFERER'))


class AnnCategoryList(ListView):
    model = Announcement
    template_name = 'ann_list.html'
    context_object_name = 'ann'
    paginate_by = 10

    def get_queryset(self):
        return Announcement.objects.filter(category__id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['cat_selected'] = context['ann'][0].category_id
        context['title'] = 'Категория - ' + str(context['ann'][0].category)
        context['cats'] = Category.objects.all()
        return context


class AnnouncementCreate(LoginRequiredMixin, CreateView):
    model = Announcement
    template_name = 'announcement_create.html'
    form_class = AnnouncementForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(AnnouncementCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['cat_selected'] = 0
        context['title'] = 'Добавить объявление'
        context['cats'] = Category.objects.all()
        return context

    def get_success_url(self):
        return reverse('ann_detail', kwargs={'pk': self.object.id})


class AnnounceUpdate(UpdateView):
    model = Announcement
    template_name = 'ann_update.html'
    context_object_name = 'ann'
    form_class = AnnouncementForm
    extra_context = {'title': 'Редактирование объявления'}

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Announcement.objects.get(pk=id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        return context

    def get_success_url(self):
        return reverse('my_ann_detail', kwargs={'pk': self.object.id})


class AnnounceDelete(DeleteView):
    model = Announcement
    template_name = 'ann_delete.html'
    success_url = reverse_lazy('ann_list')
    extra_context = {'title': 'Удаление объявления'}


class MyAnnouncement(ListView):
    model = Announcement
    template_name = 'my_ann_list.html'
    context_object_name = 'ann'
    paginate_by = 10

    def get_queryset(self):
        return Announcement.objects.filter(author__id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Мои объявления'
        return context


def my_ann_detail(request, pk):
    ann_one = Announcement.objects.get(pk=pk)
    respond = Respond.objects.filter(respond_ann_id=pk)

    response_data = {
        'ann_one': ann_one,
        'respond': respond,
        'title': 'Объявление',
        'menu': menu

    }
    return render(request, 'my_ann_detail.html', response_data)


class RespondStatus(DetailView):
    model = Respond
    template_name = 'respond_status.html'
    context_object_name = 'respond'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Новый отклик'
        return context


def respond_accept(request, pk):
    respond = Respond.objects.get(pk=pk)
    ann_pk = str(respond.respond_ann.pk)
    str_url = '/myanndetail/' + ann_pk
    respond.status = True
    respond.save()

    return HttpResponseRedirect(f'{str_url}')


def respond_remove(request, pk):
    respond = Respond.objects.get(pk=pk)
    ann_pk = str(respond.respond_ann.pk)
    str_url = '/myanndetail/' + ann_pk
    respond.delete()

    return HttpResponseRedirect(f'{str_url}')
