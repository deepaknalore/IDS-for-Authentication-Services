import grpc

import auth_history_pb2
import auth_history_pb2_grpc

import datetime

LATENCY_B = 0
LATENCY_A = 0
LATENCY_PUT = 0
BW_B = 0
BW_A = 0
BW_PUT = 0
LIMIT = 1000

# Status - 0 = Allowed, 1 = Failed, 2 = Blocked

def generate_messages():
    return auth_history_pb2.AuthRequest(
        user = 'abcd',
        password = 'abcd',
        ip = '1.1.1.1',
        cookie = 0,
        redirect = 0,
        os = 'abcd',
        browser = 'abcd',
        parameters = 'ip',
        threshold = 2
    )

def get_block_count(stub):
    global LATENCY_B
    a = datetime.datetime.now()
    responses = stub.GetBlockListCount(generate_messages())
    b = datetime.datetime.now()
    LATENCY_B += (b - a).microseconds
    return responses.count

def get_allow_count(stub):
    global LATENCY_A
    a = datetime.datetime.now()
    responses = stub.GetAllowListCount(generate_messages())
    b = datetime.datetime.now()
    LATENCY_A += (b - a).microseconds
    return responses.count


def run():
    global LATENCY_PUT
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = auth_history_pb2_grpc.AuthHistoryStub(channel)
        ac = get_allow_count(stub)
        bc = get_block_count(stub)
        if bc > ac:
            a = datetime.datetime.now()
            stub.PutAuthEntry(auth_history_pb2.AuthRequest(
                                user = 'abcd',
                                password = 'abcd',
                                ip = '1.1.1.1',
                                cookie = 0,
                                redirect = 0,
                                os = 'abcd',
                                browser = 'abcd',
                                parameters = 'ip',
                                threshold = 2,
                                status = 1
                                ))
            b = datetime.datetime.now()
            LATENCY_PUT += (b - a).microseconds
        else:
            a = datetime.datetime.now()
            stub.PutAuthEntry(auth_history_pb2.AuthRequest(
                user='abcd',
                password='abcd',
                ip='1.1.1.1',
                cookie=0,
                redirect=0,
                os='abcd',
                browser='abcd',
                parameters='ip',
                threshold=2,
                status=0
            ))
            b = datetime.datetime.now()
            LATENCY_PUT += (b - a).microseconds

if __name__ == '__main__':
    for i in range(LIMIT):
        run()
    print("Latency for Get Allow List Count: " + str(LATENCY_A/LIMIT))
    print("Latency for Get Block List Count: " + str(LATENCY_B / LIMIT))
    print("Latency for Put: " + str(LATENCY_PUT / LIMIT))
    print("Througphut for Get Allow List Count: " + str(LIMIT*1000000/LATENCY_A))
    print("Througphut for Get Block List Count: " + str(LIMIT * 1000000 / LATENCY_B))
    print("Througphut for PUT: " + str(LIMIT * 1000000 / LATENCY_PUT))