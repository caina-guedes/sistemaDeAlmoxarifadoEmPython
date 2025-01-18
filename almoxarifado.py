import funcoesBancoDeDados as fbd
import copy
# FerEquip={
#     'mr':'marreta',
#     'mt':'martelo',
#     'tq':'torquez',
#     'mr':'marreta',
#     'ch':'chave de boca',
#     'au':'alicate universal',
#     'acp':'alicate de corte pequeno',
#     'acg':'alicate de corte grande',
#     'sdm':'serra de mao',
#     'nm':'nivel magnetico',
#     'cp':'colher de pedreiro',
#     'tal':'talhadeira',
#     'pon':'ponteira',
#     'ctt':'catraca de torque',
#     'ctc':'catraca de carga',
#     'cin':'cinta de carga',
#     'prf':'parafusadeira',
#     'frd':'furadeira',
#     'des':'desimpenadeira',
#     'lv':'luva',
#     'mtb':'martelo de borracha',
#     'pa':'pa',
#     'enx':'enxada',
#     'cl':'cavadeira lisa',
#     'ca':'cavadeira ariticulada',
#     'chi':'chibanca',
#     'pic':'picareta',
#     'exd':'enxadao',
#     'esq':'esquadro',
#     'esc':'escada',
#     'pre':'prenca',
#     'vib':'vibrador de concreto',
#     'ger':'gerador',
#     'comp':'compactador de solo',
#     'esm':'esmerilhadeira',
#     'sec':'serra circular',
#     'sem':'serra mármore',}
## esse codigo abaixo é para recolocar as siglas quando for refazer o banco de dados

#for x in FerEquip:
#    querry=f"insert into siglasENomesDeEquips (abreviaturaDeEquipamento,nomeCompleto) values ('{x}','{FerEquip[x]}')"
#    print(querry)
#    exe(querry)


    



