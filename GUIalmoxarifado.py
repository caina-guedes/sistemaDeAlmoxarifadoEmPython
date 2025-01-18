import flet as ft
import almoxarifado as amx
import copy
##print('passei do import')


debugPai  =  amx.fbd.Debug()
debug     =  debugPai.debug
              
obj = amx.Controle()
obj.preparaObj()
obj.FromGUI = True

var =  []

class historicoDeResultados():
    
    """ função criada para ter em si o histórico dos comandos executados e dos resultados obtidos  """

    def __init__( self  ,  comando  =  []  ,  resultadoGUI  = [] ,listaDeIDs  =  copy.copy([]) ):
        self.historico = [] ################################### os elementos nessa lista tem que ser uma lista com 2 elementos,
                            ################################### o primeiro sendo a string do comando e o segundo o resultado que foi enviado para a tela
        self.listaDeListasDeIDs  = []
        if listaDeIDs:
            self.listaDeListasDeIDs.append(listaDeIDs)
        self.posicaoAtual = 0   ##### aqui vai ficar a posição das informações que estarão sendo exibidas na tela.
        
        if resultadoGUI and comando:
            self.historico.append([comando,resultadoGUI])
        

    def registrar(self, comando, resultado, listaDeIDs):
        print("dentro da funcao registrar do historico a lista de IDS que veio é: ",listaDeIDs)
        try:
            tabela  =  copy.deepcopy(resultado.content.controls[-1].content.controls[0])
            resultado.content.controls[-1].content.controls[0] = tabela
        except:
            pass
        
        self.historico.append(  [  comando  ,  copy.copy(  resultado  )    ]  )
        self.listaDeListasDeIDs.append(  listaDeIDs  )
        self.posicaoAtual  =  len(self.historico) - 1

    def Atual (self):
        return {'historico'  :  self.historico[self.posicaoAtual]  ,  'listaDeIDs'  :  self.listaDeListasDeIDs[self.posicaoAtual]}

    def Proximo(self):
        
        if self.posicaoAtual  ==  len(self.historico)-1:
            return  self.historico[  self.posicaoAtual  ]
        else:
            self.posicaoAtual += 1
            return  self.historico[  self.posicaoAtual  ]

    def Anterior(self):
        
        if self.posicaoAtual  ==  0  :
            return  self.historico[  self.posicaoAtual  ]
        else:
            self.posicaoAtual -= 1
            return  self.historico[  self.posicaoAtual  ] 

    
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
    historico  =  historicoDeResultados()
    
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
                                           alignment      = ft.alignment.center ,
                                           ),
                              expand              = 1,
                              border_radius       =  20   ,
                              bgcolor    =   ft.Colors.BLUE  ,
                              padding    =   50,
                              alignment  =   ft.alignment.center,
                              )

                
            if len(resp.colunas)  >  0  :
                colunas  =  []
                for nome in resp.colunas:
                    colunas.append(  ft.DataColumn(  ft.Text(nome,  size  =  20  ,),  ))
                    
                respostaAtual.content.controls[0].columns  =  colunas

            if resp.avisoAntes:
                respostaAtual.content.controls.insert(0,ft.Text(resp.avisoAntes))
                
##            var.append(respostaAtual)
            if debug:
                print('a respostaAtual.content é:', respostaAtual.content)
                print('a respostaAtual.content.controls é: ',respostaAtual.content.controls)
                print('as colunas do respAtual são:  ',respostaAtual.content.controls[0].columns)    
            if type(resp.resposta[0])  != str:    
                linhas  =  []
                if resp.listaDeIDs:
                    print('a lista de ips que chegou é:  ',resp.listaDeIDs )
                    contador  =  0
                for linha in resp.resposta:
                    if resp.listaDeIDs:
                        idAtual     =  resp.listaDeIDs[contador]
                        contador   +=  1
                    linhaAtual  =  []
                    for info in linha:
                        linhaAtual.append(ft.DataCell(ft.Text(  info  ,  size  =  15  ,  theme_style  =  ft.TextThemeStyle.DISPLAY_SMALL,overflow = ft.TextOverflow.ELLIPSIS  ), ) )  #### weight  =  ft.FontWeight.W_900 se refere ao quanto é grossa a fonte, estilo negrito a fininho
                    linhas.append(ft.DataRow( cells  =  linhaAtual, on_select_changed = getRow))
                respostaAtual.content.controls[0].rows           =  linhas
