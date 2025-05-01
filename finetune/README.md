# CareConnect Model Fine-tuning

This directory contains the code and resources for fine-tuning the CareConnect AI model.

## 🎯 Overview

The CareConnect model is fine-tuned using medical datasets to provide accurate and responsible health advice. This process involves:

- Dataset preparation and preprocessing
- Model training and validation
- Performance evaluation
- Model deployment to Hugging Face

## 📊 Dataset Preparation

### Dataset Location
All training datasets are located in the `/data` directory at the project root. The directory structure is as follows:

```
/data/
├── drug/          
├── explain/ 
├── predict-illness/     
└── predict-treatment/ 
```

### Medical Datasets
- Treatment Prediction datasets (by health catagory) (`/data/predict-treatment/`)
- Illness Prediction datasets (by health catagory) (`/data/predict-illness/`)
- Drug Information datasets (`/data/drug/`)
- General Health Questions Qatasets (`/data/explain/`)

### Preprocessing Steps
1. Data cleaning and normalization
2. Tokenization and formatting
3. Dataset splitting (train/validation/test)
4. Quality assurance checks

## 🚂 Model Training

### Base Models
- Llama 3.2 (3B parameters)
- Gemma 3 (4B parameters) - Coming Soon

### Training Configuration
```python
training_args = {
    "learning_rate": 2e-5,
    "num_train_epochs": 3,
    "per_device_train_batch_size": 16,
    "gradient_accumulation_steps": 8,
    "warmup_steps": 500,
    "weight_decay": 0.01,
    "logging_steps": 10,
    "save_steps": 1000
}
```

### Training Process
1. Load pre-trained model
2. Apply medical dataset
3. Fine-tune with specified parameters
4. Validate performance
5. Save checkpoints

## 📈 Performance Metrics

### Evaluation Criteria
- Medical accuracy
- Response coherence
- Safety compliance
- Response time
- Token efficiency

### Benchmark Results
- Medical QA accuracy: 
- Response coherence:
- Safety compliance: 
- Average response time: 

## 🚀 Deployment

### Hugging Face Integration
1. Model conversion to Hugging Face format
2. Upload to Hugging Face Hub
3. Set up inference API
4. Configure model card and documentation

### Model Cards
- [careconnect-llama3.2-3b](https://huggingface.co/JdoubleU/careconnect-llama3.2-3b)
- careconnect-gemma3-4b (Coming Soon)

## 🛠️ Local Development

### Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure environment:
   ```bash
   export HF_TOKEN=your_huggingface_token
   export WANDB_API_KEY=your_wandb_key
   ```

### Training
1. Prepare dataset:
   ```bash
   python prepare_dataset.py
   ```

2. Start training:
   ```bash
   python train.py
   ```

3. Evaluate model:
   ```bash
   python evaluate.py
   ```

## 📦 Docker Support

Build the training environment:
```bash
docker build -t careconnect-training .
```

Run training:
```bash
docker run -it \
  -v $(pwd)/data:/app/data \
  -e HF_TOKEN=your_huggingface_token \
  careconnect-training
```

## 🔍 Testing

Run model tests:
```bash
python -m pytest tests/
```

Test categories:
- Dataset validation
- Training pipeline
- Model performance
- Deployment checks

## 📚 Resources

### Documentation
- [Hugging Face Transformers](https://huggingface.co/docs/transformers/index)
- [Medical NLP Best Practices](https://huggingface.co/docs/transformers/tasks/medical)
- [Model Cards](https://huggingface.co/docs/hub/model-cards)


## 📞 Support

For questions about model fine-tuning or training:
- Team Lead & LLM Training Lead: Jabin Wade [jwade23@pvamu.edu](mailto:Jwade23@pvamu.edu)
- Lead Data Engineer: Zero Nelson [jnelson50@pvamu.edu](mailto:jnelson50@pvamu.edu)
