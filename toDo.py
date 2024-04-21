import flet as ft
import sqlite3

class ToDo:
    #metodo construtor
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.bgcolor = ft.colors.BLACK # define a cor de fundo da página
        self.page.window_width = 350 #tamanho de largura da tela
        self.page.window_height = 650 #tamanho de altura da tela
        self.page.window_resizable = False #Para não redimensionar a página
        self.page.window_always_on_top = True #para a aplicação sempre ficar por cima da tela do editor
        self.page.title = 'ToDo App' #titulo da pagina
        self.task = '' #variável onde será armazenada a task
        self.view ='all' #view padrão onde mostra todos os elementos
        
        #inicialização do banco de dados SQLite
        self.db_execute('CREATE TABLE IF NOT EXISTS tasks(name, status)') #Criando tabela chamada 'tasks' com 2 colunas 'name e status'
        self.results = self.db_execute('SELECT * FROM tasks') #selecionar tudo que esta nas tasks
        self.main_page()
        
    def db_execute(self, query, params = []): #Função que vai manipular o BANDO DE DADOS (BD)
        with sqlite3.connect('database.db') as con: #abrir e fechar conexão do BD/ conectando ao banco de dados
            cur = con.cursor() #criando um cursor
            cur.execute(query, params) #realiza a execução da query no BD
            con.commit() #salvar qualquer execução do BS
            return cur.fetchall() #retornar todas as linhas do BD
        
    def set_value(self, e): #função para pegar o valor que está no input
        self.task = e.control.value #salvar o valor do input dentro da variável task
    
    def add(self, e, input_task): #criando função para o botão de + funcionar
        name = self.task #valor inserido no banco de dados 
        status = 'incomplete' #sempre sera inicializada como incompleta
        
        if name:
            self.db_execute(query = 'INSERT INTO tasks VALUES(?, ?)', params = [name, status])
            input_task.value = '' #ao inserir uma task, o input será limpado e zerado
            self.results = self.db_execute('SELECT * FROM tasks') #selecionar tudo que esta no BD
            self.update_task_list() #função para atualizar as tasks
            
    def checked(self, e): #função para task check
        is_checked = e.control.value #verificar se a task esta marcada
        label = e.control.label #pegar o titulo da checkbox e verifiar se esta selecionado
        
        if is_checked:
            self.db_execute('UPDATE tasks SET status = "complete" WHERE name = ?', params = [label]) #atualizando o status como completo 
        else:        
            self.db_execute('UPDATE tasks SET status = "incomplete" WHERE name = ?', params = [label]) #atualizando o status como incompleto
        
        if self.view == 'all': #se eu estiver visualizando todos os itens
            self.results = self.db_execute('SELECT * FROM tasks') #seleciono todos as tasks do BD
        else: #se não for todos os itens
            self.results= self.db_execute('SELECT * FROM tasks WHERE status = ?', params=[self.view]) #irá mostrar os itens de acordo com o status
        
        self.update_task_list()

            
    def tasks_container(self): #criando o container das checkbox
        return ft.Container( #irá retornar um container
            height = self.page.height * 0.8, # tamanho limite, sempre irá pegar 80% do tamanho disponível da página
            content = ft.Column( #conteudo em forma de coluna da pagina
                controls = [ #elementos dentro da coluna
                    ft.Checkbox(label = res[0], 
                                on_change = self.checked,
                                value = True if res[1] == 'complete' else False #o elemento será a checkbox, o value determina que ela esteja marcada se a coluna estiver como completa e False se estiver com Incomplete
                    )  for res in self.results if res], #criando um elemento para cada checkbox em results
                scroll = ft.ScrollMode.ALWAYS
            )
        )
        
    
    def update_task_list(self):
        tasks = self.tasks_container() #criar container com todas as tasks na página
        self.page.controls.pop() #deletear o último elemento
        self.page.add(tasks) # sobreescrever com o elemento novo
        self.page.update() #aparecer pro usuário
        
    def tabs_changed(self, e):
        if e.control.selected_index == 0: #se o index for 0, mostrará tds as tasks
            self.results = self.db_execute('SELECT * FROM tasks')
            self.view == 'all'
        elif e.control.selected_index == 1:
            self.results = self.db_execute('SELECT * FROM tasks WHERE status = "incomplete"')
            self.view = 'incomplete'
        elif e.control.selected_index == 2:
            self.results = self.db_execute('SELECT * FROM tasks WHERE status = "complete"')
            self.view = 'complete'
        
        self.update_task_list()
    
    def main_page(self):
        input_task = ft.TextField(#primeiro campo de input do app
            hint_text = 'Digite aqui uma tarefa',
            expand=True,
            on_change = self.set_value 
        )
        
        input_bar = ft.Row( #criando uma nova linha para adicionar o input e o botao na mesma linha
            controls=[ #elementos que estarao dentros dessa row(linha)
                input_task, #o campo de digitar a task
                ft.FloatingActionButton( #botão de +
                    icon = ft.icons.ADD,
                    on_click = lambda e: self.add(e, input_task) #ao clicar no botão de +, irá adicionar um evento e um input
                    ) 
            ]
        )
        
        tabs = ft.Tabs( #abas de status das tasks
            selected_index = 0, #das tabs criadas sempre sera selecionada a primeira
            on_change = self.tabs_changed,
            tabs = [
                ft.Tab(text = 'Todos'), #primeira tab
                ft.Tab(text = 'Em andamento'), #segunda tab
                ft.Tab(text = 'Finalizados') #terceira tab
            ],
        )
        
        tasks = self.tasks_container() #criando container das tasks

        self.page.add(input_bar, tabs, tasks) #adicionando o input na page
        
ft.app(target = ToDo)