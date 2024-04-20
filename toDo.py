import flet as ft


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
        self.main_page()
        
    def tasks_container(self): #criando o container das checkbox
        return ft.Container( #irá retornar um container
            height = self.page.height * 0.8, # tamanho limite, sempre irá pegar 80% do tamanho disponível da página
            content = ft.Column( #conteudo em forma de coluna da pagina
                controls = [ #elementos dentro da coluna
                    ft.Checkbox(label = 'Tarefa 1', value = True) #o elemento será a checkbox, o value determina que ela esteja marcada
                ]
            )
        )
    
    def main_page(self):
        input_task = ft.TextField(hint_text = 'Digite aqui uma tarefa', expand=True) #primeiro campo de input do app
        
        input_bar = ft.Row( #criando uma nova linha para adicionar o input e o botao na mesma linha
            controls=[ #elementos que estarao dentros dessa row(linha)
                input_task, #o campo de digitar a task
                ft.FloatingActionButton(icon = ft.icons.ADD) #botão de +
            ]
        )
        
        tabs = ft.Tabs( #abas de status das tasks
            selected_index = 0, #das tabs criadas sempre sera selecionada a primeira
            tabs = [
                ft.Tab(text='Todo'), #primeira tab
                ft.Tab(text = 'Em andamento'), #segunda tab
                ft.Tab(text = 'Finalizados') #terceira tab
            ]
        )
        
        tasks = self.tasks_container() #criando container das tasks

        self.page.add(input_bar, tabs, tasks) #adicionando o input na page
        
ft.app(target = ToDo)