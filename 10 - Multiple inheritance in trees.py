"""
Assignment 10, by Leonardo Blas.
In this assignment we will be optimizing the code for assignment 9, our trees'
programs, by using multiple inheritance.
To minimize the alteration of the code provided, per specs request, we
individually call the parent classes' methods, rather than using an
MRO approach.
"""

# client (as a function) -----------------------------------
import copy


def main():
    """ test the FhSdTree  class """

    # instantiate a "data" tree of strings
    scene_tree = FhSdDataTree(str)

    print("Starting tree empty? " + str(scene_tree.empty()))

    scene_tree.add_child_to_cur("room")

    # add three objects to the scene tree
    scene_tree.find("room")
    scene_tree.add_child_to_cur("Lily the canine")
    scene_tree.add_child_to_cur("Miguel the human")
    scene_tree.add_child_to_cur("table")

    # add some parts to Miguel
    scene_tree.find_in_cur_subtree("Miguel the human")
    scene_tree.add_child_to_cur("torso")

    # Miguel's arms
    scene_tree.find_in_cur_subtree("torso")
    scene_tree.add_child_to_cur("left arm")
    scene_tree.add_child_to_cur("right arm")

    # add things Miguel's left arm (only one in room)
    scene_tree.find("left arm")
    scene_tree.add_child_to_cur("left hand")

    # for variety, we won't label fingers left/right
    scene_tree.find_in_cur_subtree("left hand")
    scene_tree.add_child_to_cur("thumb")
    scene_tree.add_child_to_cur("index finger")
    scene_tree.add_child_to_cur("middle finger")
    scene_tree.add_child_to_cur("ring finger")
    scene_tree.add_child_to_cur("pinky")

    # add things Miguel's right arm (only one in room)
    scene_tree.find("right arm")
    scene_tree.add_child_to_cur("right hand")

    # for variety, we won't label fingers left/right
    scene_tree.find_in_cur_subtree("right hand")
    scene_tree.add_child_to_cur("thumb")
    scene_tree.add_child_to_cur("index finger")
    scene_tree.add_child_to_cur("middle finger")
    scene_tree.add_child_to_cur("ring finger")
    scene_tree.add_child_to_cur("pinky")

    # add some parts to Lily
    scene_tree.find("Lily the canine")
    scene_tree.add_child_to_cur("torso")

    # we are careful to add to Liliy's "torso" not Miguel's
    scene_tree.find_in_cur_subtree("torso")
    scene_tree.add_child_to_cur("right front paw")
    scene_tree.add_child_to_cur("left front paw")
    scene_tree.add_child_to_cur("right rear paw")
    scene_tree.add_child_to_cur("left rear paw")
    scene_tree.add_child_to_cur("spare mutant paw")
    scene_tree.add_child_to_cur("wagging tail")

    # add some parts to table
    scene_tree.find("table")
    scene_tree.add_child_to_cur("north east leg")
    scene_tree.add_child_to_cur("north west leg")
    scene_tree.add_child_to_cur("south east leg")
    scene_tree.add_child_to_cur("south west leg")

    print("\n------------ Loaded Tree --------------- \n", scene_tree)

    # test of deep copy and soft deletion --------------------------
    my_copy = copy.deepcopy(scene_tree)

    # remove some real and imagined parts from original
    scene_tree.remove("spare mutant paw")
    scene_tree.remove("Miguel the human")
    scene_tree.remove("an imagined higgs boson")
    scene_tree.remove("torso")

    print("\n----------- Virtual Tree ------------ \n", scene_tree)
    print("\n----------- Physical Tree ------------ \n",
          scene_tree.str_physical())

    print("\n----------- Miguel and Torso should be gone ------------ \n")
    if scene_tree.find("miguel"):
        print("bad")
    else:
        print("good")

    if scene_tree.find("thumb"):
        print("bad")
    else:
        print("good")

    if scene_tree.find("torso"):
        print("bad")
    else:
        print("good")

    if scene_tree.find("Miguel the human"):
        print(my_copy.find("Miguel the human"))
        print("bad")
    else:
        print("good")

    print("\n------- Testing Sizes (compare with above) ------ \n")
    print("\nvirtual (soft) size:", scene_tree.size())
    print("\nphysical (hard) size:", scene_tree.size_physical())

    print("\n------------ Collecting Garbage ------------ \n")
    print("found soft-deleted nodes?", scene_tree.collect_garbage())
    print("immediate collect again?", scene_tree.collect_garbage())
    print("-------- Hard Display after garb col ----------\n",
          scene_tree.str_physical())

    print("Semi-deleted tree empty? " + str(scene_tree.empty()))
    scene_tree.remove("room")
    print("Completely-deleted tree empty? " + str(scene_tree.empty()))

    print("\n------------ Cloned Tree? ------------ \n")
    # remove and add some parts of copy and compare with original
    my_copy.remove("left rear paw")
    my_copy.find("Miguel the human")
    my_copy.add_child_to_cur("head")
    my_copy.find_in_cur_subtree("torso")
    my_copy.remove_at_cur()

    print("\n----------- Virtual Tree ------------ \n", my_copy)
    print("\n----------- Physical Tree ------------ \n",
          my_copy.str_physical())

    print("\n------- Testing Sizes (compare with above) ------ \n")
    print("\nvirtual (soft) size:", my_copy.size())
    print("\nphysical (hard) size:", my_copy.size_physical())

    print("\n------------ Testing find() ------------ \n")
    if my_copy.find("table"):
        print("good")
    else:
        print("bad")

    if my_copy.find("spare mutant paw"):
        print("good")
    else:
        print("bad")

    if my_copy.find("imagined higgs boson"):
        print("bad")
    else:
        print("good")

    # will find Lily's torso
    if my_copy.find("torso"):
        print("good")
    else:
        print("bad")

    # won't find Miguels's torso
    my_copy.find("Miguel the Human")
    if my_copy.find_in_cur_subtree("torso"):
        print("bad")
    else:
        print("good")

    #  remove Lily, and search for torso  (should fail)
    my_copy.find("Lily the canine")
    my_copy.remove_at_cur()
    if my_copy.find("torso"):
        print("bad")
    else:
        print("good")

    if my_copy.find("pinky"):
        print("bad")
    else:
        print("good")


