from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

tarefas = []

def ordenar_tarefas(tarefa):
    prioridades = {'Baixa': 0, 'Média': 1, 'Alta': 2}
    return (-prioridades[tarefa['prioridade']], tarefa['data_vencimento'])

@app.route('/')
def index():
    tarefas_ordenadas = sorted(tarefas, key=ordenar_tarefas)
    return render_template('index.html', tarefas=tarefas_ordenadas)

@app.route('/cadastrar_tarefa', methods=['POST'])
def cadastrar_tarefa():
    descricao = request.form.get('descricao')
    data_vencimento = request.form.get('data_vencimento')
    prioridade = request.form.get('prioridade')
    concluida = False

    tarefa = {'descricao': descricao, 'data_vencimento': data_vencimento, 'prioridade': prioridade, 'concluida': concluida}
    tarefas.append(tarefa)

    tarefas[:] = sorted(tarefas, key=ordenar_tarefas)
    return redirect(url_for('index'))

@app.route('/editar_tarefa/<int:task_id>', methods=['GET', 'POST'])
def editar_tarefa(task_id):
    if task_id >= 0 and task_id < len(tarefas):
        if request.method == 'POST':
            descricao = request.form.get('descricao')
            data_vencimento = request.form.get('data_vencimento')
            prioridade = request.form.get('prioridade')
            concluida = request.form.get('concluida') == 'on'

            tarefa = tarefas[task_id]
            tarefa['descricao'] = descricao
            tarefa['data_vencimento'] = data_vencimento
            tarefa['prioridade'] = prioridade
            tarefa['concluida'] = concluida

            tarefas[:] = sorted(tarefas, key=ordenar_tarefas)
            return redirect(url_for('index'))
        else:
            tarefa = tarefas[task_id]
            return render_template('editar_tarefa.html', tarefa=tarefa, task_id=task_id)
    else:
        return "Tarefa não encontrada."

@app.route('/excluir_tarefa/<int:task_id>')
def excluir_tarefa(task_id):
    if task_id >= 0 and task_id < len(tarefas):
        tarefas.pop(task_id)

        tarefas[:] = sorted(tarefas, key=ordenar_tarefas)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

