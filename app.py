from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

class Tarea:
    def __init__(self, descripcion):
        self.descripcion = descripcion
        self.completada = False

    def marcar_completada(self):
        self.completada = True

    def __str__(self):
        estado = "Completada" if self.completada else "Pendiente"
        return f"{self.descripcion} - {estado}"

class ListaTareas:
    def __init__(self):
        self.tareas = []

    def agregar_tarea(self, descripcion):
        nueva_tarea = Tarea(descripcion)
        self.tareas.append(nueva_tarea)

    def marcar_tarea_completada(self, posicion):
        try:
            self.tareas[posicion].marcar_completada()
        except IndexError:
            pass

    def eliminar_tarea(self, posicion):
        try:
            self.tareas.pop(posicion)
        except IndexError:
            pass

lista_tareas = ListaTareas()

@app.route('/')
def index():
    return render_template('index.html', tareas=lista_tareas.tareas)

@app.route('/add', methods=['POST'])
def add_tarea():
    descripcion = request.form['descripcion']
    lista_tareas.agregar_tarea(descripcion)
    return redirect(url_for('index'))

@app.route('/complete', methods=['POST'])
def complete_tarea():
    try:
        posicion = int(request.form['posicion']) - 1
        lista_tareas.marcar_tarea_completada(posicion)
    except ValueError:
        pass
    return redirect(url_for('index'))

@app.route('/delete', methods=['POST'])
def delete_tarea():
    try:
        posicion = int(request.form['posicion_delete']) - 1
        lista_tareas.eliminar_tarea(posicion)
    except ValueError:
        pass
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
