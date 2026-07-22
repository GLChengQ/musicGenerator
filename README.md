# 🎵 Music Generator MCP Server

基于 **FastMCP + HuggingFace MusicGen + PyTorch** 构建的音乐生成 MCP Server。

用户可以通过 MCP Client（如 MCP Inspector、mcp-use、Agent 平台等）输入自然语言描述，服务端调用本地音乐生成模型生成 `.wav` 音频文件。

支持：

- ✅ MCP Streamable HTTP 协议
- ✅ 多设备远程访问
- ✅ GPU 模型常驻
- ✅ 异步任务队列
- ✅ 单 GPU 推理调度
- ✅ 本地音频保存
- ✅ uv Python 环境管理


---

# 🏗️ Architecture

```
                MCP Client
          (Inspector / Agent / App)
                    |
                    |
          Streamable HTTP (/mcp)
                    |
                    |
             FastMCP Server
                    |
          ---------------------
          |                   |
     Async Queue          MCP Tools
          |
          |
      GPU Worker
          |
          |
      MusicGen Model
          |
          |
     outputs/*.wav
```


## Workflow

1. 用户输入音乐描述

例如：

```
一首充满力量的电子摇滚音乐，
适合运动训练，快速节奏，高能量
```

2. MCP Client 调用：

```
generate_music()
```

3. FastMCP Server：

```
接收请求
 ↓
进入异步队列
 ↓
GPU Worker处理
 ↓
MusicGen生成音乐
 ↓
保存wav文件
 ↓
返回文件路径
```


---

# 📦 Environment

## Requirements

- Python >= 3.11
- CUDA (optional but recommended)
- NVIDIA GPU recommended


测试环境：

```
GPU:
RTX3060 12GB

Python:
3.11

FastMCP:
3.4.4

PyTorch:
CUDA version compatible

Model:
facebook/musicgen-small
```


---

# 🚀 Installation


## 1. Clone repository

```bash
git clone <your-repository>

cd musicGenerator
```


---

## 2. Install uv

如果没有安装：

```bash
pip install uv
```


检查：

```bash
uv --version
```


---

## 3. Create environment

使用 uv 创建虚拟环境：

```bash
uv venv
```


激活：

Windows:

```powershell
.venv\Scripts\activate
```


Linux/macOS:

```bash
source .venv/bin/activate
```


---

## 4. Install dependencies


```bash
uv sync
```


或者：

```bash
uv add fastmcp torch transformers scipy
```


---

# 📁 Project Structure


```
musicGenerator
│
├── server.py
│
├── music
│   ├── __init__.py
│   └── music_generator.py
│
├── outputs
│
├── pyproject.toml
│
└── README.md
```


---

# 🎼 Model


当前使用：

## Meta MusicGen

HuggingFace:

```
facebook/musicgen-small
```


模型能力：

输入：

```
text prompt
```

输出：

```
wav audio
```


示例：

Input:

```
A cinematic orchestra with powerful drums
```


Output:

```
outputs/xxxx.wav
```


---

# ▶️ Run Server


启动 MCP Server：

```bash
uv run server.py
```


成功启动：

```
Starting music worker

🎵 Music worker started

Starting MCP server
with transport streamable-http

http://0.0.0.0:8000/mcp
```


---

# 🔌 MCP Client Connection


## MCP Inspector


安装：

```bash
npx @modelcontextprotocol/inspector
```


连接：

```
Transport:

Streamable HTTP


URL:

http://127.0.0.1:8000/mcp
```



---

# 🛠️ MCP Tools


## generate_music


生成音乐。


Input:

```json
{
    "prompt":
    "energetic electronic rock music"
}
```


Output:

```
outputs/xxxx.wav
```



---

# ⚡ Async Processing


为了支持多个设备同时访问：

服务端采用：

```
asyncio.Queue
+
asyncio.to_thread()
+
single GPU worker
```


请求流程：

```
Device A
    |
    |
generate_music()
    |
    |
Queue


Device B
    |
    |
generate_music()
    |
    |
Queue


        GPU

        |
        |
     MusicGen
```


特点：

- HTTP请求不会阻塞
- 多用户请求不会导致模型重复加载
- GPU任务统一调度


---

# 🎧 Output


生成文件：

```
outputs/

xxxx.wav
```


未来计划：

```
Local Storage

        |

File Service

        |

Consumer Device
```


实现：

- 在线播放
- 下载
- 手机端推送


---

# ⚠️ Limitations


## 1. Music duration


MusicGen-small 默认生成长度有限。

当前：

```
约5~30秒
```

后续考虑：

- MusicGen-large
- AudioCraft
- Stable Audio
- Long-form generation


---

## 2. Vocal generation


当前模型：

主要生成：

```
instrumental music
```


不擅长：

```
完整人声歌曲
```


后续考虑：

- Lyrics model
- TTS singing model
- Song generation pipeline


---

## 3. GPU concurrency


单GPU环境：

推荐：

```
one worker
+
queue
```


不推荐：

```
multiple MusicGen inference
simultaneously
```


否则可能：

- CUDA OOM
- GPU slowdown


---

# 🛣️ Roadmap


## V1

完成：

- [x] MusicGen integration
- [x] FastMCP Server
- [x] Streamable HTTP
- [x] Async queue


## V2

计划：

- [ ] Audio file API
- [ ] Online playback
- [ ] User authentication
- [ ] Task progress


## V3

商业化方向：

```
MCP Gateway

        |

Task Queue

        |

GPU Cluster

        |

Object Storage

        |

Mobile App
```


---

# License

MIT