##                respostaAtual.padding = ft.padding.symmetric(100, 300)
##                respostaAtual.margin = 30
##                respostaAtual.
                if debug:
                    print("as linhas do resp atual sao: ",respostaAtual.content.controls[0].rows)
                
            
            else:
                respostaAtual  =  ft.Text(resp.resposta[0],text_align=ft.TextAlign.CENTER)
                if debug:
                    print("o texto do respAtual é:  ",respostaAtual.value)
                ############ aqui implementarei as mensagens diretas que nao precisam de coluna
                
            elementos.append(respostaAtual)
            if debug:
                print('a variavel elementos é:' , elementos)
            
        result  =  ft.Column(
                    controls              =  elementos,
                    spacing               =  10,
                    height                =  500,
                    width                 =  1500,
                    expand                =  True,
                    horizontal_alignment  =  ft.CrossAxisAlignment.CENTER,
##            bccolor   =  'black',
##            scroll    =  ft.ScrollMode.ALWAYS
                    )
            #for linha in resposta:
        if debug:
            print('o result no fim da função é: ',result)
            print('os elementos do result no fim da função são: '  ,  result.controls)
        
        realResult   =  ft.Container(
            
            border_radius  =  20  ,
            content        =  result         ,
            bgcolor        =  'grey'         ,
            margin         =  10             ,
            padding        =  40             ,
            alignment      = ft.alignment.center ,
            
            
            )

        return realResult
    
    def getRow(e):
        print('cheguei no get row e a row é:  '  ,  e  )
##        print('seus atributos são:  ', dir(e))
##        print('o control dele é: ',e.control)
##        print('os atributos do control dele são: ',dir(e.control))
        
        e.control.selected  =  not e.control.selected

        ######################################################## esse aqui é o endereço da tabela na pagina atual  ##############################
        possivelTabela = page.controls[0].controls[0].content.controls[-1].content.controls[0]
        print('o elemento page.controls[0].controls[0]..content.controls[-1].content.controls[0] é:   ',possivelTabela)
        for x in range(len(possivelTabela.rows)):
            if possivelTabela.rows[x].selected:
                print(x  ,  possivelTabela.rows[x], historico.Atual()['listaDeIDs'][x])
##        print('o data dele é: ',e.data)
##        print('o nome dele é: ',e.name)
##        print('o page dele é: ',e.page)

        page.update()

    def limpaResposta():
        if page.controls[0].controls[0] != textComandos:
                if debug:
                    print(" entrei no if para retirar as respostas anteriores")
                while page.controls[0].controls[0]  !=  textComandos:
                    page.controls[0].controls  =  page.controls[0].controls[1:]
                    if debug:
                        print("retirei resposta")
        
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
            respostaParaGUI   = obj.resgataRespostaGUI()       ##########   isso aqui é na verdade ums LISTA de Respostas   ##############
            respostaTratada   =  trataRespostaDoOBJ(respostaParaGUI)
            listaDeListasDeIDs  =  []
            for x in range(len(respostaParaGUI)):
                listaDeListasDeIDs.append(copy.copy(respostaParaGUI[x].listaDeIDs))
                print('dentro desse for maluco veio a listaDeIDs assim:  ',respostaParaGUI[x].listaDeIDs)
            print('a lista de ids resgatada diretamente no enterkeyboard é:  ',listaDeListasDeIDs)
                                          
            
##            if debug:
##            print('a variavel respostaParaGUI la na função enterkeyboard é: ',respostaParaGUI)    
            print('a resposta depois de tratada na GUI é:',respostaTratada)
            print('o tipo da resposta tratada é:',type(respostaTratada))
            print('o conteudo do content da resposta tratada é:', respostaTratada.content)
            print('o respostaTratada.content.controls  ', respostaTratada.content.controls)
