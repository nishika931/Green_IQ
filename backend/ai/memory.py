from collections import defaultdict


conversation_memory = defaultdict(list)


def add_message(user_id: int, role: str, message: str):
    conversation_memory[user_id].append({
        "role": role,
        "message": message
    })


def get_recent_memory(user_id: int, limit: int = 4):
    messages = conversation_memory[user_id]

    return messages[-limit:]


def get_memory_text(user_id: int, limit: int = 4):
    messages = get_recent_memory(user_id, limit)

    if not messages:
        return ""

    return "\n".join(
        f"{message['role']}: {message['message']}"
        for message in messages
    )


def clear_memory(user_id: int):
    conversation_memory[user_id] = []