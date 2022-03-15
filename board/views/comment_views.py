from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from board.models import Question, Answer
from board.forms import QuestionForm, AnswerForm, CommentForm

@login_required(login_url='common:login_view')
def comment_create_question(request, question_id):
    # 질문 댓글 등록
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)       # 가저장
            comment.create_date = timezone.now()    # 댓글 작성일
            comment.author = request.user           # 댓글 글쓴이
            comment.question = question             # 댓글이 달린 질문
            comment.save()                          # db에 저장
            return redirect('board:detail', question_id=question.id)
    else:
        form = CommentForm()
    context = {'form':form}
    return render(request, 'board/comment_form.html', context)