明白啦 👍 我帮你写一个 **超级小白版的 README.md**，从零开始一步一步，每个命令都解释清楚，照着做就能跑起来、调用、再关闭服务。

---

# Game24 API 使用说明（小白版）

这是一个用 Python 写的 **24 点游戏求解 API**。你可以输入四个数字，它会告诉你能不能算出 24，以及给出解法。

---

## 1. 准备环境

1. **安装 Python 3.10 或更高版本**
   （在命令行里输入 `python --version` 检查）

2. **进入项目目录**（你解压/下载后的 `GAME24-api` 文件夹）
   Windows PowerShell 里：

   ```powershell
   cd D:\pycharm\GAME24-api
   ```

3. **创建虚拟环境（可选，但推荐）**

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   激活后，你会看到命令行前面多了一个 `(.venv)`。

4. **安装依赖**（只需要 requests 库，用于测试）

   ```powershell
   pip install -r requirements.txt
   ```

---

## 2. 启动 API 服务

在项目目录运行：

```powershell
python api.py
```

看到提示：

```
Game24 REST API listening on http://127.0.0.1:5000
```

说明服务启动成功。此时不要关闭这个窗口。

---

## 3. 调用 API

你可以用三种方式：

### 方式 A：浏览器

在浏览器地址栏输入：

```
http://127.0.0.1:5000/solve?nums=4,7,8,8
```

浏览器会返回一段 JSON，里面有所有的解。

### 方式 B：前端页面

双击打开项目里的 **`index.html`** 文件：

* 在输入框里输入 `4,7,8,8`，点击 **求解**，能看到解。
* 在下面输入框里写一个表达式，比如 `(8/(7-4))*8`，点击 **校验**，能看到 `{"valid": true}` 或 `false`。

### 方式 C：命令行（推荐）

在新的 PowerShell 窗口输入：

**获取解**

```powershell
Invoke-RestMethod "http://127.0.0.1:5000/solve?nums=4,7,8,8" | ConvertTo-Json -Depth 5
```

**校验表达式**

```powershell
Invoke-RestMethod `
  -Method Post `
  -Uri "http://127.0.0.1:5000/check" `
  -ContentType "application/json" `
  -Body '{"expr":"(8/(7-4))*8","nums":[4,7,8,8]}'
```

---

## 4. 关闭 API 服务

有两种方式：

### 如果服务在前台运行

直接在运行 `python api.py` 的那个窗口里按 **Ctrl + C**。

### 如果端口 5000 被占用，手动关闭进程

**Windows PowerShell**

```powershell
# 查看 5000 端口的进程
Get-NetTCPConnection -LocalPort 5000 | Select-Object OwningProcess

# 杀掉进程（替换 <PID> 为上面查到的数字）
Stop-Process -Id <PID> -Force
```

---

## 5. 运行测试（可选）

确保服务没启动，在项目目录里执行：

```powershell
python -m unittest discover -s tests -v
```

---

## 6. 常见问题

* **为什么看到 `GET /favicon.ico 404`？**
  正常现象，没图标，不影响使用。

* **为什么浏览器显示一堆大括号和引号？**
  这是 JSON 格式，正常的。

* **如何换端口？**

  ```powershell
  $env:GAME24_PORT="5050"
  python api.py
  ```

  然后用 `http://127.0.0.1:5050/...` 访问。

---

你要不要我直接帮你生成一个 `README.md` 文件，放到项目里？这样你在 PyCharm 里点开就能看说明，不用翻聊天记录。