# END CLIENT main()  -------------------------------------------
# BEGIN CLASS FhTreeNode -------------------------------------------
class FhTreeNode:
    """ FhTreeNode class for a FhTree - not designed for
        general clients, so no accessors or exception raising """

    # initializer ("constructor") method ------------------------
    def __init__(self,
                 sib=None, first_child=None, prev=None,
                 root=None):
        # instance attributes
        self.sib, self.first_child, self.prev, self.my_root \
            = sib, first_child, prev, root

    # stringizer ----------------------------------------------
    def __str__(self):
        return "(generic tree node)"


# END CLASS FhTreeNode -------------------------------------------
# BEGIN CLASS FhTree -------------------------------------------
class FhTree:
    """ FhTree is our base class for a data-filled general trees """

    # static constant helpers for stringizer
    BLANK_STRING = "                                    "
    BLANK_STR_LEN = len(BLANK_STRING)

    # constructor ------------------------------------------------
    def __init__(self):
        self.clear()

    # accessors --------------------------------------------------
    def empty(self):
        """ traditionally, is_empty() is just called empty() """
        return (self.size() == 0)

    def size(self):
        """ traditionally, get() for size is just siae() """
        return self.m_size

    # current pointer mutators --------------------------------------
    def reset_cur(self):
        self.current = self.m_root

    def set_cur(self, tree_node):
        if not self.valid_node_in_tree(tree_node):
            self.current = None
            return False
        # else
        self.current = tree_node
        return True

    # tree mutators --------------------------------------------------
    def clear(self):
        self.m_root = None
        self.m_size = 0
        self.reset_cur()

    def remove_node_rec(self, node_to_delete):
        """ node_to_delete points to node in tree to be removed
            (along w/entire subtree). deletes children recursively
            errors handled by caller (remove_at_cur()) """

        ntd = node_to_delete  # alias for shorter lines
        # remove all the children of this node (need loop unfortunately)
        while ntd.first_child:
            self.remove_node_rec(ntd.first_child)

        # we have a non-null prev pointer
        # either it has a left sib ...
        if ntd.prev.sib == node_to_delete:
            ntd.prev.sib = node_to_delete.sib
        # ... or it's the first_child of some parent
        else:
            ntd.prev.first_child = ntd.sib

        # deal with a possible right sib
        if ntd.sib != None:
            ntd.sib.prev = ntd.prev

        # node is now out of the tree (Python will g.c. if appropriate)
        # wipe the fields to prevent client from doing harm
        ntd.first_child, ntd.prev, ntd.sib, ntd.my_root \
            = None, None, None, None

        # finally, update tree size
        self.m_size -= 1

    def remove_at_cur(self):
        """ calls remove_node() passing cur, and resets cur
           handles all errors here to avoid repetition in rec call """

        ntd = self.current  # saves cur so we can reset early
        self.reset_cur()  # no matter what, we'll return fresh cur

        # bad current or empty tree
        if not self.valid_node_in_tree(ntd) or self.size() == 0:
            return False

        # deleting root?
        if ntd.prev == None:
            self.clear()
            return True

        # since we know this node is in tree, call will succeed
        self.remove_node_rec(ntd)
        return True

    def add_child_node_to_cur(self, to_add=None):
        """ 'push' node_to_add as new first child of parent.
             return None (error) or ref to newly created node
             expect parent == None IFF tree is empty """

        if not self.valid_node_to_add(to_add):
            return False

        # empty tree
        if self.m_size == 0:
            self.m_root = to_add
            self.m_root.my_root = self.m_root
            self.m_size = 1
            self.reset_cur()  # for empty tree we ignore what cur *was*
            return True

        if not self.valid_node_in_tree(self.current):
            return False

        # "push" new_node as the head of the sibling list; adjust all ptrs
        # notice "None": any "subtree: hanging off to_add, is trimmed
        cur = self.current  # for brevity...
        ta = to_add  # ... of next block

        ta.sib, ta.first_child, ta.prev, ta.my_root \
            = cur.first_child, None, cur, self.m_root
        cur.first_child = ta
        if ta.sib != None:
            ta.sib.prev = ta
        self.m_size += 1
        return True

    # stringizers ------------------------------------------------
    def __str__(self):
        ret_str = "The Tree -----------------------\n" \
                  + self.str_recurse(self.m_root, 0) \
                  + "---------- End of Tree --------\n"

        return ret_str

    def str_recurse(self, tree_node, level=0):
        """ recursive tree stringizer (with indentation)
            for subtree with root tree_node in this instance's tree """

        ret_str = ""

        # multi-purpose termination:  error, None or not-in-self
        if not self.valid_node_in_tree(tree_node):
            return ret_str

        # stop runaway indentation, otherwise set indent for this level
        if level > self.BLANK_STR_LEN - 1:
            return self.BLANK_STRING + " ... "

        # this call's node
        indent = self.BLANK_STRING[0:level]
        ret_str += (indent + str(tree_node) + "\n")

        # recurse over children
        ret_str += self.str_recurse(tree_node.first_child, level + 1)

        # recurse over siblings
        if level > 0:
            ret_str += self.str_recurse(tree_node.sib, level)

        return ret_str

    # helpers ---------------------------------------
    def valid_node_to_add(self, am_i_valid):
        """ insists that node is an FhTreeNode """
        if (not isinstance(am_i_valid, FhTreeNode)):
            return False
        return True

    def valid_node_in_tree(self, am_i_valid):
        """ insists that node is an FhTreeNode AND in this tree """
        if (not isinstance(am_i_valid, FhTreeNode)) \
                or (am_i_valid.my_root != self.m_root):
            return False
        return True
    # END CLASS FhTree ----------------------------------------


