# DenunciasApp
App denuncias 


## App Denuncias

### Estructura del proyecto 
La estructura del proyecto esta organizado de acuerdo a Blueprint
- App (Carpeta del proyecto)
    - User (Modulo)
      - views.py (Controlador modulo)
      - models.py (Modelo Base de datos)
      - forms.py (Formulario vistas flaskwtf)
      - decorators.py (metodos) 
    - Complaint (Modulo)
      - views.py (Controlador modulo)
      - models.py (Modelo Base de datos)
      - forms.py (Formulario vistas flaskwtf)
    - utilities (funciones)
      - storage.py (Metodo de cliente almacenamiento google cloud storage)
    - Static (Carpeta estaticos)
      - css/style.css (Estilos)
      - img (carpeta imagenes)
    - Templates (Vistas)
      - /complaint (Vistas modulo complaint)
      - /user (Vistas modulo user)
      - base.html (Estructura Views)
      - googleapi.html (script googleapi)     
    - env (carpeta de entorno virtual con virtual env)
    - app.py (Inicializador de cada modulo)
    - config.py (archivo configuracion del proyecto)
    - run.py (iniciar servidor) 

 
 
 ## Iniciar proyecto

### Activar entorno virtual
 `source env/bin/activate`

### Iniciar servidor
`python run.py`

## Preview Proyecto
![home](https://user-images.githubusercontent.com/8931588/83959536-8d974e00-a843-11ea-9944-b7ebe9ef169f.png)
  
  
