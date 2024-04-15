from django.shortcuts import render
from .models import Usuarios
# Create your views here.
def mostrarIndex(request):
    return render(request,'index.html')

#R2 mensaje de error 
#R mensaje de que paso correctamente
def mostrarFormActualizar(request, id):
    try:
        pro = Usuarios.objects.get(id = id)
        datos = { 'pro' : pro }
        return render(request, 'form_actualizar.html', datos)
    except:
        pro = Usuarios.objects.all().values()
        datos = { 
            'pro' : pro, 
            'r2' : 'El ID ('+str(id)+') No Existe. Imposible Actualizar!!' 
        }
        return render(request, 'listado.html', datos)



def mostrarFormRegistrar(request):
    return render(request,'form_registrar.html')

def mostrarListado(request):
    pro = Usuarios.objects.all().values()
    datos = { 'pro' : pro }
    return render(request,'listado.html',datos)

def insertarClientes(request):
    if request.method =='POST':
        nom = request.POST['txtnom']
        ema = request.POST['txtemail']
        pas = request.POST['txtpassword']
        crol = request.POST['croles']
        usu = Usuarios(nombre=nom, email=ema, contraseña=pas, rol= crol)
        usu.save()
        datos = { 'r' : 'Registro Realizado Correctamente!!' }
        return render(request, 'form_registrar.html', datos)
    else:
        datos = { 'r2' : 'No Se Puede Procesar Solicitud!!' }
        return render(request, 'form_registrar.html', datos)
    

def actualizarClientes(request, id):
    if request.method == 'POST':
        nom = request.POST['txtnom']
        ema = request.POST['txtemail']
        pas = request.POST['txtpassword']
        crol = request.POST['croles']
        pro =Usuarios.objects.get(id = id)
        pro.nombre = nom
        pro.email = ema
        pro.contraseña = pas
        pro.rol = crol
        pro.save()
        pro = Usuarios.objects.all().values()
        datos = { 
            'pro' : pro,
            'r' : 'Datos Modificados Correctamente!!' 
        }
        return render(request, 'listado.html', datos)
    else:
        datos = { 'r2' : 'No Se Puede Procesar Solicitud!!' }
        return render(request, 'listado.html', datos)

def eliminarUsuario(request, id):
    try:
        pro = Usuarios.objects.get(id = id)
        pro.delete()
        pro = Usuarios.objects.all().values()
        datos = { 
            'pro' : pro,
            'r' : 'Registro Eliminado Correctamente!!' 
        }
        return render(request, 'listado.htlm', datos)
    except:
        pro = Usuarios.objects.all().values()
        datos = { 
            'pro' : pro, 
            'r2' : 'El ID ('+str(id)+') No Existe. Imposible Eliminar!!' 
        }
        return render(request, 'listado.html', datos)