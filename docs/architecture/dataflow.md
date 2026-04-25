# CareConnect Data Flow Diagram

```plantuml
@startuml CareConnect Dataflow

' Data Sources and Storage
rectangle "Snowflake\nCARECONNECT_TRAINING_DATA_STAGE" as SnowflakeStage {
    rectangle "Training Data" as TrainData
    rectangle "Validation Data" as ValData
    rectangle "Metadata" as Metadata
}

' Processing Components
rectangle "Snowflake Snowpark\nContainer Services" as SnowparkContainer {
    rectangle "ML Runtime 1.0" as MLRuntime {
        rectangle "Data Loader" as DataLoader
        rectangle "Preproecessing" as Preprocessing
        rectangle "Training Pipeline" as TrainingPipeline
        rectangle "Model Checkpointing" as Checkpointing
    }
}

' Model Storage and Deployment
rectangle "Model Artifacts" as ModelArtifacts {
    rectangle "Model Weights" as Weights
    rectangle "Config" as Config
    rectangle "Tokenizer" as Tokenizer
}

rectangle "HuggingFace\nModel Repository" as HuggingFaceRepo {
    rectangle "Model Files" as ModelFiles
    rectangle "Inference Endpoint" as Endpoint
}

' Application Components
rectangle "FastAPI\nApplication" as FastAPI {
    rectangle "HuggingFaceEndpoint" as HFEndpoint
    rectangle "API Endpoints" as APIEndpoints
}

' External Systems
rectangle "Client Applications" as Clients

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

## Data Flow Description

### Training Data Flow
1. **Data Loading**: Training data is loaded from Snowflake CARECONNECT_TRAINING_DATA_STAGE
2. **Preprocessing**: Raw data is preprocessed in the ML Runtime
3. **Training**: Processed data is used to train the model
4. **Checkpointing**: Model checkpoints are saved during training
5. **Artifact Creation**: Final model artifacts are created

### Deployment Flow
6. **Model Deployment**: Model artifacts are deployed to HuggingFace
7. **Endpoint Connection**: FastAPI connects to the HuggingFace endpoint
8. **Request Serving**: API endpoints serve client requests
9. **Response Delivery**: Responses are delivered to client applications

### Key Components
- **Snowflake Stage**: Primary data storage
- **ML Runtime**: Training environment
- **Model Artifacts**: Trained model files
- **HuggingFace Repository**: Model hosting
- **FastAPI Application**: Request handling 