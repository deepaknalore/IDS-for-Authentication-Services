import grpc

import auth_history_pb2
import auth_history_pb2_grpc

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
    responses = stub.GetBlockListCount(generate_messages())
    print(responses.count)
    return responses.count

def get_allow_count(stub):
    responses = stub.GetAllowListCount(generate_messages())
    print(responses.count)
    return responses.count


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = auth_history_pb2_grpc.AuthHistoryStub(channel)
        print("-------------- GetFeature --------------")
        ac = get_allow_count(stub)
        print("-------------- ListFeatures --------------")
        bc = get_block_count(stub)
        if bc > ac:
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
        else:
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

if __name__ == '__main__':
    run()