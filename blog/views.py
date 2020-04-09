from django.shortcuts import render,redirect
from .models import Post,Quiz,Question,Report
from django.http import HttpResponse,JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
i=0
NextQ=[]
totalq=0
qq=[]
pass_marks=0
marks_per_q=0
score=0
@login_required
def quiz(request):
    quizz=Quiz.objects.all().values()
    contexts=[]
    report=Report.objects.filter(username=request.user.username).values('quiz_name')
    new_report=[]
    for k in report:
        new_report.append(k['quiz_name'])
    for i in quizz:
            tq=i['total_questions']
            sub=i['subject_id']
            name=i['name']
            questions=Question.objects.filter(subject_id=sub).values()
            if name in new_report:
                continue
            l=len(questions)
            if l>=tq:
                contexts.append(i)
    cost={'quiz_data':contexts}        
    return render(request,'blog/home.html',cost)
@login_required
def progress(request):
    data=Report.objects.filter(username=request.user.username).values()
    return render(request,'blog/progress.html',{'data':data})

@login_required
def home(request):
    return render(request,'blog/index.html')

@login_required
def nextQuestion(request):
    global NextQ
    global i
    global totalq
    global qq
    global pass_marks
    global marks_per_q
    global score
    global quizData_name
    global total_marks
    data={}
    total_marks=totalq*marks_per_q
    pass_percentage=pass_marks*100//total_marks
    if request.method=='POST':  
        ans=request.POST['answer_user']
        original_ans=NextQ[i]
        if ans==original_ans['Answer']:
            score=score+marks_per_q
        else:
            score=score 
        i=i+int(request.POST['question_id'])
        qq.append(ans)
        if i==totalq:
            if score>=pass_marks:
                status='PASS'
            else:
                status='FAIL'
            # print(total_marks)
            your_percentage=score*100//total_marks
            REPORT=Report.objects.get(username=request.user.username,quiz_name=quizData_name)
            REPORT.passing_percentage=pass_percentage
            REPORT.score=your_percentage
            REPORT.status=status
            REPORT.save()
            html = render_to_string('blog/result.html',{'data':zip(NextQ,qq),'status':status,'score':your_percentage})
            i=0
            NextQ=[]
            qq=[]
            pass_marks=0
            marks_per_q=0
            score=0
            return HttpResponse(html)
        data=NextQ[i]
        data['next_q']=i+1
        return JsonResponse(data)

@login_required
def start(request):
    global NextQ
    global i
    global totalq
    global quizData_name
    global marks_per_q
    global pass_marks
    if request.method=='POST':
        code=request.POST.get('code')
        quiz_start=request.POST.get('Quizname')
        cheat=Report.objects.filter(username=request.user.username,quiz_name=quiz_start).values()
        wrong=Quiz.objects.filter(code=code,name=quiz_start).values()
        if cheat:
            return redirect('blog-quiz')
        if not wrong:
            return redirect('blog-quiz')   
        quiz=Quiz.objects.filter(code=code).values()
        quizData=quiz[0]
        s_id=quizData['subject_id']
        totalq=quizData['total_questions']
        marks_per_q=quizData['marks_per_question']
        pass_marks=quizData['passing_marks']
        quizData_name=quizData['name']
        Report.objects.create(username=request.user.username,quiz_name=quizData_name,score=0)
        questions=Question.objects.filter(subject_id=s_id).values()
        for j in range(0,totalq):
            NextQ.append(questions[j])
        i=0
        return render(request,'blog/start.html',{'ques':NextQ[0],'tq':totalq,'question_id':(i+1)})
    else:
        return redirect('blog-quiz')