# 🦞 AI-Tutor (OpenClaw Skill)

一个为 [OpenClaw](https://github.com/openclaw) 引擎打造的**纯文本交互式 AI 私教伴读/自测插件**。
专门为“考研”、“法考”等重文字、重逻辑的应试学习场景设计，主打：**极低 API 成本、苏格拉底式互动讲课、防走神强制抽查**。

## 🌟 核心理念与痛点解决

很多 AI 教育产品喜欢直接喂给你几万字的总结，或者生成一堆似是而非的选择题。但面对真正的应试教育，我们需要的是“学而时习之”：
- **痛点一：长文本 PDF/图文解析 API 成本极高。**
- **痛点二：一目十行看了就忘，缺乏互动和抽查。**
- **痛点三：AI 自己生成的题目脱离考纲，产生误导。**

**✨ AI-Tutor 的解决方案 (MVP)：**
1. **纯文本切块 (TXT-Only & 0 成本)**：放弃昂贵的 Vision 模型，自带轻量级 Python 脚本 (`digest_txt.py`)，将用户丢入的 `.txt` 课程讲义/网课字幕直接按字数本地切片，**0 成本规避 Token 焦虑**。
2. **读写分离与状态机并行**：不在一次会话中硬塞几十万字上下文。通过本地 `ai-tutor-state.json` 存档，支持**多门课程并行学习**，AI 每次只读取当前进度（Chunk）进行讲解。
3. **沉浸式伴读与复习双模式**：
   - **讲课模式 (`开始上课`)**：把知识点掰开揉碎详细讲给你听。
   - **复习模式 (`开始复习/抽查我`)**：不废话，直接从当前知识点里提炼问题考你。答错自动打入艾宾浩斯复习单（需配合 Ebbinghaus 插件）。

## 🚀 安装部署 

本插件完全依赖于 OpenClaw 生态系统运行。

### 1. 将文件克隆到你的工作区
将本项目直接下载或克隆到你的 OpenClaw 用户工作区 `skills/` 目录下：
```bash
git clone https://github.com/你的名字/ai-tutor.git ~/.openclaw/workspace/skills/ai-tutor
```

### 2. 创建必备的数据目录
因为 OpenClaw 的数据安全隔离，你需要手动创建存放你私密课件及进度的目录：
```bash
mkdir -p ~/.openclaw/workspace/knowledge/ai-tutor/raw
mkdir -p ~/.openclaw/workspace/knowledge/ai-tutor/materials
```

### 3. 初始化状态机 (State Machine)
在你的 OpenClaw 记忆体中创建一个初始存档文件：
```bash
cat << EOF > ~/.openclaw/workspace/memory/ai-tutor-state.json
{
  "active_course": "",
  "courses": {}
}
EOF
```

## 📚 使用流程

### 第一步：扔进课件并切块
1. 把你想要学习或复习的纯文本本子（比如法考民法典讲义、B站网课提取的字幕），保存为 `.txt` 文件（比如 `contract_law.txt`）。
2. 把这个 `contract_law.txt` 拖到 `~/.openclaw/workspace/knowledge/ai-tutor/raw/` 文件夹里。
3. 运行项目自带的免费切块脚本：
```bash
python3 ~/.openclaw/workspace/skills/ai-tutor/scripts/digest_txt.py
```
*(脚本会自动把它切成几百字一段的语意小薄片，并存入 `materials/contract_law.json`)*

### 第二步：在 `state.json` 激活课程
打开 `~/.openclaw/workspace/memory/ai-tutor-state.json`，把你想上的课（文件名）写进 `active_course`：
```json
{
  "active_course": "contract_law",
  "courses": {
    "contract_law": {
      "current_chunk": 0,
      "total_chunks": 50,
      "last_interaction": ""
    }
  }
}
```

### 第三步：去聊天软件里呼叫龙虾（老师）！
打开你的 Discord/Telegram：
- 发送：**“开始上课”** -> 老师会非常负责地把教材掰开揉碎讲给你听，必须听懂才放行。
- 发送：**“开始复习”/“抽查我”** -> 老师一上来就会拷问你考点，答错就记入小本本。

## 🎭 自定义你的人设 (Persona)
作为一个开源底座，你可以在你的 OpenClaw Agent 设置中赋予它任何性格！
不论是“严肃法学老教授”、“幽默温柔学姐”还是“喷人很凶的教练”，本引擎都会自动继承该人设的语气来执行上述讲课和抽查。

## 🤝 贡献指南
欢迎提交 Issue 和 Pull Request！特别是对于 `digest_txt.py` 的中文语义切分逻辑，期待大家一起把它优化得更聪明。

---
🎁 *本项目最初是作为一打工人的自我防摆烂生日礼物而诞生的。愿我们都能“学而时习之，不亦说乎”。*
