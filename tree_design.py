from __future__ import annotations
from abc import ABC, abstractmethod

class NotACompositeError(Exception):
    pass

class InvalidBuildOperationError(Exception):
    pass

# ==================================================== #
#           Árvore (com o padrão composite)            #
# ==================================================== #

#Equivale ao component
class Node(ABC):
    def  __init__(self, datapoints: list):
        self._datapoints = datapoints

    @property
    def datapoint_count(self) -> int:
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
        raise NotACompositeError("Tried to add a child to a node that isn't a composite")

    def set_right_child(self, child: Node) -> None:
        raise NotACompositeError("Tried to add a child to a node that isn't a composite")
    
    def get_children(self) -> tuple[Node, Node]:
        raise NotACompositeError("Tried to access children from a node that isn't a composite")

    # Interfaces das operações de nós e folhas, tanto composites quanto folhas
    # tem que sobreescrever.
    @abstractmethod
    def get_split_information(self) -> tuple[str, float]: ...

    @abstractmethod
    def set_split_information(self, split_column: str, threshold: float) -> None: ...

    @property
    @abstractmethod
    def value(self) -> float: ...

    # Interface para obter iteradores
    def get_dfs_iterator(self):
        return TreeDFSIterator(self)

    def get_bfs_iterator(self):
        return TreeBFSIterator(self)

    # Interface para receber visitors
    @abstractmethod
    def accept(self, visitor: TreeVisitor) -> None: ...


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
        return (self.left_node, self.right_node)


    def get_split_information(self):
        print("Retornando informações sobre o split de um nó específico...")

    def set_split_information(self, split_column: str, threshold: float) -> None:
        print("Mudando como o nó faz o split...")

    @property
    def value(self) -> float:
        print("Calculando valor de retorno de uma divisão com base nas folhas dela...")

    def accept(self, visitor: TreeVisitor) -> None:
        visitor.visit_decision_node(self)


class LeafNode(Node):
    def get_split_information(self):
        raise NotACompositeError("Tried to set a split rule in a leaf")

    def set_split_information(self, split_column: str, threshold: float) -> None:
        raise NotACompositeError("Tried to get a split rule from a leaf")
    
    @property
    def value(self) -> float:
        print("Calculando o valor de uma folha com base nos datapoints dela...")

    def accept(self, visitor: TreeVisitor) -> None:
        visitor.visit_leaf_node(self)

# ==================================================== #
#         Construção da árvore (padrão state)          #
# ==================================================== #

# Equivale ao Context
class TreeBuilder:
    def __init__(self, dataset):
        self._dataset = dataset
        self._tree_root = None
        self._state = SplittingState() # toda construção de árvore começa pelo split
    
    @property
    def dataset(self):
        return self._dataset
    
    @property
    def tree(self):
        return self._tree_root
    
    def start_split(self) -> Node:
        return self._state.split_tree(self)
    
    def start_prune(self) -> Node:
        return self._state.prune_tree(self)


class TreeBuilderState(ABC):
    @abstractmethod
    def split_tree(self, context: TreeBuilder) -> Node: ...

    @abstractmethod
    def prune_tree(self, context: TreeBuilder) -> Node: ...


class SplittingState(TreeBuilderState):
    def split_tree(self, context: TreeBuilder) -> Node:
        print("Fazendo split da árvore... Adicionando nós...")
        
        # criando uma estrutura mock pra poder testar outras coisas depois
        context._tree_root = DecisionNode(context.dataset)
        context._tree_root.set_split_information("coluna_1", 9)

        # na prática os nós teriam cada um um subset do dataset, com os
        # subsets respeitando a hierarquia. Mas isso é só um mock
        decision_node_1 = DecisionNode(context.dataset)
        decision_node_1.set_split_information("coluna_2", 5)

        decision_node_2 = DecisionNode(context.dataset)
        decision_node_2.set_split_information("coluna_3", -42)

        leaf_node_1 = LeafNode(context.dataset)
        leaf_node_2 = LeafNode(context.dataset)
        leaf_node_3 = LeafNode(context.dataset)
        leaf_node_4 = LeafNode(context.dataset)

        decision_node_1.set_left_child(leaf_node_1)
        decision_node_1.set_right_child(leaf_node_2)
        
        decision_node_2.set_left_child(decision_node_1)
        decision_node_2.set_right_child(leaf_node_3)

        context._tree_root.set_left_child(decision_node_2)
        context._tree_root.set_right_child(leaf_node_4)

        # a mudança de estado é atomica: essa única linha faz isso.
        # assim evito estados inválidos
        context._state = PruningState()
        return context._tree_root

    def prune_tree(self, context: TreeBuilder) -> Node:
        raise InvalidBuildOperationError("Tried to prune a tree that wasn't split yet")


