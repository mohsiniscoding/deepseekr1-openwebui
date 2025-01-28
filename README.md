# Deploying DeepSeek R1 Models Using Modal and OpenWebUI

## Introduction
Deploying machine learning models can be complex, especially when dealing with varying model sizes and ensuring scalability. The GitHub repository by mohsiniscoding aims to simplify this process by providing a production-ready setup for deploying DeepSeek R1 models using Modal, Ollama and OpenWebUI.

### Tools Overview
- **Modal**: A cloud platform designed for deploying machine learning models, offering flexibility in scaling resources based on model size.
- **OpenWebUI**: Developed by togethercomputer, it is an open-source project focused on creating user-friendly interfaces for interacting with AI models.
- **Ollama**: A lightweight, easy-to-use, and open-source server for running large language models.

## Key Features of the Repository

1. **Multi-model Support**:
   - The repository supports models ranging from 1.5B to 671B parameters, accommodating various deployment needs.

2. **Persistent Storage**:
   - Utilizes Modal volumes to cache models persistently across restarts, reducing the need for repeated downloads and saving time.

3. **GPU Optimization**:
   - Offers support for different GPU options (T4 and A100), ensuring that larger models with higher parameter counts can be efficiently deployed.

4. **Enterprise Readiness**:
   - Includes features like logging, error handling, and a secure and stable production environment.


## Deployment Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/mohsiniscoding/deepseekr1-openwebui.git
   cd deepseekr1-openwebui
   ```

2. **Install Dependencies** (locally, if needed):
   - Install modal
   ```bash
    pip install modal  
   ```

3. **Configure the Model**:
   - Edit `handler.py` to set your desired model under the `MODEL` constant.
   - Ensure that the model exists in the `DEEPSEEK_R1_MODELS` mapping.

4. **Deploy Using Modal**:
   ```bash
   modal token new  # If not already authenticated
   modal serve handler.py
   ```

5. **Access OpenWebUI**:
   - Once deployed, Modal provides a public URL accessible (even prior to launching ollama or openwebui)

## Troubleshooting

- **Ollama Issues**: If Ollama fails to start or models take too long to pull, consider increasing the `time.sleep()` delay in `handler.py`.
- **GPU Configuration**: Ensure your GPU is properly configured and meets the VRAM requirements for your model size.
- **Secrets Management**: Verify that all secrets and environment variables are correctly set up for seamless operation.

## Future Enhancements

1. **Determine GPU Configurations**:
   - Investigate GPU settings for models beyond 70B parameters to optimize hardware usage.

2. **Session Persistence**:
   - Develop features to save chat sessions and maintain OpenWebUI sessions across system restarts.

3. **Additional Features**:
   - Explore adding more functionalities as needed, enhancing the deployment experience further.

## Contributing

To contribute to this project:

1. Fork the repository.
2. Create a new branch from `main`.
3. Make your changes.
4. Commit and push your branch.
5. Open a pull request for review.

This setup provides a robust framework for deploying DeepSeek R1 models in production, leveraging Modal's scalability and OpenWebUI's interface capabilities. While some specifics like model configuration details may require further exploration, the repository offers a solid foundation for deployment needs.