# BEGIN CLASS FhDataTreeNode ----------------------------------------
class FhDataTreeNode(FhTreeNode):
    """ FhDataTreeNode subclass of FhTreeNode.
    It is the node class for a data tree.
    Requires data item, x, be vetted by client (FhDataTree) """

    # constructor ------------------------------------------------
    def __init__(self, x,
                 sib=None, first_child=None, prev=None,
                 root=None):
        # first chain to base class
        super().__init__(sib, first_child, prev, root)

        # added attribute
        self.data = x

    # stringizer(s) ----------------------------------------------
    # ultimate client, main(), can provide data stringizer if needed
    def __str__(self):
        return str(self.data)


# END CLASS FhDataTreeNode ----------------------------------------
# BEGIN CLASS FhDataTree ----------------------------------------
class FhDataTree(FhTree):
    """ FhDataTree subclass of FhTree """
    # default type is string
    DEFAULT_TYPE = type("")

    # constructor -----------------------------------------------
    def __init__(self, tree_type=None):
        super().__init__()
        self.set_tree_type(tree_type)

    # current pointer mutators --------------------------------------
    def find(self, x):
        """ look for x in entire tree.
            if found and valid, current will point to it and return T,
            else current None and return F (all done by find_rec())"""

        self.reset_cur()
        return self.find_in_cur_subtree(x)

    def find_in_cur_subtree(self, x):
        """ look for x in subtree rooted at self.current.
           if x valid and found, current will point to it and return T,
           else current None and return F """

        if not self.current or not self.valid_data(x):
            return False

        return (self.find_rec(x, self.current) != None)

    def find_rec(self, x, root):
        """ recursively search for x in subtree rooted at root.
           if found, current set to node and returned,
           else current/return = None.
           x and current vetted by non-recursive originator """

        # default current if all recursive calls fail
        self.current = None

        # not found (in this sub-search)
        if not root:
            return None

        # found (current will survive all higher-level calls)
        if root.data == x:
            self.current = root
            return root

        # recurse children
        child = root.first_child
        while child:
            test_result = self.find_rec(x, child)
            if test_result:
                return test_result
            child = child.sib

        return None

    # tree mutators --------------------------------------------------
    def set_tree_type(self, the_type):
        # make sure it's a subclass of type
        if isinstance(the_type, type):
            self.tree_type = the_type
        else:
            self.tree_type = self.DEFAULT_TYPE

    def remove(self, x):
        """ looks for x in entire tree.
           if valid and found, remove node, return T (cur reset by base
           call, remove_at_cur()). else curr = None and return F """

        self.current = None  # prepare for not found or error return
        if self.size() == 0 or (not self.valid_data(x)):
            return False

        found_node = self.find_rec(x, self.m_root)
        if not found_node:
            return False

        # found x
        self.current = found_node
        self.remove_at_cur()  # not overriden, so base call
        return True

    def add_child_to_cur(self, x):
        """ calls base add_child_node_to_cur(). no change to cur """
        if not self.valid_data(x):
            return False

        new_node = FhDataTreeNode(x)
        return (super().add_child_node_to_cur(new_node))

    # helpers -------------------------------------------------
    def valid_data(self, am_i_valid):
        if not isinstance(am_i_valid, self.tree_type):
            return False
        # else
        return True


