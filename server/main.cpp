
#include <grpc/grpc.h>
#include <grpcpp/security/server_credentials.h>
#include <grpcpp/server.h>
#include <grpcpp/server_builder.h>
#include <grpcpp/server_context.h>
#include "simplegrpcble.grpc.pb.h"

class SimpleGRPCBleImpl final : public simplegrpcble::SimpleGRPCBLE::Service {
  public:
};

void RunServer() {
    std::string server_address("0.0.0.0:50051");
    SimpleGRPCBleImpl service;

    grpc::ServerBuilder builder;
    builder.AddListeningPort(server_address, grpc::InsecureServerCredentials());
    builder.RegisterService(&service);
    std::unique_ptr<grpc::Server> server(builder.BuildAndStart());
    std::cout << "Server listening on " << server_address << std::endl;
    server->Wait();
}

int main(int argc, char** argv) {
    RunServer();

    return 0;
}
