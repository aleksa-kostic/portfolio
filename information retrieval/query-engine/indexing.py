# indexing.py

class IndexNode:
    def __init__(self,
                 val,
                 is_head=False,
                 next_node=None,
                 parent=None):
        """

        :param val: tuple
        :param is_head: bool
        :param next_node: IndexNode
        :param parent: IndexNode
        """
        self.ishead = is_head
        self.value = val
        self.nextNode = next_node
        self.parent = parent

    def setNext(self, next_node):
        """

        :param next_node: IndexNode
        :return: None
        """
        self.nextNode = next_node

    def getValue(self):
        """

        :return: tuple
        """
        return self.value

    def getNext(self):
        """

        :return: IndexNode
        """
        return self.nextNode

    def setNext(self, new_next):
        """

        :param new_next: IndexNode
        :return: None
        """
        self.nextNode = new_next

    def getParent(self):
        """

        :return: IndexNode
        """
        return self.parent

    def isHead(self):
        """

        :return: bool
        """
        return self.ishead

    def setIsHead(self, val):
        """

        :param val: bool
        :return: None
        """
        self.ishead = val

    def setParent(self, new_parent):
        """

        :param new_parent: IndexNode
        :return: None
        """
        self.parent = new_parent

    def getDocument(self):
        """

        :return: str
        """
        if self.value is not None:
            return self.value[0]

    def getFrequency(self):
        """

        :return: int
        """
        if self.value is not None:
            return self.value[1]


class PostingLinkedList:
    def __init__(self, head_node=None, tail_node=None):
        """

        :param head_node: IndexNode
        :param tail_node: IndexNode
        """
        self.size = 0
        self.head = head_node
        self.tail = tail_node

    def add(self, next_node):
        """
        Insert new IndexNode
        :param next_node: IndexNode
        :return: None
        """
        if self.head is None:
            self.head = next_node
            next_node.setIsHead(True)
            self.tail = next_node
            self.size += 1
        else:
            self.tail.setNext(next_node)
            next_node.setParent(self.tail)
            self.tail = next_node
            self.size += 1

    def contains_node(self, node_check):
        """
        Check if a node is in this Posting Linked List
        :param node_check: IndexNode
        :return: bool
        """
        current = self.head
        while current is not None:
            if current == node_check:
                return True
            else:
                current = current.getNext()
        return False

    def contains_tuple(self, tuple_check):
        """
        Check if a specific value of a IndexNode is in this Posting Linked List
        :param tuple_check: tuple
        :return: bool
        """
        current = self.head
        while current is not None:
            if current.getValue == tuple_check:
                return True
            else:
                current = current.getNext()
        return False

    def contains_document(self, doc_check):
        """
        Check if a document (path) is included somewhere in this Posting Linked List
        :param doc_check: str
        :return: bool
        """
        current = self.head
        while current is not None:
            if current.getDocument() == doc_check:
                return True
            else:
                current = current.getNext()
        return False


    #
    # def remove_term(self, term_check):
    #     if self.contains(value_check):
    #         current = self.head
    #         while current is not None:
    #             if current.getValue() == value_check:
    #                 if current.getNext() is not None and not current.isHead():
    #                     current.getParent().setNext(current.getNext())
    #                     current.getNext().setParent(current.getParent())
    #                 elif current.getNext() is not None and current.isHead():
    #                     current.getNext().setParent(None)
    #                     current.getNext().setIsHead(True)
    #                     self.head = current.getNext()
    #                 elif current.getNext() is None:
    #                     current.getParent().setNext(None)
    #                     self.tail = current.getParent()
    #                 self.size -= 1
    #         raise IndexError(f"value_check not in linked list. \nCheck PostingLinkedList.contains(value_check) function.\n Value:{value_check}")

    def __len__(self):
        """

        :return: int
        """
        return self.size

    # def __sizeof__(self):
    #     return self.__sizeof__()


class InvertedIndex:
    def __init__(self):
        """
        This is the inverted index. It is simply a dictionary whose values
        are PostingLinkedList types.
        """
        self._invertedIndex = dict()

    def __setitem__(self, term, values):
        """

        :param term: str
        :param values: tuple
        :return: None
        """
        to_insert = IndexNode(values)

        if term not in self._invertedIndex:
            self._invertedIndex[term] = PostingLinkedList()
            self._invertedIndex[term].add(to_insert)

        else:
            self._invertedIndex[term].add(to_insert)

    def __getitem__(self, term):
        """

        :param term: str
        :return: PostingLinkedList
        """
        if term in self._invertedIndex:
            return self._invertedIndex[term]
        else:
            return None






