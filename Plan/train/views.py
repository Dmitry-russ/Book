from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse

import tablib

from .forms import CasesForm, NewTrainForm, NewMaiForm, NewMaiFormFromList
from .models import Cases, Train, DoneMaiDate, Maintenance
from .utils import page_control, result_mai_list

PAGE_LIST = 40


@login_required
def train_list(request):
    """Вывод списка поездов."""

    trains = Train.objects.all()
    page_obj = page_control(request, trains, PAGE_LIST)

    main_delete = DoneMaiDate.objects.filter(musthave=False)

    context = {'page_obj': page_obj,
               'main_delete': main_delete,
               'admin': request.user.is_staff, }
    return render(request, 'trains/train_list.html', context)


@login_required
def train_create(request):
    """Создание поезда."""

    form = NewTrainForm(request.POST or None, files=request.FILES or None)
    if not form.is_valid():
        return render(request, 'trains/train_create.html', {'form': form})
    train = form.save(commit=False)
    train.author = request.user
    train.save()
    return redirect('train:train_list')


@login_required
def train_detail(request, train_id):
    """Изменение поезда."""

    train = get_object_or_404(Train, id=train_id)
    form = NewTrainForm(
        request.POST or None,
        files=request.FILES or None,
        instance=train)
    if form.is_valid():
        train.save()
        form = NewTrainForm(
            request.POST or None,
            files=request.FILES or None,
            instance=train)
        return redirect('train:train_list')

    context = {'form': form,
               'train': train,
               'is_edit': True, }
    return render(request, 'trains/train_create.html', context)


@login_required
def cases_list(request, train_id):
    """Вывод списка замечаний на поезде."""

    train = get_object_or_404(Train, id=train_id)
    cases = Cases.objects.filter(train=train)
    page_obj = page_control(request, cases, PAGE_LIST)
    context = {
        'page_obj': page_obj,
        'train': train,
    }
    return render(request, 'trains/cases_list.html', context)


@login_required
def case_detail(request, case_id):
    """Редактирование замечания."""

    case = get_object_or_404(Cases, id=case_id)
    form = CasesForm(
        request.POST or None,
        files=request.FILES or None,
        instance=case)
    if form.is_valid():
        case.save()
        form = CasesForm(
            request.POST or None,
            files=request.FILES or None,
            instance=case)

    context = {'form': form,
               'case': case, }
    return render(request, 'trains/case_detail.html', context)


@login_required
def case_create(request, train_id):
    """Создание замечания."""

    form = CasesForm(request.POST or None, files=request.FILES or None)
    train = get_object_or_404(Train, id=train_id)
    context = {'form': form,
               'train': train}
    if not form.is_valid():
        return render(request, 'trains/case_create.html', context)
    case = form.save(commit=False)
    case.author = request.user
    case.train = train
    case.save()
    return redirect('train:cases_list', train.id)


@login_required
def case_delete(request, case_id, train_id):
    """Удаление замечания."""

    case = Cases.objects.filter(id=case_id)
    case.delete() if case.exists() else None
    return redirect('train:cases_list', train_id)


@login_required
def mai_list(request, train_id):
    """Вывод списка проведенных и ближайших инспекций."""

    train = get_object_or_404(Train, id=train_id)
    donemai = list(DoneMaiDate.objects.filter(train=train))
    main = list(Maintenance.objects.filter(order=True))
    main_another = list(Maintenance.objects.filter(order=False))
    result = result_mai_list(main, donemai)
    context = {
        'result': result,
        'train': train,
        'main_another': main_another,
        'admin': request.user.is_staff,
    }
    return render(request, 'trains/mai_list.html', context)


@login_required
def mai_delete(request, mai_id):
    """Удаление проведенной инспекции."""

    mai = get_object_or_404(DoneMaiDate, id=mai_id)
    if request.user.is_staff:
        train = mai.train
        mai.delete()
        return redirect('train:mai_list', train.id)

    train = mai.train
    if mai.musthave is False:
        mai.musthave = True
        mai.save()
        return redirect('train:mai_detail', mai.id)
    mai.musthave = False
    mai.save()
    return redirect('train:mai_detail', mai.id)


@login_required
def mai_not_delete(request, mai_id):
    """Отмена удаления админом."""

    mai = get_object_or_404(DoneMaiDate, id=mai_id)
    if request.user.is_staff:
        mai.musthave = True
        mai.save()
        return redirect('train:mai_detail', mai.id)


@login_required
def mai_create(request, train_id):
    """Создание проведенной инспекции (произвольной)."""

    form = NewMaiForm(
        request.POST or None,
        files=request.FILES or None, )
    train = get_object_or_404(Train, id=train_id)
    context = {'form': form,
               'train': train, }
    if not form.is_valid():
        return render(request, 'trains/mai_create.html', context)
    mai = form.save(commit=False)
    mai.author = request.user
    mai.train = train
    mai.save()
    return redirect('train:mai_list', train_id)


@login_required
def mai_create_from_list(request, train_id, mai_id):
    """Создание проведенной инспекции из списка инспекций."""

    mai_type = get_object_or_404(Maintenance, id=mai_id)
    form = NewMaiFormFromList(

        request.POST or None,
        files=request.FILES or None,
    )
    train = get_object_or_404(Train, id=train_id)
    context = {'form': form,
               'train': train,
               'create': True,
               'mai_type': mai_type, }
    if not form.is_valid():
        return render(request, 'trains/mai_create.html', context)
    mai_done = form.save(commit=False)
    mai_done.author = request.user
    mai_done.train = train
    mai_done.maintenance = mai_type
    mai_done.save()
    return redirect('train:mai_list', train_id)


@login_required
def mai_detail(request, mai_id):
    """Редактирование проведенной инспекции."""

    mai_done = get_object_or_404(DoneMaiDate, id=mai_id)
    train = get_object_or_404(Train, id=mai_done.train.id)
    form = NewMaiFormFromList(
        request.POST or None,
        files=request.FILES or None,
        instance=mai_done, )
    if form.is_valid():
        mai_done.author = request.user
        mai_done.save()
        form = NewMaiFormFromList(
            request.POST or None,
            files=request.FILES or None,
            instance=mai_done)
        return redirect('train:mai_list', train.id)
    context = {'form': form,
               'train': train,
               'is_edit': True,
               'mai_done': mai_done,
               'mai_type': mai_done.maintenance,
               'admin': request.user.is_staff, }
    return render(request, 'trains/mai_create.html', context)


@login_required
def mai_export(request, train_id=None):
    if train_id is not None:
        maintenance = DoneMaiDate.objects.filter(train__id=train_id)
    else:
        maintenance = DoneMaiDate.objects.all().order_by('train')
    headers = ('Поезд',
               'Вид ТО',
               'Дата',
               'Пробег',
               'Место',
               'Комментарий',)
    data = []
    data = tablib.Dataset(*data, headers=headers)
    for mai in maintenance:
        data.append([f'{mai.train.serial.serial}-{mai.train.number}',
                     mai.maintenance.type,
                     mai.maintenance_date,
                     mai.mileage,
                     mai.place,
                     mai.comment, ])
    response = HttpResponse(
        data.export('xls'),
        content_type='application/vnd.ms-excel;charset=utf-8')
    if train_id:
        text = (f'attachment; '
                f'filename={mai.train.serial.slug}-{mai.train.number}.xls')
    else:
        text = "attachment; filename=All.xls"
    response['Content-Disposition'] = text
    return response
