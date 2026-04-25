# CareConnect Architecture Documentation

## System Architecture

### Class Diagram
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

### Data Flow Diagram
```plantuml
@startuml CareConnect Dataflow

!define RECTANGLE class

' Data Sources and Storage
RECTANGLE "Snowflake\nCARECONNECT_TRAINING_DATA_STAGE" as SnowflakeStage {
    + training_data: Table
    + validation_data: Table
    + metadata: JSON
}

' Processing Components
RECTANGLE "Snowflake Snowpark\nContainer Services" as SnowparkContainer {
    RECTANGLE "ML Runtime 1.0" as MLRuntime {
        RECTANGLE "Data Loader" as DataLoader
        RECTANGLE "Preprocessing" as Preprocessing
        RECTANGLE "Training Pipeline" as TrainingPipeline
        RECTANGLE "Model Checkpointing" as Checkpointing
    }
}

' Model Storage and Deployment
RECTANGLE "Model Artifacts" as ModelArtifacts {
    + model_weights: safetensors
    + config: JSON
    + tokenizer: files
}

RECTANGLE "HuggingFace\nModel Repository" as HuggingFaceRepo {
    + model_files: files
    + inference_endpoint: URL
}

' Application Components
RECTANGLE "FastAPI\nApplication" as FastAPI {
    RECTANGLE "HuggingFaceEndpoint" as HFEndpoint
    RECTANGLE "API Endpoints" as APIEndpoints
}

' External Systems
RECTANGLE "Client Applications" as Clients

' Data Flow
SnowflakeStage --> DataLoader : "1. Load training data"
DataLoader --> Preprocessing : "2. Raw data"
Preprocessing --> TrainingPipeline : "3. Processed data"
TrainingPipeline --> Checkpointing : "4. Model checkpoints"
Checkpointing --> ModelArtifacts : "5. Save artifacts"
ModelArtifacts --> HuggingFaceRepo : "6. Deploy model"
HuggingFaceRepo --> HFEndpoint : "7. Connect to endpoint"
HFEndpoint --> APIEndpoints : "8. Serve requests"
APIEndpoints --> Clients : "9. API responses"

' Notes
note right of SnowflakeStage
  Contains:
  - Training conversations
  - Medical knowledge base
  - Healthcare guidelines
end note

note right of MLRuntime
  GPU-accelerated training
  LoRA fine-tuning
  Gradient checkpointing
end note

note right of ModelArtifacts
  Includes:
  - Fine-tuned weights
  - Model configuration
  - Tokenizer files
  - Training metadata
end note

note right of HuggingFaceRepo
  Hosts:
  - Model repository
  - Inference endpoint
  - Model versioning
end note

@enduml
```

## How to Use These Diagrams

These diagrams are written in PlantUML format. To view them, you can:

1. Use the [PlantUML Online Editor](https://www.plantuml.com/plantuml/uml/)
2. Install a PlantUML plugin in your IDE (VS Code, IntelliJ, etc.)
3. Use a tool like [Mermaid](https://mermaid.live/) (though you'll need to convert the syntax)

## Diagram Updates

When making changes to the system architecture, please update these diagrams to maintain accurate documentation. The diagrams should reflect:

1. New components added to the system
2. Changes in relationships between components
3. Updates to data flow patterns
4. New deployment or infrastructure changes 