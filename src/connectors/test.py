
from src.connectors.registry import registry

print(registry.available())


from src.config import RAW_DIR
from src.connectors.wbpcb import WBPCBConnector

connector = WBPCBConnector(RAW_DIR)

connector.connect()

files = connector.discover()

print(len(files))

print(files[:3])