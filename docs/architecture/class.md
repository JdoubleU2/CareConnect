# CareConnect Class Diagram

```plantuml
@startuml CareConnect

' Main Application Components
class FastAPI {
    + title: str
    + version: str
    + description: str
    + add_middleware()
    + mount()
}

class HuggingFaceEndpoint {
    + endpoint_url: str
    + huggingfacehub_api_token: str
    + ainvoke()
}

class LLMInput {
    + input: str
}

class CORSMiddleware {
    + allow_origins: List[str]
    + allow_credentials: bool
    + allow_methods: List[str]
    + allow_headers: List[str]
}

class StaticFiles {
    + directory: str
    + html: bool
}

' Finetuning Components
class SnowflakeSnowpark {
    + container_services: ContainerServices
    + data_warehouse: DataWarehouse
    + execute_finetuning()
}

class FinetuningProcess {
    + base_model: str
    + training_data: Dataset
    + hyperparameters: Dict
    + train()
    + evaluate()
    + save_model()
}

class LlamaModel {
    + model_name: str
    + model_size: str
    + quantization: str
    + load_model()
    + save_model()
}

class Dataset {
    + data_source: str
    + preprocessing: Preprocessing
    + load_data()
    + preprocess()
}

' Deployment Components
class HuggingFaceHosting {
    + model_repository: str
    + deployment_config: Dict
    + deploy_model()
    + update_model()
    + inference_endpoint: str
}

' Relationships
FastAPI --> HuggingFaceEndpoint : uses
FastAPI --> LLMInput : processes
FastAPI --> CORSMiddleware : uses
FastAPI --> StaticFiles : serves

SnowflakeSnowpark --> FinetuningProcess : executes
FinetuningProcess --> LlamaModel : trains
FinetuningProcess --> Dataset : uses
LlamaModel --> HuggingFaceHosting : deploys to

' Updated HuggingFace relationship
HuggingFaceHosting --> HuggingFaceEndpoint : provides endpoint for
HuggingFaceEndpoint ..> HuggingFaceHosting : consumes model from

note right of SnowflakeSnowpark
  Runs in Snowpark Container Services
  Provides GPU resources for training
end note

note right of FinetuningProcess
  Uses LoRA for efficient fine-tuning
  Optimizes for healthcare domain
end note

note right of HuggingFaceHosting
  Hosts CareConnect model
  Provides inference endpoint
  Manages model versioning
end note

note right of HuggingFaceEndpoint
  Connects to HuggingFaceHosting
  endpoint_url points to hosted model
end note

@enduml
```

## Component Descriptions

### Application Components
- **FastAPI**: Main application server handling HTTP requests
- **HuggingFaceEndpoint**: Interface to HuggingFace LLM services
- **LLMInput**: Data model for LLM input validation
- **CORSMiddleware**: Handles cross-origin resource sharing
- **StaticFiles**: Serves static web content

### Finetuning Components
- **SnowflakeSnowpark**: Container services for model training
- **FinetuningProcess**: Manages the model training workflow
- **LlamaModel**: Represents the base model being fine-tuned
- **Dataset**: Handles data loading and preprocessing

### Deployment Components
- **HuggingFaceHosting**: Manages model deployment and hosting 