# ------------------------------------------------------------------------------

# cs 3B, assignment 10 Starter


# BEGIN CLASS FhSdTreeNode -------------------------------------------
class FhSdTreeNode(FhTreeNode):
    """ FhSdTreeNode class for a FhSdTree - adds dltd flag """

    # initializer ("constructor") method ------------------------
    def __init__(self,
                 sib=None, first_child=None, prev=None,
                 root=None, dltd=False):
        super().__init__(sib, first_child, prev, root)
        # subclass instance attributes
        self.dltd = dltd


# END CLASS FhSdTreeNode -------------------------------------------
# BEGIN CLASS FhSdTree -------------------------------------------
class FhSdTree(FhTree):
    """ FhSdTree, derived from FhTree, is our base class for lazy deletion
       general trees """

    # constructor ------------------------------------------------
    # inherited
    # accessors --------------------------------------------------
    def empty(self):
        """ overridden to call new size() since m_size is physical """
        return (self.size() == 0)

    def size_physical(self):
        """ new name for base class size() method. returns size of all
            nodes, inc. deleted """
        return super().size()

    def size(self):
        """ overridden to compute the size rather than rely on m_size """
        return self.size_rec(self.m_root)

    def size_rec(self, tree_node, level=0):
        """ added -- recursively computes size of subtree
           with root tree_node """
        if not self.m_root or not tree_node:
            return 0

        sib_size, count_this, children_size = 0, 0, 0
        # count siblings
        if level > 0:
            sib_size = self.size_rec(tree_node.sib, level)

        # a deleted node cuts off its entire subtree
        if not tree_node.dltd:
            children_size = self.size_rec(tree_node.first_child, level + 1)
            count_this = 1

        return children_size + sib_size + count_this

    # current pointer mutators --------------------------------------
    # reset_cur() inherited
    def set_cur(self, tree_node):
        """ overridden.  add test for soft deleted """
        if not self.valid_node_in_tree(tree_node) or tree_node.dltd:
            self.current = None
            return False
        # else
        self.current = tree_node
        return True

    # tree mutators --------------------------------------------------
    # clear() inherited
    def collect_garbage(self):
        """ new.  physically deletes all marked nodes in tree.
            True if anything removed, False if not. """
        return self.collect_garbage_rec(self.m_root)

    def collect_garbage_rec(self, tree_node):
        """ new. recursively deletes all marked nodes in subtree tree_node """
        if not self.m_root or not tree_node:
            return False

        sib_result, this_result, children_result = False, False, False

        # collect sib garbage (must do before root removed)
        sib_result = self.collect_garbage_rec(tree_node.sib)
        if tree_node.dltd:
            self.remove_node_rec(tree_node)  # will remove all children
            this_result = True
        else:
            # if root not deleted, must remove children manually
            children_result = self.collect_garbage_rec(tree_node.first_child)

        # if anything was deleted, return True
        return sib_result or children_result or this_result;

    # remove_node_rec() inherited
    def remove_at_cur(self):
        """ overridden to mark self.current's del flag and chk current dltd
            but if this is the root node, we can do a physical clear() """

        ntd = self.current  # saves cur so we can reset early
        self.reset_cur()  # no matter what, we'll return fresh cur

        # bad current, empty tree or already soft delted
        if not self.valid_node_in_tree(ntd) or (self.size() == 0) \
                or ntd.dltd:
            return False

        # deleting root?  we will do total gc and start fresh
        if ntd.prev == None:
            self.clear()
            return True

        # don't need recursive helper in this method - just soft delete
        ntd.dltd = True
        return True

    def add_child_node_to_cur(self, to_add=None):
        """ overridden to make sure to_add goes in non-deleted """

        # be sure  to_add is lazy-delection type
        if not self.valid_node_to_add(to_add):
            return False

        to_add.dltd = False  # just in case del flag was True
        return super().add_child_node_to_cur(to_add)

    # stringizers ------------------------------------------------
    # __str__() inherited
    def str_recurse(self, tree_node, level=0):
        """ overridden to skip soft deleted nodes and their children """
        ret_str = ""

        # multi-purpose termination:  error, None or not-in-self
        if not self.valid_node_in_tree(tree_node):
            return ret_str

        # stop runaway indentation, otherwise set indent for this level
        if level > self.BLANK_STR_LEN - 1:
            return self.BLANK_STRING + " ... "

        # this call's node
        if not tree_node.dltd:
            indent = self.BLANK_STRING[0:level]
            ret_str += (indent + str(tree_node) + "\n")

            # recurse over children
            ret_str += self.str_recurse(tree_node.first_child, level + 1)

        # recurse over siblings
        if level > 0:
            ret_str += self.str_recurse(tree_node.sib, level)

        return ret_str

    def str_physical(self):
        """ added.  client version of new stringizer showing dltd nodes """
        ret_str = "The Tree (including soft-deleted nodes ----\n" \
                  + self.str_recurse_phys(self.m_root, 0) \
                  + "---------- End of Tree --------\n"

        return ret_str

    def str_recurse_phys(self, tree_node, level=0):
        """ added - like old str_recurse, but with (D) tag added """
        ret_str = ""

        # multi-purpose termination:  error, None or not-in-self
        if not self.valid_node_in_tree(tree_node):
            return ret_str

        # stop runaway indentation, otherwise set indent for this level
        if level > self.BLANK_STR_LEN - 1:
            return self.BLANK_STRING + " ... "
        indent = self.BLANK_STRING[0:level]

        # this call's node
        if not tree_node.dltd:
            ret_str += (indent + str(tree_node) + "\n")
        else:
            ret_str += (indent + str(tree_node) + " (D)\n")

        # recurse over children
        ret_str += self.str_recurse_phys(tree_node.first_child, level + 1)

        # recurse over siblings
        if level > 0:
            ret_str += self.str_recurse_phys(tree_node.sib, level)

        return ret_str

    # helpers ---------------------------------------
    def valid_node_to_add(self, am_i_valid):
        """ insists that node is an FhSdTreeNode """
        if (not isinstance(am_i_valid, FhSdTreeNode)):
            return False
        return True

    def valid_node_in_tree(self, am_i_valid):
        """ unchanged - soft-deleted is considered valid """
        if (not isinstance(am_i_valid, FhSdTreeNode)) \
                or (am_i_valid.my_root != self.m_root):
            return False
        return True
    # END CLASS FhSdTree ------------------------------------------------


