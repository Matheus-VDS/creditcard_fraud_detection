from django.shortcuts import render,redirect,get_object_or_404
from django.http.response import HttpResponseRedirect,HttpResponse
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import DataFileUpload
from django.core.paginator import Paginator
import csv
import os
import pandas as pd
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage

def base(request):
    return render(request,'homeApp/landing_page.html')
    
def upload_credit_data(request):
    return render(request,'homeApp/upload_credit_data.html')
def prediction_button(request):
    return render(request,'homeApp/fraud_detection.html')
    
def reports(request):
    all_data_files_objs=DataFileUpload.objects.all()
    return render(request,'homeApp/reports.html',{'all_files':all_data_files_objs})
    
def enter_form_data_manually(request):
    return render(request,'homeApp/enter_form_data_manually.html')
def predict_data_manually(request):
    return render(request,'homeApp/predict_data_manually.html')

def add_files_single(request):
    return render(request,'homeApp/add_files_single.html')
def predict_csv_single(request):
    return render(request,'homeApp/predict_csv_single.html')

def add_files_multi(request):
    return render(request,'homeApp/add_files_multi.html')
    
def predict_csv_multi(request):
    return render(request,'homeApp/predict_csv_multi.html')

def account_details(request):
    return render(request,'homeApp/account_details.html')
def change_password(request):
    return render(request,'homeApp/change_password.html')
def analysis(request, file_name):
    file_path = os.path.join(settings.MEDIA_ROOT, 'uploads', file_name + '.csv')
    df = pd.read_csv(file_path)
    size = df.shape
    existe_valor_nulo = df.isnull().any().any()
    total_classe_0 = df[df['Class'] == 0]['Class'].count()
    total_classe_1 = df[df['Class'] == 1]['Class'].count()
    context = {
        'size1': size[0],
        'size2': size[1],
        'existe_valor_nulo': existe_valor_nulo,
        'total_classe_0': total_classe_0,
        'total_classe_1': total_classe_1, 
    }
    return render(request, 'homeApp/analysis.html', context)
#    return render(request,'homeApp/analysis.html')
def view_data(request):
    return render(request,'homeApp/view_data.html')
#def delete_data(request,id):
 #   obj=DataFileUpload.objects.get(id=id)
 #   obj.delete()
 #   messages.success(request, "Arquivo Deletado com successo",extra_tags = 'alert alert-success alert-dismissible show')
 #   return HttpResponseRedirect('/reports')
def delete_data(request, id):
    try:
        obj = DataFileUpload.objects.get(id=id)
        file_path = obj.actual_file.path  # Obtém o caminho completo do arquivo
        obj.delete()  # Exclui o objeto do banco de dados
        os.remove(file_path)  # Exclui o arquivo físico da pasta "uploads"
        messages.success(request, "Arquivo Deletado com sucesso", extra_tags='alert alert-success alert-dismissible show')
    except DataFileUpload.DoesNotExist:
        messages.warning(request, "Arquivo não encontrado.", extra_tags='alert alert-warning alert-dismissible show')
    except Exception as e:
        messages.error(request, "Ocorreu um erro ao excluir o arquivo.", extra_tags='alert alert-danger alert-dismissible show')
    
    return redirect('/reports')    
def validate_csv(value):
    ext = os.path.splitext(value.name)[1]  # Obtém a extensão do arquivo enviado
    valid_extensions = ['.csv']  # Lista de extensões válidas (neste caso, apenas .csv)

    if not ext.lower() in valid_extensions:
        raise ValidationError('Tipo de arquivo não suportado. Por favor, envie um arquivo CSV.')
        

def upload_data(request):
    if request.method == 'POST':
        actual_file = request.FILES.get('actual_file_name')

        if actual_file is None:
            messages.warning(request, "Formato Inválido/Errado. Faça o upload do Arquivo.")
            return redirect('/upload_credit_data')

        try:
            validate_csv(actual_file)
        except ValidationError as e:
            messages.warning(request, str(e))
            return redirect('/upload_credit_data')

        description = request.POST.get('description')

        data_file_name, _ = os.path.splitext(request.FILES.get('actual_file_name').name)

        # Verifique se o nome do arquivo já existe no banco de dados
        if DataFileUpload.objects.filter(file_name=data_file_name).exists():
            messages.warning(request, "Nome de arquivo já existe. Por favor, escolha outro nome.")
            return redirect('/upload_credit_data')

        DataFileUpload.objects.create(
            file_name=data_file_name,
            actual_file=actual_file,
            description=description,
        )
        messages.success(request, "Upload do Arquivo realizado com sucesso", extra_tags='alert alert-success alert-dismissible show')
        return redirect('/reports')

    return redirect('/reports')
    # return HttpResponseRedirect('reports')
    

def userLogout(request):
    try:
      del request.session['username']
    except:
      pass
    logout(request)
    return HttpResponseRedirect('/') 
    

def login2(request):
    data = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        print(user)
        if user:
            login(request, user)
            return HttpResponseRedirect('/')
        
        else:    
            data['error'] = "Nome de Usuário ou Senha está incorreto"
            res = render(request, 'homeApp/login.html', data)
            return res
    else:
        return render(request, 'homeApp/login.html', data)

#about
def about(request):
    #return render(request,'homeApp/about.html')
    return render(request,'homeApp/about.html')
def detection(request):
    #return render(request,'homeApp/about.html')
    return render(request,'homeApp/fraud_detection.html')

def dashboard(request):
    return render(request,'homeApp/dashboard.html')
#Função vazia sem uso {view_table}    
def view_table(request):
    files = YourFileModel.objects.all()  # Replace YourFileModel with your actual model
    return render(request, 'homeApp/view_data.html', {'files': files})
    
def view_data_detail(request, file_name):
    
    file_path = os.path.join(settings.MEDIA_ROOT, 'uploads', file_name + '.csv')
    df = pd.read_csv(file_path)
    df_records = df.to_dict('records')

    paginator = Paginator(df_records, 10)  # Show 10 records per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }

    return render(request, 'homeApp/view_data.html', context)
    
def size_data(request, file_name):
    
    file_path = os.path.join(settings.MEDIA_ROOT, 'uploads', file_name + '.csv')
    df = pd.read_csv(file_path)
    size = df.shape
    context = {
        'size1': size[0],
        'size2': size[1]
    }
#    return render(request, 'homeApp/analysis.html', context)
    return render(request, 'homeApp/analysis.html', context)
