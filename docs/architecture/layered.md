# CareConnect Layered Architecture

```plantuml
@startuml CareConnect Layered Architecture

skinparam packageStyle rectangle

package "Presentation Layer" {
    [Client Applications] as Clients
    [Web Interface] as WebUI
    [API Endpoints] as API
}

package "Application Layer" {
    [FastAPI Application] as FastAPI
    [Request Handlers] as Handlers
    [Middleware] as Middleware
}

package "Service Layer" {
    [HuggingFaceEndpoint] as HFEndpoint
    [LLM Service] as LLMService
    [Model Inference] as Inference
}

package "Model Layer" {
    [HuggingFace Hosting] as HFHosting
    [Model Repository] as ModelRepo
    [Model Versioning] as Versioning
}

package "Training Layer" {
    [Snowflake Snowpark] as Snowpark
    [ML Runtime] as MLRuntime
    [Training Pipeline] as Training
}

package "Data Layer" {
    [Snowflake Data Stage] as DataStage
    [Training Data] as TrainData
    [Validation Data] as ValData
}

' Layer Relationships
Clients --> WebUI
Clients --> API
WebUI --> API
API --> FastAPI
FastAPI --> Handlers
FastAPI --> Middleware
Handlers --> HFEndpoint
HFEndpoint --> LLMService
LLMService --> Inference
Inference --> HFHosting
HFHosting --> ModelRepo
ModelRepo --> Versioning
Versioning --> Training
Training --> MLRuntime
MLRuntime --> Snowpark
Snowpark --> DataStage
DataStage --> TrainData
DataStage --> ValData

note right of "Presentation Layer"
  Handles user interaction
  and request/response flow
end note

note right of "Application Layer"
  Manages application logic
  and request processing
end note

note right of "Service Layer"
  Provides LLM services
  and model inference
end note

note right of "Model Layer"
  Manages model deployment
  and versioning
end note

note right of "Training Layer"
  Handles model training
  and fine-tuning
end note

note right of "Data Layer"
  Stores and manages
  training data
end note

@enduml
```

## Layer Descriptions

### Presentation Layer
- **Client Applications**: End-user applications that interact with the system
- **Web Interface**: Web-based user interface
- **API Endpoints**: RESTful API endpoints for client communication

### Application Layer
- **FastAPI Application**: Main application server
- **Request Handlers**: Handles incoming requests
- **Middleware**: Cross-cutting concerns like CORS, logging, etc.

### Service Layer
- **HuggingFaceEndpoint**: Interface to HuggingFace services
- **LLM Service**: Language model service implementation
- **Model Inference**: Handles model inference requests

### Model Layer
- **HuggingFace Hosting**: Model hosting service
- **Model Repository**: Model storage and management
- **Model Versioning**: Version control for models

### Training Layer
- **Snowflake Snowpark**: Training infrastructure
- **ML Runtime**: Machine learning runtime environment
- **Training Pipeline**: Model training workflow

### Data Layer
- **Snowflake Data Stage**: Data storage in Snowflake
- **Training Data**: Training dataset management
- **Validation Data**: Validation dataset management 