class Controle:
    def __init__( self  ,  funcionario  =  ''  ,modo  =  ''  ,  equip  =  []  )  :

        self.modos               = { 's':'saida', 'e':'entrada', } #variavel contendo os tipos de modos (entrada ou saida)             
        self.funcionarioAtual    = funcionario
        self.modoAtual           = modo
        
        self.historicoDeComandos             = []
        self.stringDosComandosDoBancoDeDados = []

        self.listaEquipAtual = equip
        
        self.verificarPossiveisEquips = False
        self.possiveisEquipsParaRegistrar = []

        self.dataInicio  =  ''                                 # acho que nao esta sendo usado 
        self.dataFim     =  ''                                 # acho que não esta sendo usado

        self.funcionariosdb  =  {}
        self.funcionarioQueSeraOAtual  =  ''

        self.usoExterno = False

        self.stringsDeComandos=[]

        self.comandControler  = {}

        self.ferEquipdb = {}
        
        self.FromGUI = False

        self.respostaParaGUI  =  [] #######################esta variável precisa receber objetos no formato do respostaUnitaria ############
        
        self.respostaUnitaria = {'colunas':[],'resposta':[]}
        
        self.comandControler  =  {
    'funcionarios'  :  [False  ,  fbd.mostraFuncionarios             ],       # feito
    'obj'           :  [False  ,  fbd.printObj                       ],       # feito
    'newf'          :  [False  ,  fbd.registraFuncionarioNovo        ],       # feito
    'saida'         :  [False  ,  fbd.modoSaida                      ],       # tem que implementar esse comando
    's'             :  [False  ,  fbd.modoSaida                      ],
    'entrada'       :  [False  ,  fbd.modoEntrada                    ],       # tem que implementar esse comando
    'e'             :  [False  ,  fbd.modoEntrada                    ],
    'pendenciasfunc':  [False  ,  fbd.pendenciasFuncionario          ],
    'histhojefunc'  :  [False  ,  fbd.equipamentosHojeDeFuncionario  ],
    'equipsfora'    :  [False  ,  fbd.equipsforaHoje                 ],
    #'histequip'     :  [False  ,  fbd.historicoFerramenta            ],
    'externo'       :  [False  ,  fbd.usoExterno                     ],
    'siglasequips'  :  [False  ,  fbd.mostraListaDeSiglasEEquips     ],
    'externo'       :  [False  ,  fbd.usoExterno                     ],
    'comandos'      :  [False  ,  fbd.ShowComands                    ],
    'limparegistros':  [False  ,  fbd.limpaRegistros                 ],
    'histhoje'      :  [False  ,  fbd.histHoje                       ],
    'inicio'        :  [False  ,  fbd.retornaObjParaValoresIniciais  ],
    1               :  [False  ,  None                               ,  {}  ]  ,
    #'cancela'       :  [False  ,  fbd.cancelaRegistro                ]
    }

        self.signalToWait  =  '.;.;'

    class RespostaUnitaria:
        
        def __init__( self  ,  resposta  =  []  ,  colunas = []  ,  antes  =  '',  ids  =  []  ) :

            self.avisoAntes = antes
            self.resposta   =  resposta   ###############     aqui tem que ser uma lista de linhas
            self.colunas    =  colunas    ###############     aqui vai a lista com o nome das colunas
            self.listaDeIDs  =  copy.deepcopy(ids)
        
        def __str__(self):
            
            cara  =  "a resposta é : "  +  str(self.resposta)  +  "\n    e as colunas são:  "  +  str(self.colunas) + "\n e o aviso antes é: "  +  str(self.avisoAntes)
            print(cara)
            return cara
        


    def setaFuncaoRecorrente(self, funcao):
        self.comandControler[1][0] = True             ###################### preciso setar isso sempre que for a primeira vez que usa função recorrente
        self.comandControler[1][1] = funcao 
    
    def enviaParaRespostaGUI(  self  ,  resposta  ,  nomesColunas  ,  antes  =  '' ,identificador =  False ) :
        """
        nesta função para pegar o id corretamente ele precisa vir como o primeiro valor
        """
        print('dentro do enviaParaRespostaGUI veio o argumento:  ',resposta)
        respostaAtual=copy.deepcopy(self.RespostaUnitaria())
        respostaAtual.colunas  =  nomesColunas
            
        if type(resposta)  ==  str  :        ######################## se for string acrescenta diretamenta a string dentro da resposta da GUI
            respostaAtual.resposta.append(resposta)
        
        elif type(resposta) in [list,tuple]:
            listaDeIDs =  []
            for linha in resposta:
                if identificador:
                    respostaAtual.resposta.append(linha[1:])
                    respostaAtual.listaDeIDs.append(linha[0])
                else:
                    respostaAtual.resposta.append(linha)
        else:
            print("não sei trabalhar com isso: ",resposta)
            print('o tipo é: ', type(resposta))
        self.respostaParaGUI.append(respostaAtual)
        strDaRespostaUnitaria = str(self.respostaParaGUI[0].__str__)
        print('a resposta para GUI é: ', strDaRespostaUnitaria)

    def resgataRespostaGUI(self):

        print(  'a resposta resgatada da GUI é: '  ,  self.respostaParaGUI  )
        resposta  =  self.respostaParaGUI.copy()
        self.respostaParaGUI  =  copy.deepcopy([])
        return resposta
            
        
    
    def atualizaVariavelFuncionarios(self):

        debug  =  fbd.Debug()
        var  =  {}
        for x in fbd.exe('select nome, funcao from funcionarios'):
            var[str(x[0])]=str(x[1])
        self.funcionariosdb = fbd.dictToSortedDict(var)
        if debug.debug:
            print('self.funcionariosdb: ',self.funcionariosdb)


    def atualizaVariavelferEquipdb(self):

        for x in fbd.exe('select abreviaturaDeEquipamento,nomeCompleto from siglasENomesDeEquips'):
            self.ferEquipdb[x[0]]=x[1]
        self.ferEquipdb = fbd.dictToSortedDict(self.ferEquipdb)


    def preparaObj(self):

        debug  =  fbd.Debug()
        self.atualizaVariavelFuncionarios()
        self.atualizaVariavelferEquipdb()
        self.FromGUI  =  debug.debug

    def inputTratadaGUI(self,string):

        stringInicial  =  string.lower()
        palavrasNaoTratadas  =  stringInicial.split(' ')
        palavras  =  []
        for word in palavrasNaoTratadas:
            if word == '':
                pass
            elif word[0].isdigit():
                quant  =  ''
                while word[0].isdigit():
                    quant  +=  word[0]
                    word  =  word[1:]
                    
                for x in range(int(quant)):
                    palavras.append(word)
            else:
                palavras.append(word)

        return palavras
            
    def atualizaFerEquipdb(self):

         self.ferEquipdb  =  {}
         res  =  fbd.exe('select abreviaturaDeEquipamento,nomeCompleto from siglasENomesDeEquips')
         if len(res)  >  0  :
             for x in res:
                 self.ferEquipdb[x[0]]  =  x[1]
         else:
             self.enviaParaRespostaGUI('banco de dados sem registro na lista de ferramentas',nomesColunas  =  []  )


    def __str__(self):

        a  =  f""" \n funcionarioAtual é: {self.funcionarioAtual}  \n
                    modoAtual é: {self.modoAtual} \n
                    historicoDeComandos é: {self.historicoDeComandos} \n
                    listaEquipAtual é: {self.listaEquipAtual}\n
                    usoExterno é: {self.usoExterno}\n
                    """
        return a

    def action(self):
        """nessa função haverá o comando para de fato executar os comandos requeridos"""
        
        if not self.funcionariosdb or not self.ferEquipdb:
            self.preparaObj()
        if  self.comandControler[1][0]:
            resposta  =  self.comandControler[  1  ][  3  ]
            self.comandControler[  1  ][  1  ](  resposta  )
            if len(  self.comandControler[1] )  >=  4 :
                print('vou apagar a resposta por fora da função de recorrencia e a resposta é:  ',self.comandControler[1])
                self.comandControler[1] = self.comandControler[1][:3]
            else:
                print('a função apagou a resposta internamente')
        else:
            for x in self.comandControler:
                
                if  x  ==  1  :
                    pass                       
                else:
                    print('o atributo do comand controler é:  ',x)
                    if self.comandControler[  x  ][  0  ]  :

                        self.comandControler[  x  ][  1  ](  self  )     #### invoca a função referenciada ao comando
                        self.comandControler[  x  ][  0  ]  =  False
                    
        if self.funcionarioQueSeraOAtual:
            self.atualizaFuncionario(self.funcionarioQueSeraOAtual)
            self.funcionarioQueSeraOAtual  =  ''

        if len(self.listaEquipAtual)  >  0  :
            if self.funcionarioAtual  :
                
                if   self.modoAtual  ==  "saida":
                    fbd.registraSaida(self)
                elif self.modoAtual  ==  'entrada':
                    fbd.registraEntrada(self)
                else  :
                    if self.FromGUI  :
                        self.enviaParaRespostaGUI(f'modo não reconhecido: {self.modoAtual}',nomesColunas=[])
                    else  :
                        print(f'modo não reconhecido: {self.modoAtual}')
            else  :
                if self.FromGUI  :
                    self.enviaParaRespostaGUI('não há funcionario definido',nomesColunas=[])
                else  :
                    print('não há funcionario definido')
                
        if self.verificarPossiveisEquips:
            print('vou verificar possíveis equips novos, e a lista é: ',self.possiveisEquipsParaRegistrar)
            ######################################### acho que o problema esta nessa variavel "possiveisEquipsParaRegistrar"
            ######################################### pois não estou alterando ela durante as recorrências
            if  self.FromGUI  :

                sigla  =  self.possiveisEquipsParaRegistrar[0]
                self.enviaParaRespostaGUI(f"a palavra: {sigla} é uma nova sigla de ferramenta? (y/n)",nomesColunas  =  []  )
                self.comandControler[1][0]  =  True
                self.comandControler[1][2]['sigla']  = copy.copy(sigla)
                self.comandControler[1][1]  =  self.recorrenteConfirmaSeEFerramenta
                                    
                if len(self.possiveisEquipsParaRegistrar) == 1:
                    self.comandControler[1][2]['equipsRemanescentes'] = [].copy()
                    
                elif len(self.possiveisEquipsParaRegistrar)  >  1  :
                    self.comandControler[1][2]['equipsRemanescentes'] = self.possiveisEquipsParaRegistrar[1:]
                    print('a linha da recorrencia aqui esta assim:  ',self.comandControler[1])
            else  :

                for  coisa  in  self.possiveisEquipsParaRegistrar  :

                    if input(f"a palavra: {coisa} é uma nova sigla de ferramenta? (y/n)").lower() == 'y':
                        nomeCompleto = input('qual o nome dessa ferramenta?').lower()
                        querry = f"insert into siglasENomesDeEquips (abreviaturaDeEquipamento,nomeCompleto) values ('{coisa}','{nomeCompleto}')"

                        fbd.exe(querry)
                        fbd.mydb.commit()
                        self.atualizaFerEquipdb()
                    else:                    
                        print( ' eu nao sei o que é isso: ',coisa)

                self.verificarPossiveisEquips = False
                self.possiveisEquipsParaRegistrar = [].copy()
            
    def recorrenteConfirmaSeEFerramenta(self,resposta):
        print('cheguei na recorrente da possivel ferramenta')

        palavra  =  ''
        for x in resposta.split(' '):
            if x:
                palavra  =  x.lower()
                break
        if palavra == 'y':
            print('a resposta foi que sim')
            self.enviaParaRespostaGUI('qual o nome dessa ferramenta?', nomesColunas  =  [])
            self.comandControler[1][1]  =  self.recorrenteRegistraNomeFerramenta
        else:
            sigla  =  self.comandControler[1][2]['sigla'] 
            self.enviaParaRespostaGUI(f'não sei o que é isso  {sigla}', nomesColunas  =  [])
            self.verificaMaisFerramentasParaRecorrencia()


    def recorrenteRegistraNomeFerramenta(self,resposta):
        print('entrei na segunda funcao de registrar nova ferramenta')
        sigla  =  self.comandControler[1][2]['sigla']
        nomeCompleto = resposta

        querry = f"insert into siglasENomesDeEquips (abreviaturaDeEquipamento,nomeCompleto) values ('{sigla}','{nomeCompleto}')"

        fbd.exe(querry)
        fbd.mydb.commit()

        self.atualizaFerEquipdb()
        self.verificaMaisFerramentasParaRecorrencia()

    def verificaMaisFerramentasParaRecorrencia(self):
        if len(self.comandControler[1][2]['equipsRemanescentes'])  >  0:
            palavra  =  self.comandControler[1][2]['equipsRemanescentes'][0]
            self.comandControler[1][2]['sigla']  = palavra
            self.comandControler[1][2]['equipsRemanescentes']  =  self.comandControler[1][2]['equipsRemanescentes'][1:]
            self.enviaParaRespostaGUI(f"a palavra: {palavra} é uma nova sigla de ferramenta? (y/n)", nomesColunas  =  []  )
            self.comandControler[1][1]  =  self.recorrenteConfirmaSeEFerramenta
        else:
            self.verificarPossiveisEquips  =  False
            fbd.fimDaRecorrencia(self)
            self.possiveisEquipsParaRegistrar = [].copy()
            
            
    def atualizaFuncionario(self,funcionarioNovo):
        """toda atualização de funcionario atual tem que ser feita por aqui"""
        funcionarioAntigo      =  self.funcionarioAtual
        self.funcionarioAtual  =  funcionarioNovo   # aqui que eu atualizo o funcionario atual

        if funcionarioNovo: 
            if funcionarioAntigo:
                resposta  =  ' funcionario mudou de '  +  funcionarioAntigo  +  ' para '  +  self.funcionarioAtual
                if self.FromGUI:
                    self.enviaParaRespostaGUI(resposta,nomesColunas  =  []  )
                else:
                    print(resposta)
            else :
                resposta = 'funcionario atual é : '  +  self.funcionarioAtual
                if self.FromGUI:                   
                    self.enviaParaRespostaGUI(resposta,nomesColunas  =  []  )
                else:
                    print(resposta)
        else:
            self.funcionarioAtual  =  ''
            
    def atualizaFerramentaAtual(self,ferramenta, identificador):
        
        self.listaEquipAtual.append({'nome'  :  ferramenta , 'identificador'  :  identificador})

    
    def usoForaDaObra(self):
        if self.FromGUI:
            pass   ############################## preciso implementar essa parte com a GUI
        else:
            if input('deseja setar o uso para externo?(s/n)').lower()  ==  's'  :
                self.usoExterno  =  True
            else:
                self.usoExterno  =  False
            
        
    def RegistraELimpaListaEquipAtual(self):

        self.historicoDeComandos.append( 
            [  
               self.funcionarioAtual  ,  
               self.modoAtual  ,  
               self.listaEquipAtual  ,  
               self.stringDosComandosDoBancoDeDados  
            ]  
        )
        self.listaEquipAtual  =  [].copy()
        self.stringDosComandosDoBancoDeDados  =  [].copy()
        

