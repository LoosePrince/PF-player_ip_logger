![PF-player_ip_logger](https://socialify.git.ci/LoosePrince/PF-player_ip_logger/image?description=1&font=Inter&language=1&name=1&pattern=Floating%20Cogs&theme=Light)
# Player IP Logger for MCDReforged

#### 插件简介
**Player IP Logger** 是一款为 MCDReforged (MCDR) 开发的插件，主要功能是记录玩家的 IP 地址。该插件能够追踪玩家的登录和断线信息，并将玩家对应的 IP 地址保存在配置文件中。你可以随时通过插件 API 查询玩家的 IP 地址历史，方便进行服务器管理和审查。

#### 功能
- **自动记录玩家 IP**: 通过监控玩家的登录和断线事件，自动捕获并记录 IP 地址。
- **IP 地址存储**: 保存玩家的所有历史 IP 地址，避免重复记录。
- **支持 API 查询**: 插件提供了简单的 API 以便其他插件调用，例如检查玩家是否存在记录以及获取玩家的 IP 地址列表。

#### 安装与配置
1. **安装**: 将插件放入 MCDReforged 插件目录中。
2. **配置**: 插件会在首次运行时生成一个 `config.json` 文件，包含用户的 IP 记录。该文件格式如下：
    ```json
    {
        "users": {
            "玩家名称": [
                "玩家的IP1",
                "玩家的IP2"
            ]
        }
    }
    ```

#### 事件处理
- 当玩家登录或断开连接时，插件会自动解析相关日志信息，并提取玩家名称和 IP 地址。
- 如果玩家的 IP 地址尚未记录，将其添加到配置文件中，并自动保存。

#### 支持的事件格式
该插件支持以下日志格式的解析：
- `玩家名[/IP地址:端口] logged in with entity id`
- `Disconnecting 玩家名 (/IP地址:端口)`
- `玩家名 (/IP地址:端口) lost connection`

#### 使用
插件会自动运行并监控日志，不需要任何配置。

---

### API 开发

1. **is_player(name: str) -> bool**
   - **描述**: 检查某个玩家是否存在于 IP 记录中。
   - **参数**: 
     - `name`：玩家名称。
   - **返回**: 如果玩家存在记录返回 `True`，否则返回 `False`。

   **示例**:
   ```python
   if is_player("Shusao"):
       print("Shusao 的 IP 已被记录。")
   ```

2. **get_player_ips(name: str) -> list**
   - **描述**: 获取指定玩家的所有 IP 地址。
   - **参数**: 
     - `name`：玩家名称。
   - **返回**: 包含玩家所有历史 IP 地址的列表。如果玩家没有记录，返回空列表。

   **示例**:
   ```python
   ips = get_player_ips("Shusao")
   print(f"Shusao 的 IP 历史: {ips}")
   ```
### 使用此API的插件
- [PF-GUGUbot](https://github.com/LoosePrince/PF-GUGUBot) : MCDR-GUGUBot QQ机器人 群聊管理 聊天互转
>  用于区分真实玩家

---

### 贡献
欢迎提交问题或贡献代码！

- 插件初版：树梢（[LoosePrince](https://github.com/LoosePrince)）、[ChatGPT](https://chatgpt.com/)
- 技术支持：雪开（[XueK66](https://github.com/XueK66)）
- 文档编辑：树梢（[LoosePrince](https://github.com/LoosePrince)）、[ChatGPT](https://chatgpt.com/)

---

#### 未来计划
- 暂无

欢迎提建议！
