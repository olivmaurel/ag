from ag.actions.actions import Action
from ag.task_behavior.branch import Selector
from ag.task_behavior.tree import NodeStatus


class DrinkAction(Action):

    def execute(self):
        pass
        # check inventory
        # if liquid container in inventory
        # take container
        # if liquid is drinkable
        # do drink it



class DrinkSelector(Selector):
    """ When an entity decides to drink,
        successive actions to access a source of water and drink from it
    """

    def __init__(self, name='drink', *args, **kwargs):
        """ User-facing initialization
            @param name [str] The human-readable name to aid in debugging
        """
        super(Selector, self).__init__(
            name,
            run_cb=self.run,
            configure_cb=self.configure,
            cleanup_cb=self.cleanup,
            *args, **kwargs)

    def configure(self, nodedata):
        """ Initialize the start and limit values
            @param nodedata [NodeData] The shareable data associated with this node
            NodeData:
                start [int] The number the count should start on
                limit [int] The number the count sound end on
        """
        self.start = nodedata.get_data('start', 0)
        self.limit = nodedata.get_data('limit', 5)
        nodedata.index = self.start

    def run(self, nodedata):
        """ Update the count and return current status.
            @param nodedata [NodeData] The shareable data associated with this node
            NodeData:
                index [int] The current index of the count
        """
        if nodedata.index < self.limit:
            nodedata.index += 1
            return NodeStatus(NodeStatus.ACTIVE, "Count " + str(nodedata.index))
        return NodeStatus(NodeStatus.SUCCESS, "Count finished at " + str(nodedata.index))

    def cleanup(self, nodedata):
        """ Reset the count to start
            @param nodedata [NodeData]
            NodeData:
                index [int] The current index of the count
        """
        nodedata.index = self.start