##            print('o respostaTratada.content.controls[-1].content',respostaTratada.content.controls[-1].content)
##            print('o respostaTratada.content.controls[-1].content.controls',respostaTratada.content.controls[-1].content.controls[0])

            if type(respostaTratada) ==  str:
                textValor.value  =  respostaTratada
                ######################## referente ao historico ############################
                historico.registrar(  comando  ,  respostaTratada  )
                print("o historico de comandos atualmente é:  ",historico.historico)
                ############################################################################
            else:
                if debug:
                    print('o tipo do "page.controls" é: ',type(page.controls))
                    print('o "page.controls" em si da page é: ',page.controls )
                    print("o 'page.controls[0]' é:",page.controls[0])
                    print("o 'page.controls[0].controls' é:",page.controls[0].controls)
                    print("o tipo do 'page.controls[0].controls' é:",type(page.controls[0].controls))
                    print("o 'page.controls[0].controls[-1])' é:",page.controls[0].controls[-1])
                    print("o 'textValorSegundo' é: ",textValorSegundo)
                
                if page.controls[0].controls[0] != textComandos:
                    if debug:
                        print(" entrei no if para retirar as respostas anteriores")
                    while page.controls[0].controls[0]  !=  textComandos:
                        page.controls[0].controls  =  page.controls[0].controls[1:]
                        if debug:
                            print("retirei resposta")
                        
                page.controls[0].controls.insert(  0  ,  copy.deepcopy(respostaTratada)  )

                ######################## referente ao historico ############################
                print('a respostaParaGUI é  :  ', respostaParaGUI)
                
                historico.registrar(  comando  ,  respostaTratada, listaDeListasDeIDs )
                print("o historico de comandos atualmente é:  ",historico.historico)
                ############################################################################

            textComandos.value  =  ''
            textComandos.focus()
        elif e.key == "Arrow Down" and e.ctrl:
            comando  ,  elementoGUI = historico.Proximo()
            
            limpaResposta()
                        
            page.controls[0].controls.insert(  0  ,  elementoGUI   )
##            if debug:
            print("cheguei no Arrow Down")

        elif e.key == "Arrow Up" and e.ctrl:
            comando  ,  elementoGUI = historico.Anterior()
            
            limpaResposta()
                        
            page.controls[0].controls.insert(  0  , elementoGUI   )
##            if debug:
            print("cheguei no Arrow Up")

            
        elif e.key  ==  "Arrow Down" and not e.ctrl :

            #### resultado.content.controls[-1].content.controls[0] = tabela
##            print(page.controls[0].controls[0].content.controls[0])
            for element in page.controls[0].controls[0].content.controls:
                if hasattr(element,'content'):
                    if hasattr(element.content, 'scroll_to'):
                        element.content.scroll_to(delta = 40)

        elif e.key  ==  "Arrow Up" and not e.ctrl :
            
            for element in page.controls[0].controls[0].content.controls:
                if hasattr(element,'content'):
                    if hasattr(element.content, 'scroll_to'):
                        element.content.scroll_to(delta = -40)
        
        page.update()

    obj = amx.Controle()
    obj.preparaObj()
    if debug:
        print(obj)
    page.on_keyboard_event  =  enterKeyboard
    page.scroll = ft.ScrollMode.AUTO
    textValorSegundo  =  ft.Text()
    
    textValor  =  ft.Text('valores aqui')
    
    textComandos  =  ft.TextField(
        hint_text  =  'digite os comandos aqui'  ,
        autofocus  =  True,
        )

    tabela = ft.DataTable(
                            columns               =  []                        ,
                            border                =  ft.border.all(3, "black") ,
                            border_radius         =  20                        ,
                            vertical_lines        =  ft.BorderSide(1, "grey")  ,
                            horizontal_lines      =  ft.BorderSide(2, "grey")  ,
                            heading_row_height    =  35,
                            data_row_max_height   =  35,
                            expand                =  True ,
                            expand_loose          =  True,
                            horizontal_margin     =  15,
                            show_checkbox_column  = True,
                        )
    
    page.add(
        ft.Column(  controls  =  [
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
