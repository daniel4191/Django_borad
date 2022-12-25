# comment serises

from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from ..models import Question, Answer, Comment
from ..forms import CommentForm


# code line

@login_required(login_url='common:login')
def comment_create_question(request, question_id):
    """

    Add pybo comment
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.question = question
            comment.save()
            # return redirect('pybo:detail', question_id=question.id)
            return redirect('{}#comment_{}'.format(
                resolve_url('pybo:detail',
                            question_id=comment.question.id), comment.id
            ))

    else:
        form = CommentForm()
    context = {'form': form}
    return render(request, 'pybo/comment_form.html', context)


@login_required(login_url='common:login')
def comment_modify_question(request, comment_id):
    """

    Edit pybo comment
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, "you don't have permission to Edit comment")
        return redirect('pybo:detail', question_id=comment.question.id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.modify_date = timezone.now()
            comment.save()
            # return redirect('pybo:detail', question_id=comment.question.id)
            return redirect('{}#comment_{}'.format(
                resolve_url('pybo:detail',
                            question_id=comment.question.id), comment.id
            ))

        else:
            form = CommentForm(instance=comment)
        context = {'form': form}
        return render(request, 'pybo/comment_form.html', context)


@login_required(login_url='common:login')
def comment_delete_question(request, comment_id):
    """

    Delete pybo comment
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, "you don't have permission to delete")
        return redirect('pybo:detail', question_id=comment.question.id)

    else:
        comment.delete()
    return redirect('pybo:detail', question_id=comment.question.id)


@login_required(login_url='common:login')
def comment_create_answer(request, answer_id):
    """

    Submit pybo answer's comment
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.answer = answer
            comment.save()
            # return redirect('pybo:detail', question_id=comment.answer.question.id)
            return redirect('{}#comment_{}'.format(
                resolve_url('pybo:detail',
                            question_id=answer.question.id), comment.id
            ))

    else:
        form = CommentForm()
    context = {'form': form}
    return render(request, 'pybo/comment_form.html', context)


@login_required(login_url='common:login')
def comment_modify_answer(request, comment_id):
    """

    Edit pybo answer comment
    """

    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(
            request, "you don't have permission to modify this comment")
        return redirect('pybo:detail', question_id=comment.answer.question.id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.modify_date = timezone.now()
            comment.save()
            # return redirect('pybo:detail', question_id=comment.answer.question.id)
            return redirect('{}#comment_{}'.format(
                resolve_url('pybo:detail',
                            question_id=comment.question.id), comment.id
            ))

    else:
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'pybo/comment_form.html', context)


@login_required(login_url='common:login')
def comment_delete_answer(request, comment_id):
    """

    Delete pybo answer comment
    """

    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(
            request, "you don't have permission to modify this comment")
        return redirect('pybo:detail', question_id=comment.answer.question.id)

    else:
        comment.delete()
    return render('pybo:detail', question_id=comment.answer.question.id)