# FhSdDataTreeNode -------------------------------------------------------------
class FhSdDataTreeNode(FhDataTreeNode, FhSdTreeNode):
    """ FhSdDataTreeNode subclass of FhSdTreeNode.
    It is the node class for a data tree.
    Requires data item, x, be vetted by client (FhSdDataTree) """

    def __init__(self, x,
                 sib=None,
                 first_child=None,
                 prev=None,
                 root=None,
                 dltd=False):
        # first chain to base class
        FhDataTreeNode.__init__(self, x, sib, first_child, prev, root)
        FhSdTreeNode.__init__(self, dltd=dltd)

    # ultimate client, main(), can provide data stringizer if needed
    def __str__(self):
        return FhDataTreeNode.__str__(self)


class FhSdDataTree(FhSdTree, FhDataTree):
    """ FhSdDataTree subclass of FhSdTree """

    def __init__(self, tree_type=None):
        FhSdTree.__init__(self)
        FhDataTree.__init__(self, tree_type)

    def add_child_to_cur(self, x):
        """ calls base add_child_node_to_cur(). no change to cur """
        if not self.valid_data(x):
            return False
        new_node = FhSdDataTreeNode(x)
        return (super().add_child_node_to_cur(new_node))

    def find_rec(self, x, root):
        """ recursively search for x in subtree rooted at root.
           if found, current set to node and returned,
           else current/return = None.
           x and current vetted by non-recursive originator """
        # default current if all recursive calls fail
        self.current = None
        # not found (in this sub-search)
        if root and not root.dltd:
            # found (current will survive all higher-level calls)
            if root.data == x:
                self.current = root
                return root
            # recurse children
            child = root.first_child
            while child:
                test_result = self.find_rec(x, child)
                if test_result:
                    return test_result
                child = child.sib
        return None

    def find_in_cur_subtree(self, x):
        """ look for x in subtree rooted at self.current.
           if x valid and found, current will point to it and return T,
           else current None and return F """
        if not self.current or not self.valid_data(x):
            return False
        return self.find_rec(x, self.current) is not None


# -------------- main program -------------------
if __name__ == "__main__":
    main()

""" -------------------------- RUN ----------------------------

True
True
True
False

ORIGNIAL, after removing miguel and the mutant paw 
and adding fruit,  person to view fruit and #2 pencil:
The Tree -----------------------
room
 person viewing fruit
 table
  #2 pencil
  fruit bowl
  south west leg
  south east leg
  north west leg
  north east leg
 Lily the canine
  torso
   wagging tail
   left rear paw
   right rear paw
   left front paw
   right front paw
---------- End of Tree --------

COPY, after removing miguel's torso and Lily's left rear
and adding vase and person to view vase:
The Tree -----------------------
room
 person viewing vase
 table
  vase
  south west leg
  south east leg
  north west leg
  north east leg
 Miguel the human
  head
 Lily the canine
  torso
   wagging tail
   spare mutant paw
   right rear paw
   left front paw
   right front paw
---------- End of Tree --------


-------------------------------------------------------------- """