class PruningState(TreeBuilderState):
    def split_tree(self, context: TreeBuilder) -> Node:
        raise InvalidBuildOperationError("Tried to split a tree that was already split")

    def prune_tree(self, context: TreeBuilder) -> Node:
        print("Prunning the tree...")
        # aqui não estou fazendo nada. Mas estaria executando um algorítmo para
        # fazer prunning na árvore.

        context._state = FinishedState()
        return context._tree_root


class FinishedState(TreeBuilderState):
    def split_tree(self, context: TreeBuilder) -> Node:
        raise InvalidBuildOperationError("Tried to split a tree that was already splitten and pruned")

    def prune_tree(self, context: TreeBuilder) -> Node:
        raise InvalidBuildOperationError("Tried to prune a tree that was already splitten and pruned")

# ==================================================== #
#        Navegação na árvore (padrão iterator)         #
# ==================================================== #

class TreeIterator(ABC):
    def __init__(self, tree_root: Node):
        self._tree_root = tree_root
        self._current_index = 0

    @property
    def index(self) -> int:
        return self._current_index

    @property
    @abstractmethod
    def finished(self) -> bool: ...

    @abstractmethod
    def current_item(self) -> Node: ...

    @abstractmethod
    def next_item(self) -> Node: ...


class TreeDFSIterator(TreeIterator):
    def __init__(self, tree_root: Node):
        super().__init__(tree_root)
        self._stack = [tree_root]

    @property
    def finished(self) -> bool:
        return len(self._stack) == 0

    def current_item(self) -> Node:
        return self._stack[-1]

    def next_item(self) -> Node:
        if len(self._stack) == 0:
            raise RuntimeError("Tried to iterate on a exausthed iterator")

        current = self._stack.pop()

        if current.is_composite():
            children = current.get_children()
            self._stack.append(children[1])
            self._stack.append(children[0])

        self._current_index += 1
        return current


class TreeBFSIterator(TreeIterator):
    def __init__(self, tree_root):
        super().__init__(tree_root)
        self._queue = [tree_root]

    @property
    def finished(self) -> bool:
        return len(self._queue) == 0

    def current_item(self) -> Node:
        return self._stack[0]

    def next_item(self) -> Node:
        if len(self._queue) == 0:
            raise RuntimeError("Tried to iterate on a exausthed iterator")

        current = self._queue.pop(0)

        if current.is_composite():
            children = current.get_children()
            self._queue.append(children[0])
            self._queue.append(children[1])

        self._current_index += 1
        return current

# ==================================================== #
#  Execução de algorítmos na árvore (padrão visitor)   #
# ==================================================== #

class TreeVisitor(ABC):
    @abstractmethod
    def visit_decision_node(self, decision_node: DecisionNode): ...

    @abstractmethod
    def visit_leaf_node(self, leaf_node: DecisionNode): ...

class CountLeavesVisitor(TreeVisitor):
    def __init__(self):
        self._leaf_count = 0
    
    @property
    def leaf_count(self) -> int:
        return self._leaf_count
    
    def visit_decision_node(self, decision_node: DecisionNode) -> None:
        print("Visitor para contar folhas está se propagando na árvore")
        node_children = decision_node.get_children()
        node_children[0].accept(self)
        node_children[1].accept(self)

    def visit_leaf_node(self, leaf_node: DecisionNode) -> None:
        self._leaf_count += 1
    
