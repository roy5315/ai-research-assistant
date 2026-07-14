from collections import defaultdict


_chat_history = defaultdict(list)


def get_chat_history(session_id: str) -> list[dict]:
    return _chat_history[session_id]


def add_message(
    session_id: str,
    role: str,
    content: str,
) -> None:
    _chat_history[session_id].append(
        {
            "role": role,
            "content": content,
        }
    )


def clear_chat_history(session_id: str) -> None:
    _chat_history.pop(session_id, None)