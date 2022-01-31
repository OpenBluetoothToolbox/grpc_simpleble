
#include <grpc/grpc.h>
#include <grpcpp/security/server_credentials.h>
#include <grpcpp/server.h>
#include <grpcpp/server_builder.h>
#include <grpcpp/server_context.h>
#include "simplegrpcble.grpc.pb.h"

#include <iostream>

class SimpleGRPCBleImpl final : public simplegrpcble::SimpleGRPCBLE::Service {
  public:
    explicit SimpleGRPCBleImpl() {}

    grpc::Status GetAdapters(grpc::ServerContext* context, simplegrpcble::Empty const*,
                             simplegrpcble::AdapterList* response) override {
        std::cout << "GetAdapters" << std::endl;

        simplegrpcble::Adapter* adapter = response->add_adapters();
        adapter->set_identifier("Adapter1");
        adapter->set_address("00:00:00:00:00:00");
        adapter->set_id(0);

        adapter = response->add_adapters();
        adapter->set_identifier("Adapter2");
        adapter->set_address("00:00:00:00:00:02");
        adapter->set_id(1);

        return grpc::Status::OK;
    }

    grpc::Status AdapterScanStart(grpc::ServerContext* context, simplegrpcble::AdapterId const* adapter_id,
                                  simplegrpcble::Empty* response) override {
        std::cout << "AdapterScanStart" << std::endl;
        return grpc::Status::OK;
    }

    grpc::Status AdapterScanStop(grpc::ServerContext* context, simplegrpcble::AdapterId const* adapter_id,
                                 simplegrpcble::Empty* response) override {
        std::cout << "AdapterScanStop" << std::endl;
        return grpc::Status::OK;
    }

    grpc::Status AdapterScanIsActive(grpc::ServerContext* context, simplegrpcble::AdapterId const* adapter_id,
                                     simplegrpcble::Bool* response) override {
        std::cout << "AdapterScanIsActive" << std::endl;
        return grpc::Status::OK;
    }

    grpc::Status AdapterScanGetResults(grpc::ServerContext* context, simplegrpcble::AdapterId const* adapter_id,
                                       simplegrpcble::DeviceList* response) override {
        std::cout << "AdapterScanResults" << std::endl;

        simplegrpcble::Device* device = response->add_devices();
        device->set_identifier("Device1");
        device->set_address("00:00:00:00:00:01");
        device->set_id(0);
        device->set_is_connectable(true);
        device->mutable_manufacturer_data()->insert({0x01, "FIELD1"});
        device->mutable_manufacturer_data()->insert({0x02, "FIELD2"});

        return grpc::Status::OK;
    }
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
