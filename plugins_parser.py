import pluginlib

@pluginlib.Parent('plugin_common', group='msg_plugin')
class plugin_common(object):

    # @staticmethod
    # def pluginbaseinfo():
    #     pass
    @classmethod
    @pluginlib.abstractmethod
    def main(cls,msg_l):
        pass

@pluginlib.Parent('plugin_admin', group='msg_plugin')
class plugin_admin(object):

    # @staticmethod
    # def pluginbaseinfo():
    #     pass
    @classmethod
    @pluginlib.abstractmethod
    def main(cls,msg_l):
        pass


@pluginlib.Parent('replace_static', group='msg_replace')
class replace_static(object):

    # @staticmethod
    # def pluginbaseinfo():
    #     pass

    @pluginlib.abstractmethod
    def replace(self, msg_l):
        pass


@pluginlib.Parent('replace_dynamic', group='msg_replace')
class replace_dynamic(object):

    # @staticmethod
    # def pluginbaseinfo():
    #     pass

    @pluginlib.abstractmethod
    def replace_main(self, msg_l):
        pass