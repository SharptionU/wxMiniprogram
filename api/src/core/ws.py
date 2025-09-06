from typing import Dict, List, Set, Optional, Callable, Awaitable
from fastapi import WebSocket, WebSocketDisconnect
import asyncio
from uuid import UUID, uuid4

# 连接标识：用 UUID 区分每个连接
ConnectionID = UUID

class WebSocketConnection:
    """单个 WebSocket 连接的封装"""
    def __init__(self, websocket: WebSocket, user_id: Optional[int] = None):
        self.websocket = websocket  # FastAPI WebSocket 对象
        self.connection_id = uuid4()  # 唯一连接 ID
        self.user_id = user_id  # 关联用户 ID（可选，用于认证后绑定）
        self.connected_at = asyncio.get_event_loop().time()  # 连接时间

class WebSocketManager:
    """WebSocket 连接管理器：处理连接生命周期和消息分发"""
    def __init__(self):
        # 存储所有活跃连接：connection_id -> WebSocketConnection
        self.active_connections: Dict[ConnectionID, WebSocketConnection] = {}
        # 按用户分组：user_id -> 该用户的所有连接 ID
        self.user_connections: Dict[int, Set[ConnectionID]] = {}
        # 按房间/频道分组：room_name -> 该房间的所有连接 ID
        self.room_connections: Dict[str, Set[ConnectionID]] = {}

    async def connect(self, websocket: WebSocket, user_id: Optional[int] = None) -> WebSocketConnection:
        """建立新连接并存储"""
        await websocket.accept()  # 接受 WS 连接
        connection = WebSocketConnection(websocket, user_id)
        self.active_connections[connection.connection_id] = connection

        # 若绑定用户，添加到用户分组
        if user_id:
            if user_id not in self.user_connections:
                self.user_connections[user_id] = set()
            self.user_connections[user_id].add(connection.connection_id)
        return connection

    def disconnect(self, connection_id: ConnectionID):
        """移除连接（连接关闭时调用）"""
        connection = self.active_connections.pop(connection_id, None)
        if not connection:
            return

        # 从用户分组中移除
        if connection.user_id and connection.user_id in self.user_connections:
            self.user_connections[connection.user_id].discard(connection_id)
            # 清理空用户分组
            if not self.user_connections[connection.user_id]:
                del self.user_connections[connection.user_id]

        # 从所有房间中移除（简化示例，实际需遍历房间）
        for room_name in list(self.room_connections.keys()):
            self.room_connections[room_name].discard(connection_id)
            if not self.room_connections[room_name]:
                del self.room_connections[room_name]

    async def send_personal_message(self, connection_id: ConnectionID, message: dict):
        """向单个连接发送消息"""
        connection = self.active_connections.get(connection_id)
        if connection:
            await connection.websocket.send_json(message)

    async def broadcast_to_user(self, user_id: int, message: dict):
        """向用户的所有连接广播消息"""
        if user_id not in self.user_connections:
            return
        # 复制连接 ID 集合，避免迭代中修改
        connection_ids = list(self.user_connections[user_id])
        for conn_id in connection_ids:
            await self.send_personal_message(conn_id, message)

    async def join_room(self, connection_id: ConnectionID, room_name: str):
        """将连接加入房间"""
        if connection_id not in self.active_connections:
            return
        if room_name not in self.room_connections:
            self.room_connections[room_name] = set()
        self.room_connections[room_name].add(connection_id)

    async def broadcast_to_room(self, room_name: str, message: dict, exclude: Optional[ConnectionID] = None):
        """向房间内所有连接广播消息（可选排除发送者）"""
        if room_name not in self.room_connections:
            return
        for conn_id in self.room_connections[room_name]:
            if conn_id != exclude:  # 排除发送者
                await self.send_personal_message(conn_id, message)

    async def close_connection(self, connection_id: ConnectionID, code: int = 1000, reason: str = "正常关闭"):
        """主动关闭连接"""
        connection = self.active_connections.get(connection_id)
        if connection:
            await connection.websocket.close(code=code, reason=reason)
            self.disconnect(connection_id)

# 全局 WS 管理器实例（单例）
ws_manager = WebSocketManager()
