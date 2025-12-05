from __future__ import annotations
from abc import ABC, abstractmethod, abstractproperty

class notACompositeError(Exception):
    pass

class InvalidBuildOperation(Exception):
    pass

# ==================================================== #
#           Árvore (com o padrão composite)            #
# ==================================================== #

class Node(ABC):
    def  __init__(self, datapoints: list):
        self._datapoints = datapoints

    @property
    def datapointCount(self) -> int:
        return len(self._datapoints)

    @property
    def datapoints(self) -> list:
        return self._datapoints

    # Interfaces de composite
    # elas oferecem uma implementação padrão para folhas. Então só subclasses
    # que são composite precisam sobreescrever.
    def is_composite(self):
        return False

    def set_left_child(self, child: Node) -> None:
        raise notACompositeError("Tried to add a child to a node that isn't a composite")

    def set_right_child(self, child: Node) -> None:
        raise notACompositeError("Tried to add a child to a node that isn't a composite")
    
    def get_children(self) -> tuple[Node, Node]:
        raise notACompositeError("Tried to access children from a node that isn't a composite")

    # Interfaces das operações de nós e folhas, tanto composites quanto folhas
    # tem que sobreescrever.
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

# ==================================================== #
#         Construção da árvore (padrão state)          #
# ==================================================== #

# Equivale ao Context
class TreeBuilder:
    def __init__(self, dataset):
        self._dataset = dataset
        self._treeRoot = None
        self._state = SplittingState() # toda construção de árvore começa pelo split
    
    @property
    def dataset(self):
        return self._dataset
    
    @property
    def tree(self):
        return self._treeRoot
    
    def start_split(self) -> Node:
        return self._state.split_tree(self)
    
    def start_prune(self) -> Node:
        return self._state.prune_tree(self)


class TreeBuilderState(ABC):
    @abstractmethod
    def split_tree(self, context: TreeBuilder): ...

    @abstractmethod
    def prune_tree(self, context: TreeBuilder): ...


class SplittingState(TreeBuilderState):
    def split_tree(self, context: TreeBuilder):
        print("Fazendo split da árvore... Adicionando nós...")
        
        # criando uma estrutura mock pra poder testar outras coisas depois
        context._treeRoot = DecisionNode(context.dataset)
        context._treeRoot.setSplitInformation("coluna_1", 9)

        # na prática os nós teriam cada um um subset do dataset, com os
        # subsets respeitando a hierarquia. Mas isso é só um mock
        other_node = DecisionNode(context.dataset)
        other_node.setSplitInformation("coluna_2", 5)

        leaf_node_1 = LeafNode(context.dataset)
        leaf_node_2 = LeafNode(context.dataset)
        leaf_node_3 = LeafNode(context.dataset)

        other_node.set_left_child(leaf_node_1)
        other_node.set_right_child(leaf_node_2)
        context._treeRoot.set_left_child(other_node)
        context._treeRoot.set_right_child(leaf_node_3)

        # a mudança de estado é atomica: essa única linha faz isso.
        # assim evito estados inválidos
        context._state = PruningState()
        return context._treeRoot

    def prune_tree(self, context: TreeBuilder):
        raise InvalidBuildOperation("Tried to prune a tree that wasn't split yet")


class PruningState(TreeBuilderState):
    def split_tree(self, context: TreeBuilder):
        raise InvalidBuildOperation("Tried to split a tree that was already splitten")

    def prune_tree(self, context: TreeBuilder):
        print("Prunning the tree...")
        # aqui não estou fazendo nada. Mas estaria executando um algorítmo para
        # fazer prunning na árvore.

        context._state = FinishedState()
        return context._treeRoot


class FinishedState(TreeBuilderState):
    def split_tree(self, context: TreeBuilder):
        raise InvalidBuildOperation("Tried to split a tree that was already splitten and pruned")

    def prune_tree(self, context: TreeBuilder):
        raise InvalidBuildOperation("Tried to prune a tree that was already splitten and pruned")

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
