MyGest Projet - parte dedicada para a explicação do sistema

BIBLIOTECAS
As bibliotecas utilizadas foram:
  Tkinter para criação de janela e seus elementos (botoes, frames, etc)
  SQLite para criação integrada do Banco de Dados
  ReportLab para criar relatorios em PDF
  WebBrowser para visualizar e editar o documento PDF via programa terceirizado ou na web

CLASSE RELATORIOS
Nessa classe, estão as duas funções reponsaveis por criar, montar e visualizar o documento PDF em um outro ambiente virtual.
"def printcliente()" abre uma pagina em um abiente virtual, enquanto "def geraRelatCliente()" usa das ferramentas de ReportLab para montar o PDF com as informações selecionadas, 
se nenhuma informação for selecionada, o documento estará vazio.

CLASSE VALIDADOR
Esta classe serve para tratar de exceções dentro do sistema e garantir que os campos sejam preenchidos com as os tipos primitivos corretos, isso é, int, alph e alnum.
Infelizmente, essa classe ainda não contem linhas de código, por isso está comentada, mas seram implementados codigos dentro dele.

CLASSE FUNCS
Essa classe é responsavel por todas as ações funcionais do sistema, aqui o são gerados as execuções de CRUD do Banco, funções responsaveis pela ação de cada botão dentro das abas dos 
sistema, e também funções responsáveis por sempre atualizar a tabela com as informações do Banco, sempre que alguma alteração for feita. 

CLASSE APLICAÇÃO
Na classe Aplicação, estão todos os objetos reponsáveis por fazer o sistema existir, como a criação e a definição do tamanho e formato de cada aba, frame, botões e tabelas, 
além da janela principal onde tudo isso está sendo geral. Ela também recebe como parametro o nome das outras classes para que possa usar as suas funções.
As funções:
"def __init__(self, master=none)" inicializa as funções do sistema. 
"def tela()" contem as informações da janela principal. 
"def nova_janela()" acabou sendo usada para fins didáticos, sem conter uma real funcionalidade. 
"def abas()" cria três abas, uma dedicada para cadastro de usuários (cliente, vendedor, fabricante), uma para cadastro  de produtos, e uma para gestão de pedidos e vendas
"def frames()" contem diversos frames (mini-janelas) dentro de cada aba, cada aba contem uma quantidade exclusiva de frames, eles estão divididos em um contagem crescente de cima para
              baixo e da esquerda para a direrita, ou seja, o frame mais alto e mais a esqueda será o primerio frame e o frame mais baixo e mais a direita será o ultimo frame, 
              segue o mesmo formato das revistas em quadrinhos. 
"def menus()" cria um menu no canto superior esquerdo contendo as funções nova_janela e relatorio. 
"def widgets_frame1()" aqui, estão sendo criados, armazenados e organizados TODAS as informações e funcionalidades de widgets que estejam dentro de QUALQUER frame 1 do sistema.
"def widgets_frame2()" aqui, estão sendo criados, armazenados e organizados TODAS as informações e funcionalidades de widgets que estejam dentro de QUALQUER frame 2 do sistema.                                   Atualmente, aqui também está contido as informações do frame3_aba2. 






