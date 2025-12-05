# Projeto de Modelagem: Árvores de decisão

O intuito deste repositório é demonstrar a modelagem de classes de um sistema
de árvores de decisão.

## Modelagem

### Estrutura da árvore

A árvore de decisão é a parte central do projeto e foi modelada utilizando o
padrão [composite](https://github.com/pedrotokar/engenharia-software/blob/master/resumos/composite.md). 
O padrão estabelece uma forma de compartilhar interfaces entre diferentes
objetos que fazem parte de uma estrutura hierárquica. Com o padrão, o cliente
pode utilizar intercambiavelmente as interfaces, independente do objeto
manipulado ser uma folha ou uma coleção de outros objetos.

No caso do projeto atual, foi definida uma classe `Node`, equivalente a classe
`Component` do padrão. Essa classe define métodos para navegação de filhos em
composites e métodos importantes para a lógica das árvores de decisão. Essa
classe fornece uma implementação padrão para os métodos de navegação, e a
implementação por sua vez lança um erro `notACompositeError`, indicando que
aquele método está sendo chamado em uma folha, comportamento que não faz
sentido. 

Definir o funcionamento desses métodos nesse padrão é um desafio, e esta
implementação vai de acordo com o sugerido no livro do GoF (página 165/166).
Assim, as folhas não precisam se preocupar com sobreescrever esses métodos, e
apenas os composites farão isso. A interface também define um método 
`is_composite`, para que o cliente possa averiguar se um objeto é folha ou nó.
Essa é uma adaptação da abordagem com `getComposite` apresentada no livro.

As folhas da árvore são representadas pela subclasse `LeafNode` (que no padrão)
se encaixa como uma `Leaf`) e os nós de decisão são representados pela
subclasse `DecisionNode` (que no padrão se encaixa como um `Composite`). Os
`DecisionNode` sobreescrevem os métodos de navegação para permitir a adição
de nós. Como se trata de uma árvore de decisão simples, os métodos consideram
uma árvore binária (ou seja, o `Composite` só tem duas childs.), já que
árvores mais complexas podem ser reduzidas para árvores binárias.

A interface comum para nós e folhas (equivalente ao método `Operation()` do
padrão) envolve a inspeção de critérios de divisão da árvore, de quais
valores um nó retorna e quais datapoints do treino estão naquela ramificação
da árvore.

### Construção da árvore

A árvore é construida com o auxilio de uma classe `TreeBuilder`. Ela contém
os métodos `start_splitting` e `start_pruning`, e é inicializadda com o dataset
que será usado para fazer a árvore. Cada método inicia a respectiva etapa de
construção da árvore, e retorna a árvore resultante da etapa (que também pode
ser acessada por uma propriedade do `treeBuilder`). A ideia é que cada
instância de `treeBuilder` só seja capaz de inicializar uma única árvore, e não
repetir as etapas nela. Se for desejado fazer outra árvore, outra instância de
`treeBuilder` deve ser inicializada. Uma árvore também não pode ser podada
antes de ter sido criada.

Esse comportamento é atingido por meio do padrão [state](https://github.com/pedrotokar/engenharia-software/blob/master/resumos/state.md)
. Aqui, a classe `TreeBuilder` equivale ao contexto, e só pode ter três
estados: a árvore estar pronta para ser criada, pronta para ser podada ou já
finalizada. Uma classe abstrata `treeBuilderState` define os métodos para
subclasses dela, que representam esses três estados, efetivamente 
implementarem. Esses métodos são expostos na classe `treeBuilder`, mas ela
basicamente delega eles para a subclasse de `treeBuilderState` que estiver
setada como seu estado atual.

O estado de poda, por exemplo, não permite que uma chamada para criar a árvore
funcione, e lança uma exceção caso isso seja feito. Em compensação, outros
estados também não permitem a chamada para podar a árvore, e apenas o estado
de poda efetivamente implementa isso. O último estado, `FinishedState`, não
permite nenhuma chamada, já que a árvore está finalizada e não há o que mexer
nela.

As instâncias de estados não mantém informações sobre a árvore armazenadas
nelas mesmas, e sim usam a instância de `TreeBuilder` para isso. Seria possível
então usar um singleton nessas subclasses, mas isso não foi feito por fugir do
escopo do trabalho.

### Navegação na árvore
