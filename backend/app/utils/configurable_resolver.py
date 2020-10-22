import logging

from connexion import Resolver, utils, Resolution


class ConfigurableResolver(Resolver):
    def __init__(self, function_resolver=utils.get_function_from_name, operation_prefix=''):
        """
        Standard resolver

        :param function_resolver: Function that resolves functions using an operationId
        :type function_resolver: types.FunctionType
        :param operation_prefix: prefix added to each operation
        :type operation_prefix: str
        """
        super().__init__(function_resolver)
        self.operation_prefix = operation_prefix

    def resolve(self, operation):
        """
        Default operation resolver

        :type operation: connexion.operations.AbstractOperation
        """
        operation_id = self.operation_prefix + self.resolve_operation_id(operation)
        logging.debug('operation id: %s', operation_id)
        return Resolution(self.resolve_function_from_operation_id(operation_id), operation_id)
