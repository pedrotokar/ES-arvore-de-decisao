from abc import ABC, abstractmethod

# Árvore (com o padrão composite)
class Node(ABC):
    pass

class DecisionNode(Node):
    pass

class LeafNode(Node):
    pass

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
