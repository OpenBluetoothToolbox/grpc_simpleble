import grpc
import time
import simplegrpcble_pb2 as ble_pb
import simplegrpcble_pb2_grpc as ble_grpc
from typing import List


class Device:
    def __init__(self, stub: ble_grpc.SimpleGRPCBLEStub, adapter_id: int, pb_device: ble_pb.Device) -> None:
        self._stub = stub
        self._adapter_id = adapter_id
        self._id = pb_device.id
        self._identifier = pb_device.identifier
        self._address = pb_device.address
        self._is_connectable = pb_device.is_connectable
        self._manufacturer_data = {}
        for key, value in pb_device.manufacturer_data.items():
            self._manufacturer_data[key] = value

    def identifier(self) -> str:
        return self._identifier

    def address(self) -> str:
        return self._address

    def is_connectable(self) -> bool:
        return self._is_connectable

    def manufacturer_data(self) -> dict:
        return self._manufacturer_data

class Adapter:
    def __init__(self, stub: ble_grpc.SimpleGRPCBLEStub, pb_adapter: ble_pb.Adapter) -> None:
        self._stub = stub
        self._id = pb_adapter.id
        self._identifier = pb_adapter.identifier
        self._address = pb_adapter.address
        self._devices = {}

    def identifier(self) -> str:
        return self._identifier

    def address(self) -> str:
        return self._address

    def scan_start(self) -> None:
        self._stub.AdapterScanStart(ble_pb.AdapterId(id=self._id))

    def scan_stop(self) -> None:
        self._stub.AdapterScanStop(ble_pb.AdapterId(id=self._id))

    def scan_is_active(self) -> bool:
        return self._stub.AdapterScanIsActive(ble_pb.AdapterId(id=self._id)).active

    def scan_get_results(self) -> List[Device]:
        response = self._stub.AdapterScanGetResults(ble_pb.AdapterId(id=self._id))
        device_list = []
        for device in response.devices:
            self._devices[device.id] = Device(self._stub, self._id, device)
            device_list.append(self._devices[device.id])
        return device_list

    def scan_for(self, timeout_ms: int) -> None:
        self.scan_start()
        time.sleep(timeout_ms / 1000)
        self.scan_stop()


class Client:
    def __init__(self, ip_address: str, port: int) -> None:
        self._channel = grpc.insecure_channel(f"{ip_address}:{port}")
        self._stub = ble_grpc.SimpleGRPCBLEStub(self._channel)
        self._adapters = {}

    def get_adapters(self) -> Adapter:
        response: ble_pb.AdapterList = self._stub.GetAdapters(ble_pb.Empty())
        adapter_list = []
        for adapter in response.adapters:
            self._adapters[adapter.id] = Adapter(self._stub, adapter)
            adapter_list.append(self._adapters[adapter.id])
        return adapter_list
