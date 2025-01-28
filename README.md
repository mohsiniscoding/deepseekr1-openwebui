# DeepSeek R1 - OpenWebUI Deployment via Modal

This repository by [@mohsiniscoding](https://github.com/mohsiniscoding) provides a production-ready deployment of DeepSeek R1 models using [Modal](https://modal.com) with integrated [Open-WebUI](https://github.com/togethercomputer/OpenWebUI).

## 🚀 Key Features

- **Multi-model Support**: Deploy 1.5B to 671B parameter models
- **Persistent Storage**: Automatic model caching with Modal volumes
- **GPU Optimization**: Configurable GPU allocations (T4/A100)
- **Enterprise Ready**: Built-in logging and error handling
- **Secure**: Encrypted secrets management

## TODO
- [ ] Determine the GPU configuration for models other than 70B parameter.
- [ ] Ability to persist chat and openwebui sessions across restarts.
- [ ] Add more...

## 📦 Quick Deployment

### Prerequisites
- Python 3.11+
- [Modal Account](https://modal.com/signup)
- CLI Access

### Installation

1. Clone the Repository:  
   git clone https://github.com/mohsiniscoding/deepseekr1-openwebui.git  
   cd deepseekr1-openwebui

2. Install Dependencies (Locally, Optional):  
   pip install -r requirements.txt
   pip install modal (required for deployment)

3. Configure the Model:  
   • In handler.py, set your desired model under the `MODEL` constant.  
   • Ensure it exists in the `DEEPSEEK_R1_MODELS` mapping.

4. Deploy the Modal App:  
   • If you have Modal installed locally, run:  
     modal token new  
     modal serve handler.py  
   • Alternatively, set up a CI-based deployment that invokes Modal in your environment.

5. Access Open-WebUI:  
   • The web server runs on port 8080 by default.  
   • Once deployment is complete, Modal provides a public URL. (before ollama or openwebui starts - copy it)

## Model Caching

• The container will pull your model into /root/models/.  
• A Modal volume is mapped to this location, preserving downloads across restarts.

## Troubleshooting

• If Ollama fails to start or the model pull times out, try increasing the time.sleep() delay in handler.py.  
• Check that your GPU is accessible within the Modal environment and meets model VRAM requirements.  
• Confirm your secrets and environment variables align with your usage patterns (if you are using custom endpoints or tokens).

## Contributing

1. Fork the repository and create your branch from main.  
2. Commit changes, then open a pull request for review.  

