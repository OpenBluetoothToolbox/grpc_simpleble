import simplegrpcble

if __name__ == "__main__":
    client = simplegrpcble.Client("localhost", 50051)

    adapters = client.get_adapters()

    for adapter in adapters:
        print(f"Adapter: {adapter.identifier()} [{adapter.address()}]")
