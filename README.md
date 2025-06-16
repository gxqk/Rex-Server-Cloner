# 🦕 Rex Server-Cloner

<div align="center">

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Discord.py](https://img.shields.io/badge/discord.py--self-green.svg)
![License](https://img.shields.io/badge/License-Educational-yellow.svg)
![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightblue.svg)

*A powerful Discord selfbot to fully clone Discord servers with complete hierarchy preservation*

[Features](#-features) • [Installation](#-installation) • [Configuration](#-configuration) • [Usage](#-usage) • [Support](#-support)

</div>

---

## 📋 Table of Contents

- [✨ Features](#-features)
- [🚀 Installation](#-installation)
- [⚙️ Configuration](#️-configuration)
- [🎯 Usage](#-usage)
- [🔧 Customization](#-customization)
- [⚠️ Important Notes](#️-important-notes)
- [🆘 Support](#-support)
- [📝 License](#-license)

---

## ✨ Features

### 🎮 **Core Functionality**
- **Complete Server Cloning**: Clone roles, channels, categories, permissions, emojis & settings
- **Hierarchy Preservation**: Maintains exact role order and permission structure
- **Smart Cleaning**: Automatically removes existing content before cloning
- **Permission Mapping**: Preserves role and channel permissions accurately
- **Icon Cloning**: Optional server icon/banner copying

### 🔐 **Advanced Features**
- **Role Hierarchy**: Preserves exact role positions (Owner stays at top)
- **Channel Permissions**: Clones specific permissions for each channel
- **Category Structure**: Maintains channel organization within categories
- **Emoji Support**: Copies all custom emojis with proper naming
- **Rate Limit Handling**: Smart delays to avoid Discord restrictions

### 🖥️ **User Experience**
- **Windows Compatible**: No emoji display issues on Windows 10/11
- **ASCII Art Interface**: Beautiful Rex dinosaur banner
- **Colored Output**: Clear status messages with color coding
- **Progress Tracking**: Real-time feedback during cloning process
- **Error Handling**: Robust error management with detailed feedback

---

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- Discord account with access to source and target servers
- Administrator permissions on target server

### Quick Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/gxqk/Rex-Server-Cloner.git
   cd rex-server-cloner
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your token**
   ```bash
   # Edit config.json with your Discord token
   notepad config.json
   ```

4. **Run the cloner**
   ```bash
   python main.py
   ```

---

## ⚙️ Configuration

### 📄 config.json

```json
{
    "discord_token": "YOUR_DISCORD_TOKEN_HERE",
    "settings": {
        "role_create_delay": 1.0,
        "channel_create_delay": 0.5,
        "emoji_create_delay": 1.0,
        "permission_update_delay": 0.3
    }
}
```

### 🔧 Configuration Options

| Setting | Description | Recommended Value |
|---------|-------------|-------------------|
| `discord_token` | Your Discord user token | Required |
| `role_create_delay` | Delay between role creation (seconds) | 1.0 |
| `channel_create_delay` | Delay between channel creation (seconds) | 0.5 |
| `emoji_create_delay` | Delay between emoji creation (seconds) | 1.0 |
| `permission_update_delay` | Delay for permission updates (seconds) | 0.3 |

### 🎯 **Getting Your Discord Token**

1. Open Discord in your browser
2. Press F12 to open Developer Tools
3. Go to Network tab and refresh the page
4. Look for requests to `api/v9` or similar
5. In the request headers, copy the "Authorization" value

---

## 🎯 Usage

### 🎮 **Basic Cloning Process**

1. **Launch the application**
   ```bash
   python main.py
   ```

2. **Follow the prompts and enjoy the cloning process!**

### 🔍 **Getting Server IDs**

1. Enable Developer Mode in Discord (Settings > Advanced > Developer Mode)
2. Right-click on the server name
3. Select "Copy ID"

---

## 🔧 Customization

### ⚡ **Speed Optimization**

For faster cloning (higher risk of rate limits):
```json
{
    "settings": {
        "role_create_delay": 0.5,
        "channel_create_delay": 0.3,
        "emoji_create_delay": 0.5,
        "permission_update_delay": 0.2
    }
}
```

### ⚖️ **Balanced Configuration (Default)**

Perfect balance between speed and stability (recommended):
```json
{
    "settings": {
        "role_create_delay": 1.0,
        "channel_create_delay": 0.5,
        "emoji_create_delay": 1.0,
        "permission_update_delay": 0.3
    }
}
```

### 🛡️ **Stability Optimization**

For more stable cloning (slower but safer):
```json
{
    "settings": {
        "role_create_delay": 2.0,
        "channel_create_delay": 1.0,
        "emoji_create_delay": 2.0,
        "permission_update_delay": 0.5
    }
}
```

---

## ⚠️ Important Notes

### 🚨 **Disclaimer**
- This tool is for **educational purposes only**
- Using selfbots may violate Discord's Terms of Service
- Use at your own risk and responsibility
- The author is not responsible for any consequences

### 🔒 **Security**
- Never share your Discord token with anyone
- Keep your `config.json` file private
- Use this tool responsibly and ethically



---

## 🆘 Support

Need help with Rex Server-Cloner? Have questions or issues?

**Contact me on Discord: `gxqk_secours`**

I'm here to help you with:
- 🔧 Configuration and setup assistance
- 🐛 Troubleshooting and bug reports
- ⚙️ Customization and optimization
- 💡 General questions and guidance

Don't hesitate to reach out!

---

## 📝 License

This project is for educational purposes only. Please use responsibly and in accordance with Discord's Terms of Service.

---

<div align="center">

**Made with ❤️ by gxqk_secours**

*If you find this project useful, please consider giving it a ⭐!*

**🦕 Rex Server-Cloner - Clone with the power of a T-Rex! 🦕**

</div>
