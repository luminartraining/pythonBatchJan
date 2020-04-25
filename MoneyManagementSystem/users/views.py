from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.views.generic import TemplateView
from users.models import Users,Expense
from users.forms import UserCreationForm,UserLoginForm,AddExpenseForm
from django.http import JsonResponse
class CreateUser(TemplateView):
    template_name ="users/userregistration.html"
    model_name=Users
    form_class=UserCreationForm



    def get(self, request, *args, **kwargs):
        form=self.form_class
        context={}
        context["form"]=form
        return render(request,self.template_name,context)

    def post(self, request, *args, **kwargs):

        form=self.form_class(request.POST)
        print("inside post")
        if form.is_valid():
            form.save()
            return JsonResponse({"message": "created", 'status': 200})
            # return redirect("login")

class Login(TemplateView):

    model_name=Users
    template_name = "users/userlogin.html"
    form_class=UserLoginForm

    def get(self, request, *args, **kwargs):
        form = self.form_class
        context = {}
        context["form"] = form
        return render(request, self.template_name, context)

    def post(self,request, *args, **kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            qs=Users.objects.get(username=username)

            if((qs.username==username) & (qs.password==password)):
                request.session['username'] = username
                return JsonResponse({"message": "loginSuccessfull", 'status': 200})
        else:
            return JsonResponse({"message": "login failed", 'status': 204})
class UserHome(TemplateView):

    def get(self, request, *args, **kwargs):
        print(request.session["username"])
        return render(request,"users/userHome.html")

class AddExpense(TemplateView):
    template_name = "users/addexpense.html"
    model_name=Expense
    form_class=AddExpenseForm
    login_required = True



    def get(self, request, *args, **kwargs):
        form=self.form_class
        qs=self.model_name.objects.filter(user=request.session["username"]).order_by('date')
        print("query set",qs)
        context={}
        context["form"]=form
        context["qs"]=qs
        return render(request,self.template_name,context)
    def post(self, request, *args, **kwargs):

        form=self.form_class(request.POST)
        if form.is_valid():

            user=request.session["username"]

            print("userrrr",user)
            category=form.cleaned_data["category"]
            amount=form.cleaned_data["amount"]
            shortnote=form.cleaned_data["shortnote"]
            date=form.cleaned_data["date"]

            obj=self.model_name(user=user,category=category,amount=amount,shortnote=shortnote,date=date)
            obj.save()
            return redirect("addexpense")
        else:
            context = {}
            context["form"] = form
            return render(request, self.template_name, context)

@login_required
class ReviewExpense(TemplateView):
    template_name = "users/reviewexpense.html"
    model_name=Expense

    # def get(self, request, *args, **kwargs):

