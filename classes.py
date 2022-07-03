from dataclasses import dataclass, field
import marshmallow
import marshmallow_dataclass


@dataclass
class DataRequest:
    file_name: str = field(metadata={"data_key": "file_name"})
    cmd1: str = field(metadata={"data_key": "cmd1"})
    value1: str = field(metadata={"data_key": "value1"})
    cmd2: str = field(metadata={"data_key": "cmd2"})
    value2: str = field(metadata={"data_key": "value2"})

    class Meta:
        unknown = marshmallow.EXCLUDE


DataRequestSchema = marshmallow_dataclass.class_schema(DataRequest)
