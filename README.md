# 🦞 AI-Tutor (OpenClaw Skill)

一个为 [OpenClaw](https://github.com/openclaw) 引擎打造的**纯文本交互式 AI 私教伴读/自测插件**。
专门为国内公考法考考研等重文字、重逻辑的应试学习场景设计，主打：**极低 API 成本、苏格拉底式互动讲课、防走神监督模式**。

## 🌟 核心理念与痛点解决

很多 AI 教育产品喜欢直接喂给你几万字的总结，或者生成一堆似是而非的选择题。但面对真正的应试教育，我们需要的是不断的知识复现：
- **痛点一：长文本 PDF/图文解析 API 成本极高。**
- **痛点二：一目十行看了就忘，缺乏互动和抽查。**
- **痛点三：AI 自己生成的题目脱离考纲，产生误导。**

**✨ AI-Tutor 的解决方案 (MVP)：**
1. **纯文本切块 (TXT-Only & 0 成本)**：放弃昂贵的 Vision 模型，自带轻量级 Python 脚本 (`digest_txt.py`)，将用户丢入的 `.txt` 课程讲义/网课字幕直接按字数本地切片，**0 成本规避 Token 焦虑**。
2. **读写分离与状态机并行**：不在一次会话中硬塞几十万字上下文。通过本地 `ai-tutor-state.json` 存档，支持**多门课程并行学习**，AI 每次只读取当前进度（Chunk）进行讲解。
3. **沉浸式伴读与复习双模式**：
   - **讲课模式 (`开始上课`)**：把知识点掰开揉碎详细讲给你听。
   - **复习模式 (`开始复习/抽查我`)**：不废话，直接从当前知识点里提炼问题考你。答错自动打入内置的复习错题本 (Review Queue)。
   - **监督与考核 (`生成今日报告`)**：结合 OpenClaw 定时任务，实时监控学情，防走神打断，并在结束时根据当天推进的进度生成“班主任式”的日结评价。

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

## 📚 使用流程

### 第一步：扔进课件
1. 把你想要学习或复习的纯文本本子（比如法考讲义、网盘课程字幕提取文件登），保存为 `.txt` 文件（比如 `contract_law.txt`）。
2. 把这个 `contract_law.txt` 拖到 `~/.openclaw/workspace/knowledge/ai-tutor/raw/` 文件夹里。

### 第二步：一键切块与注册
运行项目自带的免费切块脚本，它会进行**重叠语义切片**（保证上下文连贯），并**全自动将课程注册到你的记忆存档中**：
```bash
python3 ~/.openclaw/workspace/skills/ai-tutor/scripts/digest_txt.py
```
*(脚本执行后，你的 `~/.openclaw/workspace/memory/ai-tutor-state.json` 就会自动创建，并把这门新课设为当前活动课程。)*

### 第三步：去聊天软件里呼叫老师！
打开你的 Discord/Telegram：
- 发送：**“开始上课”** -> 老师会非常负责地把教材掰开揉碎讲给你听，必须听懂才放行。
- 发送：**“开始复习”/“抽查我”** -> 老师一上来就会拷问你考点，答错就记入小本本。
- 发送：**“结束学习”/“今日总结”** -> 老师会根据 `state.json` 结算你今天推进的进度，生成带有人设情绪的班主任评语。

> **💡 高级用法 (防走神 Cron)**：你可以在 OpenClaw 的 `cron/jobs.json` 中配制定时任务，让机器人每隔 15 分钟检查一次进度。如果发现你没回复，它会主动在 Discord 里敲你：“同学走神了吗？”

## 🎭 自定义你的人设 (Persona)
作为一个开源底座，你可以在你的 OpenClaw Agent 设置中赋予它任何性格！
不论是“严肃教授”、“幽默温柔老师”还是“怼人很凶严师”，本引擎都会自动继承该人设的语气来执行上述讲课和抽查。

## 🤝 贡献指南
欢迎提交 Issue 和 Pull Request！特别是对于 `digest_txt.py` 的中文语义切分逻辑，期待大家一起把它优化得更聪明。

---
