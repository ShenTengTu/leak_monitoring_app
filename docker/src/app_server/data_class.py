from typing import ClassVar, List, Tuple, Any
from dataclasses import dataclass, asdict


@dataclass
class DC_EMQXWebHookBody:
    """Base Data Class of EMQX Web Hook request body."""

    _hide_fields: ClassVar[Tuple[str]] = (
        "node",
        "action",
        "ipaddress",
        "keepalive",
        "proto_ver",
    )
    node: str
    action: str

    @classmethod
    def _dict_factory(cls, mapping: List[Tuple[str, Any]]):
        d = {}
        for k, v in mapping:
            if k not in cls._hide_fields:
                d[k] = v
        return d

    def as_dict(self):
        return asdict(self, dict_factory=self._dict_factory)


class DCSet_EMQXWebHookBody:
    """Data Class set of EMQX Web Hook request body.

    Each attribute are Data Class.
    - client_connected
    - client_disconnected
    - message_publish
    """

    @dataclass
    class client_connected(DC_EMQXWebHookBody):
        clientid: str
        username: str
        ipaddress: str
        keepalive: int
        proto_ver: int
        connected_at: int

    @dataclass
    class client_disconnected(DC_EMQXWebHookBody):
        clientid: str
        username: str
        reason: str
        disconnected_at: int

    @dataclass
    class message_publish(DC_EMQXWebHookBody):
        from_client_id: str
        from_username: str
        topic: str
        qos: int
        retain: bool
        payload: str
        ts: int
