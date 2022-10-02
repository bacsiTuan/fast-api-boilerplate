import grpc # noqa
from py_header_lib.grpc_services.common.proto.ping_pb2_grpc import APIPingStub
from py_header_lib.grpc_services.common.proto.ping_pb2 import PingRequest

channel = grpc.insecure_channel("localhost:6001")
client = APIPingStub(channel)
request = PingRequest(request="ping")
a = client.Ping(request)
print(a)