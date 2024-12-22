import flet as ft
import almoxarifado as amx
##print('passei do import')


debugPai  =  amx.fbd.Debug()
debug     =  debugPai.debug
              
obj = amx.Controle()
obj.preparaObj()
obj.FromGUI = True

var =  []

def identificaTipoDeValores(lista):

    obj  =  globals()['obj']

    valores  =  []

    for x in range(len(lista[0])):
        if all(linha[x] in obj.funcionariosdb for linha in lista):
            valores.append('funcionario')
        ############falta implementar como descobrir outros valores aqui
        else:
            valores.append(None)
            

def main(page: ft.Page)-> None:

    obj  =  globals()['obj']

    page.title  =  'almoxarifado'

    page.vertical_alignment   = 'center'
    page.horizontal_alignment  =  'center'

    
    def trataRespostaDoOBJ(resposta) -> ft.Column:
        """essa função recbe uma lista de "respostaUnitária" e retorna uma coluna com a resposta apropriada para a GUI"""
        var = globals()['var']

        elementos  =  []

        if debug:
            print('o argumento inicial da função trataRespostaDoOBJ é:  ',resposta)    

        for indice in range(len(resposta)):
            resp  =  resposta[indice]
            if debug:
                print("o resp é: ")
                print(resp)
                print('as colunas dentro do resp são :  '  ,  resp.colunas)
                print('a reposta dentro do resp é:  '      ,  resp.resposta)
            
            respostaAtual  =  ft.Container(
                              content    = ft.Column(
                                           controls  = [  tabela  ],
                                           scroll              =  ft.ScrollMode.AUTO,
                                           expand              = 1,                        
                                           ),
                              expand              = 1,
                              border_radius       =  20   ,
                              bgcolor  =  ft.Colors.BLUE  ,
                              padding  =   50,
                              )

                
            if len(resp.colunas)  >  0  :
                colunas  =  []
                for nome in resp.colunas:
                    colunas.append(  ft.DataColumn(  ft.Text(nome,  size  =  20  ,),  ))
                    
                respostaAtual.content.controls[0].columns  =  colunas

            if resp.avisoAntes:
                respostaAtual.content.controls.insert(0,ft.Text(resp.avisoAntes))
                
            var.append(respostaAtual)
            if debug:
                print('a respostaAtual.content é:', respostaAtual.content)
                print('a respostaAtual.content.controls é: ',respostaAtual.content.controls)
                print('as colunas do respAtual são:  ',respostaAtual.content.controls[0].columns)    
            if type(resp.resposta[0])  != str:    
                linhas  =  []
                for linha in resp.resposta:
                    linhaAtual  =  []
                    for info in linha:
                        linhaAtual.append(ft.DataCell(ft.Text(  info  ,  size  =  15  ,  theme_style  =  ft.TextThemeStyle.DISPLAY_SMALL,overflow = ft.TextOverflow.ELLIPSIS  ), ) )  #### weight  =  ft.FontWeight.W_900 se refere ao quanto é grossa a fonte, estilo negrito a fininho
                    linhas.append(ft.DataRow( cells  =  linhaAtual))
                respostaAtual.content.controls[0].rows           =  linhas
