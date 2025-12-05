from __future__ import annotations
from abc import ABC, abstractmethod, abstractproperty

class notACompositeError(Exception):
    pass

# Árvore (com o padrão composite) =============================================

# Para evitar que operações de nó sejam feitas nas folhas, adaptei a estratégia
# do "getComposite" apresentada no livro. Mas no lugar de retornar algo
# que permita ao cliente usar os métodos de coleção, fiz um método isComposite
# que retorna uma flag dizendo se o objeto é ou não coleção. O cliente vai ler
# essa flag enquanto faz suas operações, e caso use uma operação onde não
# deveria, um erro vai ser lançado. (página 164/165 do GOF)
class Node(ABC):
    def  __init__(self, datapoints: list):
        self._datapoints = datapoints
        
    @property
    def datapointCount(self) -> int:
        return len(self._datapoints)

    @property
    def datapoints(self) -> list:
        return self._datapoints

    #interfaces de composite
    def is_composite(self):
        return False

    def set_left_child(self, child: Node) -> None:
        raise notACompositeError("Tried to add a child to a node that isn't a composite")

    def set_right_child(self, child: Node) -> None:
        raise notACompositeError("Tried to add a child to a node that isn't a composite")
    
    def get_children(self) -> tuple[Node, Node]:
        raise notACompositeError("Tried to access children from a node that isn't a composite")

    #interfaces das operações de nós e folhas
    @abstractmethod
    def getSplitInformation(self) -> tuple[str, float]: ...

    @abstractmethod
    def setSplitInformation(self, split_column: str, threshold: float) -> None: ...

    @abstractproperty
    def value(self) -> float: ...


class DecisionNode(Node):
    def __init__(self, datapoints):
        super().__init__(datapoints)
        self.left_node = None
        self.right_node = None

    def is_composite(self):
        return True

    def set_left_child(self, child: Node) -> None:
        if isinstance(child, Node):
            self.left_node = child
        else:
            raise TypeError("Tried to set a non-node object as a node in the tree")

    def set_right_child(self, child: Node) -> None:
        if isinstance(child, Node):
            self.right_node = child
        else:
            raise TypeError("Tried to set a non-node object as a node in the tree")

    def get_children(self) -> tuple[Node, Node]:
        return (self.set_left_child, self.set_right_child)


    def getSplitInformation(self):
        print("Retornando informações sobre o split de um nó específico...")

    def setSplitInformation(self, split_column: str, threshold: float) -> None:
        print("Mudando como o nó faz o split...")

    def value(self) -> float:
        print("Calculando valor de retorno de uma divisão com base nas folhas dela...")


class LeafNode(Node):
    def getSplitInformation(self):
        raise notACompositeError("Tried to set a split rule in a leaf")

    def setSplitInformation(self, split_column: str, threshold: float) -> None:
        raise notACompositeError("Tried to get a split rule from a leaf")
    
    def value(self) -> float:
        print("Calculando o valor de uma folha com base nos datapoints dela...")


# TreeBuilder e os states
class TreeBuilder: #context
    pass

class TreeBuilderState(ABC):
    pass
    #terá os mesmos métodos de tree builder

class SplittingState(TreeBuilderState):
    pass

class StoppingState(TreeBuilderState):
    pass

class PrunningState(TreeBuilderState):
    pass

# Iterator da árvore como um todo
# Serão retornados por algum nó quando solicitado
class TreeIterator(ABC):
    pass

class PreOrderIterator(TreeIterator):
    pass

class BFSIterator(TreeIterator):
    pass

# Visitors para executar algorítmos
class TreeVisitor(ABC):
    pass

class DepthVisitor(TreeVisitor):
    pass

class CountLeavesVisitor(TreeVisitor):
    pass
