# Cyra AI - Cybersecurity Assistant

![Cyra AI Banner](https://img.shields.io/badge/Cyra%20AI-Cybersecurity%20Assistant-blue?style=for-the-badge&logo=shield&logoColor=white)

## 🚀 Pre-Launch Preview

Experience the future of cybersecurity with **Cyra AI** - an advanced AI-powered cybersecurity assistant featuring voice chat, real-time threat analysis, and intelligent security tools.

### 🌐 Live Demo
**[Try Cyra AI →](https://your-username.github.io/cyra-ai/)**

## ✨ Features

### 🎙️ **Voice Chat & Recognition**
- Natural voice conversations with perfect synchronization
- Real-time speech recognition and instant AI responses
- Hands-free cybersecurity assistance

### 🛡️ **Advanced Security Analysis**
- Real-time threat detection and vulnerability assessments
- Comprehensive security audits powered by AI
- Cutting-edge threat intelligence integration

### 🔐 **Smart Password Management**
- Ultra-secure password generation
- Password strength analysis and recommendations
- Multi-platform security optimization

### ⚡ **Real-time AI Responses**
- Zero-delay threat analysis
- Immediate security recommendations
- Rapid incident response guidance

### 🎤 Voice Interaction
- High-quality text-to-speech using Azure Speech Services
- Natural, human-like voice responses
- Speech-to-text for hands-free interaction

### 🔧 Cybersecurity Toolbox
- **Password Generator**: Create cryptographically secure passwords
- **Password Strength Analyzer**: Assess password security
- **Passphrase Generator**: Create memorable yet secure passphrases
- **Security Advisor**: Get expert cybersecurity advice
- **Network Scanner**: Nmap integration for reconnaissance (planned)

### 🔐 Security Features
- User authentication and session management
- Secure password generation with customizable options
- Privacy-focused architecture
- Professional-grade security practices

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Azure OpenAI account and API key
- Azure Speech Services account and key

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd cyra
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables**
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your Azure credentials
# Required variables:
# - AZURE_OPENAI_ENDPOINT
# - AZURE_OPENAI_API_KEY
# - AZURE_OPENAI_DEPLOYMENT_NAME
# - AZURE_SPEECH_KEY
# - AZURE_SPEECH_REGION
# - SECRET_KEY
```

4. **Start the application**
```bash
python main.py
```

5. **Access Cyra**
- Web Interface: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

## 💬 Usage Examples

### Chat Interface
Ask Cyra questions in natural language:
- "Generate a strong password for my bank account"
- "How can I protect myself from phishing attacks?"
- "Check the strength of my current password"
- "Create a memorable passphrase"
- "What are the best practices for WiFi security?"

### API Endpoints

#### Chat with Cyra
```bash
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "Generate a secure password", "user_id": "user123"}'
```

#### Generate Password
```bash
curl -X POST "http://localhost:8000/tools/password/generate" \
     -H "Content-Type: application/json" \
     -d '{"length": 16, "include_special": true, "count": 1}'
```

#### Check Password Strength
```bash
curl -X POST "http://localhost:8000/tools/password/strength" \
     -H "Content-Type: application/json" \
     -d '{"password": "MyPassword123!"}'
```

## 🏗️ Architecture

```
cyra/
├── src/
│   ├── core/
│   │   ├── ai_brain.py      # AI conversation engine
│   │   ├── app.py           # FastAPI application
│   │   └── config.py        # Configuration management
│   ├── speech/
│   │   └── speech_service.py # Text-to-speech & speech-to-text
│   ├── tools/
│   │   ├── password_generator.py # Password security tools
│   │   └── tool_manager.py      # Tool coordination
│   └── auth/                # User authentication (planned)
├── config/                  # Configuration files
├── tests/                   # Unit tests
├── main.py                  # Application entry point
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🛠️ Available Tools

### Password Generator
- **Secure Generation**: Cryptographically secure random passwords
- **Customizable**: Length, character types, special requirements
- **Multiple Options**: Generate several passwords at once
- **Strength Assessment**: Automatic security analysis

### Password Analyzer
- **Strength Scoring**: 0-100 security score
- **Detailed Feedback**: Specific improvement suggestions
- **Crack Time Estimation**: Time required to break the password
- **Breach Pattern Detection**: Check for common vulnerability patterns

### Security Advisor
- **Expert Guidance**: Professional cybersecurity advice
- **Topic Coverage**: Passwords, phishing, WiFi, general security
- **Best Practices**: Industry-standard recommendations
- **Context-Aware**: Tailored advice based on user situation

## 🔮 Planned Features

### Advanced Security Tools
- **Nmap Integration**: Network discovery and port scanning
- **Vulnerability Scanner**: Automated security assessments
- **Threat Intelligence**: Real-time security feeds
- **Incident Response**: Guided response procedures

### Enhanced AI Capabilities
- **Learning Mode**: Adapt to user preferences and needs
- **Multi-language Support**: Global accessibility
- **Voice Commands**: Complete hands-free operation
- **Visual Recognition**: Screenshot security analysis

### Enterprise Features
- **Team Management**: Multi-user organizations
- **Compliance Reporting**: Security audit trails
- **Integration APIs**: Connect with existing security tools
- **Custom Policies**: Organization-specific security rules

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI service endpoint | - | Yes |
| `AZURE_OPENAI_API_KEY` | Azure OpenAI API key | - | Yes |
| `AZURE_OPENAI_DEPLOYMENT_NAME` | Model deployment name | - | Yes |
| `AZURE_SPEECH_KEY` | Azure Speech service key | - | Yes |
| `AZURE_SPEECH_REGION` | Azure Speech service region | - | Yes |
| `SECRET_KEY` | JWT token secret key | - | Yes |
| `DATABASE_URL` | Database connection string | `sqlite:///./cyra.db` | No |
| `HOST` | Server host address | `localhost` | No |
| `PORT` | Server port number | `8000` | No |
| `DEBUG` | Enable debug mode | `False` | No |

## 🧪 Development

### Running Tests
```bash
# Install development dependencies
pip install pytest pytest-asyncio

# Run tests
pytest tests/

# Run with coverage
pytest --cov=src tests/
```

### Code Quality
```bash
# Format code
black src/

# Lint code
flake8 src/
```

### API Documentation
When running the application, automatic API documentation is available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Azure OpenAI for powering the conversational AI
- Azure Speech Services for natural voice interaction
- FastAPI for the robust web framework
- The cybersecurity community for best practices and guidance

## 📞 Support

For support, feature requests, or bug reports, please:
1. Check the [documentation](http://localhost:8000/docs) when running
2. Create an issue in the repository
3. Contact the development team

---

**⚠️ Security Notice**: Cyra is designed to provide cybersecurity education and tools. Always follow responsible disclosure practices and respect applicable laws when using security tools. The developers are not responsible for misuse of this software.

**🎯 Mission**: Making cybersecurity accessible, understandable, and actionable for everyone through the power of AI conversation.
