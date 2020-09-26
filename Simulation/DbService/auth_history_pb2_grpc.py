# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import auth_history_pb2 as auth__history__pb2


class AuthHistoryStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetAllowListCount = channel.unary_unary(
                '/AuthHistory/GetAllowListCount',
                request_serializer=auth__history__pb2.AuthRequest.SerializeToString,
                response_deserializer=auth__history__pb2.AllowListCount.FromString,
                )
        self.GetBlockListCount = channel.unary_unary(
                '/AuthHistory/GetBlockListCount',
                request_serializer=auth__history__pb2.AuthRequest.SerializeToString,
                response_deserializer=auth__history__pb2.BlockListCount.FromString,
                )
        self.PutAuthEntry = channel.unary_unary(
                '/AuthHistory/PutAuthEntry',
                request_serializer=auth__history__pb2.AuthRequest.SerializeToString,
                response_deserializer=auth__history__pb2.Empty.FromString,
                )


class AuthHistoryServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetAllowListCount(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetBlockListCount(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def PutAuthEntry(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_AuthHistoryServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetAllowListCount': grpc.unary_unary_rpc_method_handler(
                    servicer.GetAllowListCount,
                    request_deserializer=auth__history__pb2.AuthRequest.FromString,
                    response_serializer=auth__history__pb2.AllowListCount.SerializeToString,
            ),
            'GetBlockListCount': grpc.unary_unary_rpc_method_handler(
                    servicer.GetBlockListCount,
                    request_deserializer=auth__history__pb2.AuthRequest.FromString,
                    response_serializer=auth__history__pb2.BlockListCount.SerializeToString,
            ),
            'PutAuthEntry': grpc.unary_unary_rpc_method_handler(
                    servicer.PutAuthEntry,
                    request_deserializer=auth__history__pb2.AuthRequest.FromString,
                    response_serializer=auth__history__pb2.Empty.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'AuthHistory', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class AuthHistory(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetAllowListCount(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/AuthHistory/GetAllowListCount',
            auth__history__pb2.AuthRequest.SerializeToString,
            auth__history__pb2.AllowListCount.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetBlockListCount(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/AuthHistory/GetBlockListCount',
            auth__history__pb2.AuthRequest.SerializeToString,
            auth__history__pb2.BlockListCount.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def PutAuthEntry(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/AuthHistory/PutAuthEntry',
            auth__history__pb2.AuthRequest.SerializeToString,
            auth__history__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
