# Game24 API 使用说明（小白版）

这是一个用 Python 写的 24 点游戏求解 API。  
你输入四个数字，它会告诉你能不能算出 24，并给出解法；  
也能检查你写的表达式是否正确。  

---

## 1. 准备环境

1. 安装 **Python 3.10 或更高版本**  
   在命令行输入：
   ```powershell
   python --version
   ```

2. 进入项目目录（例如你下载/解压后的文件夹）：  
   ```powershell
   cd D:\pycharm\game24-api
   ```

3. （可选）创建虚拟环境，避免污染系统环境：  
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
   激活后命令行前面会多一个 `(.venv)`。

4. 安装依赖：  
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
说明服务已启动成功。  
此时不要关闭这个窗口。

---

## 3. 调用 API

API 现在只支持 **POST** 请求。  
你可以通过 **前端页面** 或 **命令行** 来使用。

### 方式 A：前端页面（最简单）
- 双击打开项目里的 `index.html`
- 输入四个数字（例如 `4,7,8,8`），点击【求解】，会显示所有解法
- 在下面输入表达式（例如 `(8/(7-4))*8`），点击【校验】，会显示 `{"valid": true}`

### 方式 B：命令行（PowerShell 推荐）

**求解**
```powershell
Invoke-RestMethod -Method Post `
  -Uri "http://127.0.0.1:5000/solve" `
  -ContentType "application/json" `
  -Body '{"nums":[4,7,8,8]}' | ConvertTo-Json -Depth 5
```

**校验**
```powershell
Invoke-RestMethod -Method Post `
  -Uri "http://127.0.0.1:5000/check" `
  -ContentType "application/json" `
  -Body '{"expr":"(8/(7-4))*8","nums":[4,7,8,8]}'
```

### 方式 C：curl（Linux/macOS 常用）
```bash
# 求解
curl -X POST http://127.0.0.1:5000/solve \
  -H "Content-Type: application/json" \
  -d '{"nums":[4,7,8,8]}'

# 校验
curl -X POST http://127.0.0.1:5000/check \
  -H "Content-Type: application/json" \
  -d '{"expr":"(8/(7-4))*8","nums":[4,7,8,8]}'
```

---

## 4. 关闭 API 服务

- 如果服务在前台运行：在运行 `python api.py` 的窗口按 **Ctrl + C**。  
- 如果端口被占用，可以手动关闭进程：
  ```powershell
  # 查看 5000 端口的进程
  Get-NetTCPConnection -LocalPort 5000 | Select-Object OwningProcess

  # 杀掉进程（替换 <PID> 为上面查到的数字）
  Stop-Process -Id <PID> -Force
  ```

---

## 5. 常见问题

- **为什么浏览器直接访问 `/solve` 提示 405？**  
  因为现在只支持 **POST**，请用前端页面或命令行调用。

- **为什么浏览器显示一堆大括号和引号？**  
  这是 JSON 格式，正常的。

- **如何换端口？**  
  ```powershell
  $env:GAME24_PORT="5050"
  python api.py
  ```
  然后用 `http://127.0.0.1:5050/...` 来访问。

---

## 6. 测试（可选）

如果你写了测试代码，可以在项目目录运行：
```powershell
pytest
```
或
```powershell
python -m unittest discover -s tests -v
```

---

## 许可证
MIT License