##                respostaAtual.padding = ft.padding.symmetric(100, 300)
##                respostaAtual.margin = 30
##                respostaAtual.
                if debug:
                    print("as linhas do resp atual sao: ",respostaAtual.content.controls[0].rows)
                
            
            else:
                respostaAtual  =  ft.Text(resp.resposta[0])
                if debug:
                    print("o texto do respAtual é:  ",respostaAtual.value)
                ############ aqui implementarei as mensagens diretas que nao precisam de coluna
                
            elementos.append(respostaAtual)
            if debug:
                print('a variavel elementos é:' , elementos)
            
        result  =  ft.Column(
                    controls  =  elementos,
                    spacing   =  10,
                    height    =  500,
                    width     =  1500,
                    expand    =  True,
##            bccolor   =  'black',
##            scroll    =  ft.ScrollMode.ALWAYS
                    )
            #for linha in resposta:
        if debug:
            print('o result no fim da função é: ',result)
            print('os elementos do result no fim da função são: '  ,  result.controls)
        
        realResult   =  ft.Container(
            
            border_radius  =  20  ,
            content  =  result         ,
            bgcolor  =  'grey'         ,
            margin   =  10             ,
            padding  =  40             ,
            
            )

        return realResult
    
    def handle_submit(e):

        print(f"handle_submit e.data: {e.data}")

    
    def close_anchor(e):

        text = e.control.data
        
        print(f"closing view from {text}")

    def enterKeyboard( e : ft.KeyboardEvent ) :
        
        textValorSegundo.value  =  e.key
        obj  =  globals()['obj']
        if e.key  ==  'Enter':

            comando  =  textComandos.value
            if debug:
                print('o comando é: ',comando)
            textValorSegundo.value  =  comando
            obj.stringsDeComandos.append(comando)
            if not obj.comandControler[1][0]:
                listaDePalavras  =  obj.inputTratadaGUI(comando)
            else:
                listaDePalavras  =  comando         ###################   essa linha faz com  que a string vá sem tratamento para o stringparser,   ###################
                                                    ###################   isso será usado para o caso de interações recorrentes    ####################################
            
            obj  =  amx.stringParser(listaDePalavras,obj)
            obj.action()
            respostaParaGUI = obj.resgataRespostaGUI()
            respostaTratada   =  trataRespostaDoOBJ(respostaParaGUI)

            if debug:
                print('a variavel respostaParaGUI la na função enterkeyboard é: ',respostaParaGUI)    
                print('a resposta depois de tratada na GUI é:',respostaTratada)
                print('o tipo da resposta tratada é:',type(respostaTratada))

            if type(respostaTratada) ==  str:
                textValor.value  =  respostaTratada
            else:
                if debug:
                    print('o tipo do "page.controls" é: ',type(page.controls))
                    print('o "page.controls" em si da page é: ',page.controls )
                    print("o 'page.controls[0]' é:",page.controls[0])
                    print("o 'page.controls[0].controls' é:",page.controls[0].controls)
                    print("o tipo do 'page.controls[0].controls' é:",type(page.controls[0].controls))
                    print("o 'page.controls[0].controls[-1])' é:",page.controls[0].controls[-1])
                    print("o 'textValorSegundo' é: ",textValorSegundo)
                
                if page.controls[0].controls[-1] != textValorSegundo:
                    if debug:
                        print(" entrei no if para retirar as respostas anteriores")
                    while page.controls[0].controls[-1] != textValorSegundo:
                        page.controls[0].controls.pop()
                        if debug:
                            print("retirei resposta")
                        
                page.controls[0].controls.append(respostaTratada)
            textComandos.value  =  ''
            textComandos.focus()
        elif e.key == "Arrow Down":
            
            if debug:
                print("cheguei no Arrow Down")
        page.update()

    obj = amx.Controle()
    obj.preparaObj()
    if debug:
        print(obj)
    page.on_keyboard_event  =  enterKeyboard

    textValorSegundo  =  ft.Text()
    
    textValor  =  ft.Text('valores aqui')
    
    textComandos  =  ft.TextField(
        hint_text  =  'digite os comandos aqui'  ,
        autofocus  =  True,
        )

    tabela = ft.DataTable(
                            columns             =  []                        ,
                            border              =  ft.border.all(3, "black") ,
                            border_radius       =  20                        ,
                            vertical_lines      =  ft.BorderSide(1, "grey")  ,
                            horizontal_lines    =  ft.BorderSide(2, "grey")  ,
                            heading_row_height  =  35,
                            data_row_max_height =  35,
                            expand              =  1 ,
                            horizontal_margin   =  15,
                        )
    
    page.add(
        ft.Column(  controls  =  [
            textValor,
            textComandos,
            textValorSegundo,
        ],
        alignment  =  ft.MainAxisAlignment.CENTER,
        horizontal_alignment  =  ft.CrossAxisAlignment.CENTER,)
    )
    


if __name__ == '__main__':
    ft.app(target=main)


        
# class EntradaFuncionario(ft.UserControl):
#     def __init__(self,obj):
#         super().__init__()
#         self.obj = obj
#         self. dropdownDosFuncionarios = ft.Dropdown(
#                     # label="Color",
#                     # hint_text="Choose your favourite guy?",
                    
#                     width = 100,
#                     options = [  ft.dropdown.Option(str(funcionario)) for funcionario in self.obj.funcionariosdb   ],
#         )
#     def AtualizaFuncionario(self,nome):
        
#         if nome in self.obj.funcionariosdb:
#             self.obj.funcionarioAtual = nome
#         else:
#             pass
#             # preciso implementar um alerta com o nome e dizendo que não é funcionario da empresa
            
#             # print('não é funcionario da empresa')

    
#     def build(self) -> ft.Row:
#         self.dropdowndefuncionarios.on_change = funcionario_mudou
#         return ft.Row( controls  =  [
#             ft.Text("funcionario: ") ,
#             ft.Column(
#                 controls= [
#                     nomeFuncionario(label='aqui..'),
#                     self.dropdowndefuncionarios,
#                 ],
#                 ##     # falta propriedades para o dropdown aparecer coladinho ao textfield para parecer que são um elemento só.

#             )   
#             #ft.ElevatedButton(  text  =  "confirma" , on_click  =  self.AtualizaFuncionario, margin = ft.margin.only(left=10) ),
#             # self.myButton(),
#             ],
#             # alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
#             # width = 300,
#