def stringParser(  listaDeStrings  ,  obj  ):
    """
    essa função precisa receber a lista de strings ja pre-tratada pela função 'inputTratada'
    """
    palavras  =  listaDeStrings
    print("as palavras que entraram no string parser são:",palavras)
    debug  =  fbd.Debug()

    
    if obj.comandControler[1][0]:  ##############################   usada em caso de interações recorrentes. vai acrescentar no fim da lista correspondente #############################
                               ##############################   do comandControler a resposta para a função de recorrencia apontada nele  ###########################################
        print('vim parar nesse if do stringparser e a palavra é:  ',palavras)
        obj.comandControler[1].append(palavras)
    else:
        
        for  palavra  in  palavras  :
            
            if  palavra  in   obj.comandControler  :
                resposta = 'reconheci o comando: '  +  str(palavra)

                if obj.FromGUI:
                    obj.enviaParaRespostaGUI(resposta,nomesColunas  =  []  )

                if  debug.debug  :
                    print(resposta)

                obj.comandControler[palavra][0]  =  True
                
            elif  palavra  in  obj.funcionariosdb  :
                obj.funcionarioQueSeraOAtual  =  palavra
                                
            else  :
                fbd.analizaStringDeFerramenta(  obj  ,  palavra  )

    return obj
def prompt():
    """ essa função executa o programa via terminal"""        
    VariaveisDeControle  =  Controle()
    VariaveisDeControle.atualizaVariavelFuncionarios()    
    while  True  :
        listaDePalavras  =  fbd.inputTratada()
        VariaveisDeControle  =  stringParser(  listaDePalavras  ,  VariaveisDeControle  )
        VariaveisDeControle.action()
        
        
    
