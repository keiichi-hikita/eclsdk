# -*- coding: utf-8 -*-

from ecl.provider_connectivity.v1 import aws_connection as _aws_connection
from ecl.provider_connectivity.v1 import exchange_point as _exchange_point
from ecl.provider_connectivity.v1 import operation as _operation
from ecl.provider_connectivity.v1 import tenant_connection_request as _tc_request
from ecl.provider_connectivity.v1 import tenant_connection as _tenant_connection
from ecl.provider_connectivity.v1 import address_assignment as _addr_assignment
from ecl import proxy2


class Proxy(proxy2.BaseProxy):

    def aws_connections(self, **params):
        """List connection resource between ECL2.0 and AWS.

        :param params: The parameters as query string
            to get connections by specified condition.
        :returns: A list of connection objects
        :rtype: list of :class:`~ecl.provider_connectivity.v1.aws_connection.AWSConnection`
        """
        return list(self._list(_aws_connection.AWSConnection,
                               paginated=False,
                               **params))

    def get_aws_connection(self, connection_id):
        """Show connection resource between ECL2.0 and AWS.

        :param string connection_id: ID of specified connection.
        :return: :class:`~ecl.provider_connectivity.v1.aws_connection.AWSConnection`
        """
        return self._get(_aws_connection.AWSConnection, connection_id)

    def find_aws_connection(self, name_or_id, ignore_missing=False):
        """Find a single connection

        :param name_or_id: The name or ID of a connection.
        :param bool ignore_missing: When set to ``False``
                    :class:`~ecl.exceptions.ResourceNotFound` will be
                    raised when the resource does not exist.
                    When set to ``True``, None will be returned when
                    attempting to find a nonexistent resource.
        :returns: One :class:`~ecl.network.v2.connection.AWSConnection` or None
        """
        return self._find(_aws_connection.AWSConnection,
                          name_or_id,
                          ignore_missing=ignore_missing)

    def update_aws_connection(self, connection, **params):
        """Update connection between ECL2.0 and AWS.

        :param string connection_id: The ID of a connection.
        :attrs \*\*params: Parameters for connection update.

            * string name: Name of connection.
            * string description: Description of connection.
            * string bandwidth: Bandwidth. If you selected BestEffort
                in the qos_type, can update 100 or 1000 Mbps.
                However, in case of Guarantee, this parameter can not update.
        """
        if not isinstance(connection, _aws_connection.AWSConnection):
            connection = self._get_resource(_aws_connection.AWSConnection, connection)
            connection._body.clean()
        return self._update(_aws_connection.AWSConnection, connection, **params)

    def delete_aws_connection(self, connection_id, ignore_missing=False):
        """Delete connection between ECL2.0 and AWS.

        :param connection_id: The ID of a connection.
        :param bool ignore_missing: When set to ``False``
                    :class:`~ecl.exceptions.ResourceNotFound` will be
                    raised when the port does not exist.
                    When set to ``True``, no exception will be set when
                    attempting to delete a nonexistent port.

        :returns: ``None``
        """
        self._delete(_aws_connection.AWSConnection,
                     connection_id,
                     ignore_missing=ignore_missing)

    def prepare_aws_connection(self, aws_account_id, connected_network_address,
                           bandwidth, qos_type, exchange_point_id,
                           name=None, description=None):
        """Create connection between ECL2.0 and AWS.

        :param string aws_account_id: AWS Account ID of owner.
        :param string connected_network_address: Connected network address
            for AWS connectivity.(/28)
        :param string bandwidth: Bandwidth(Mbps). If you choose BestEffort in
            the qos_type, can select 100 or 1000.
            When you select Guarantee, choose from 50 to 500.
        :param string qos_type: QoS type of network.
            You can choose from "BestEffort" or "Guarantee".
        :param string exchange_point_id: ID of exchange_points.
        :param string name: Name of connection.
        :param string description: Description of connection.
        """
        body = {}
        body["aws_account_id"] = aws_account_id
        body["connected_network_address"] = connected_network_address
        body["bandwidth"] = bandwidth
        body["qos_type"] = qos_type
        body["exchange_point_id"] = exchange_point_id
        if name:
            body["name"] = name
        if description:
            body["description"] = description
        return self._create(_aws_connection.AWSConnection, **body)

    def approve_aws_connection(self, connection_id, action):
        """Approve/Disapprove connection between ECL2.0 and AWS.

        :param connection_id: ID of specified connection.
        :param type: Action type. You can choose from "approve" or "disapprove".
        :return: ``None``
        """
        connection = _aws_connection.AWSConnection()
        connection.approve(self.session, connection_id, action)

    def exchange_points(self, **params):
        """List exchange ponts.

        :param params: The parameters as query string
            to get exchange points by specified condition.
        :returns: A list of exchange point objects
        :rtype: list of :class:`~ecl.provider_connectivity.v1.exchange_point.
            ExchangePoint`
        """
        return list(self._list(_exchange_point.ExchangePoint,
                               paginated=False,
                               **params))

    def operations(self, **params):
        """List operations.

        :param params: The parameters as query string
            to get operations by specified condition.
        :returns: A list of operation objects
        :rtype: list of :class:`~ecl.provider_connectivity.v1.operation.
            Operation`
        """
        return list(self._list(_operation.Operation,
                               paginated=False,
                               **params))

    def tenant_connection_requests(self, **query):
        """Return a list of tenant_connection_requests

        :param kwargs query: Query parameter to get tenant_connection_requests.

        :returns: A list of tenant_connection_requests objects
        """

        return list(self._list(
            _tc_request.TenantConnectionRequest, paginated=False, **query))

    def create_tenant_connection_request(self, keystone_user_id,
                                         tenant_id_other, tenant_id,
                                         network_id, **params):
        """

        :param keystone_user_id:
        :param tenant_id_other:
        :param tenant_id:
        :param network_id:
        :param params:
        :return:
        """
        body = {
            "keystone_user_id": keystone_user_id,
            "tenant_id_other": tenant_id_other,
            "tenant_id": tenant_id,
            "network_id": network_id
        }
        if params.get("name"):
            body["name"] = params.get("name")
        if params.get("description"):
            body["description"] = params.get("description")
        if params.get("tags"):
            body["tags"] = params.get("tags")
        return self._create(_tc_request.TenantConnectionRequest, **body)

    def update_tenant_connection_request(self, tenant_connection_request,
                                         **params):
        """

        :param tenant_connection_request:
        :param params:
        :return:
        """

        if not isinstance(tenant_connection_request, _tc_request.TenantConnectionRequest):
            tenant_connection_request = self._get_resource(
                _tc_request.TenantConnectionRequest,
                tenant_connection_request)
            tenant_connection_request._body.clean()
        return self._update(_tc_request.TenantConnectionRequest,
                            tenant_connection_request, **params)

    def delete_tenant_connection_request(self, tenant_connection_request,
                                         ignore_missing=False):
        """

        :param tenant_connection_request:
        :param ignore_missing:
        :return:
        """
        self._delete(_tc_request.TenantConnectionRequest,
                     tenant_connection_request,
                     ignore_missing=ignore_missing)

    def get_tenant_connection_request(self, tenant_connection_request_id):
        """Get a single tenant connection request

        :param tenant_connection_request_id:
                The ID of a tenant connection request

        :returns: One :class:`~ecl.provider_connectivity.v1.
                tenant_connection_request.TenantConnectionRequest` or None
        """
        return self._get(_tc_request.TenantConnectionRequest, tenant_connection_request_id)

    def find_tenant_connection_request(self, name_or_id, ignore_missing=False):
        """Find a single tenant connection request

        :param name_or_id: The name or ID of a tenant connection request.
        :param bool ignore_missing: When set to ``False``
                    :class:`~ecl.exceptions.ResourceNotFound` will be
                    raised when the resource does not exist.
                    When set to ``True``, None will be returned when
                    aittempting to find a nonexistent resource.
        :returns: One :class:`~ecl.provider_connectivity.v1.
                tenant_connection_request.TenantConnectionRequest` or None
        """
        return self._find(_tc_request.TenantConnectionRequest,
                          name_or_id,
                          ignore_missing=ignore_missing)

    def tenant_connections(self, **query):
        """

        :param query:
        :return:
        """
        return list(self._list(_tenant_connection.TenantConnection,
                               paginated=False, **query))

    def get_tenant_connection(self, tenant_connection_id):
        """

        :param tenant_connection_id:
        :return:
        """
        return self._get(_tenant_connection.TenantConnection, tenant_connection_id)

    def create_tenant_connection(self, tenant_connection_request_id, device_type, device_id, **params):
        """

        :param tenant_connection_request_id:
        :param device_type:
        :param device_id:
        :param params:
        :return:
        """
        body = {
            "tenant_connection_request_id": tenant_connection_request_id,
            "device_type": device_type,
            "device_id": device_id,
        }
        if params.get("name"):
            body["name"] = params.get("name")
        if params.get("description"):
            body["description"] = params.get("description")
        if params.get("tags"):
            body["tags"] = params.get("tags")
        if params.get("device_interface_id"):
            body["device_interface_id"] = params.get("device_interface_id")
        if params.get("attachment_opts"):
            body["attachment_opts"] = params.get("attachment_opts")
        return self._create(_tenant_connection.TenantConnection, **body)

    def update_tenant_connection(self, tenant_connection, **params):
        """

        :param tenant_connection:
        :param params:
        :return:
        """
        if not isinstance(tenant_connection, _tenant_connection.TenantConnection):
            tenant_connection = self._get_resource(
                _tenant_connection.TenantConnection,
                tenant_connection)
            tenant_connection._body.clean()
        return self._update(_tenant_connection.TenantConnection,
                            tenant_connection, **params)

    def delete_tenant_connection(self, tenant_connection, ignore_missing=False):
        """

        :param tenant_connection:
        :param ignore_missing:
        :return:
        """
        self._delete(_tenant_connection.TenantConnection,
                     tenant_connection,
                     ignore_missing=ignore_missing)

    def find_tenant_connection(self, name_or_id, ignore_missing=False):
        """Find a single tenant connection

        :param name_or_id: The name or ID of a tenant connection.
        :param bool ignore_missing: When set to ``False``
                    :class:`~ecl.exceptions.ResourceNotFound` will be
                    raised when the resource does not exist.
                    When set to ``True``, None will be returned when
                    attempting to find a nonexistent resource.
        :returns: One :class:`~ecl.provider_connectivity.v1.
                tenant_connection.TenantConnection` or None
        """
        return self._find(_tenant_connection.TenantConnection,
                          name_or_id,
                          ignore_missing=ignore_missing)

    def address_assignments(self, tenant_connection_request_id, **query):
        """

        :param tenant_connection_request:
        :param query:
        :return:
        """
        return list(self._list(_addr_assignment.AddressAssignment,
                               paginated=False,
                               tenant_connection_request_id=tenant_connection_request_id,
                               **query))
