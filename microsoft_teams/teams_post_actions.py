import requests
from sema4ai.actions import action, OAuth2Secret, Response, ActionError
from typing import Literal
from microsoft_teams.models import TeamDetails
from microsoft_teams.support import (
    BASE_GRAPH_URL,
    build_headers,
)


@action
def post_channel_message(
    token: OAuth2Secret[
        Literal["microsoft"],
        list[Literal["ChannelMessage.Send"]],
    ],
    team_id: str,
    channel_id: str,
    message: str,
) -> Response[dict]:
    """
    Post a message to a specific channel in a Microsoft Team. Always confirm by telling the Team name where the post is about to go.

    Args:
        token: OAuth2 token to use for the operation.
        team_id: The ID of the Microsoft Team.
        channel_id: The ID of the channel within the team.
        message: The message to post.

    Returns:
        Result of the operation
    """
    if not team_id or not channel_id or not message:
        raise ActionError("The team_id, channel_id, and message must be provided")

    headers = build_headers(token)
    payload = {"body": {"content": message}}
    response = requests.post(
        f"{BASE_GRAPH_URL}/teams/{team_id}/channels/{channel_id}/messages",
        headers=headers,
        json=payload,
    )
    if response.status_code in [200, 201]:
        return Response(result=response.json())
    else:
        raise ActionError(f"Failed to post channel message: {response.text}")


@action
def create_team(
    team_details: TeamDetails,
    token: OAuth2Secret[
        Literal["microsoft"],
        list[Literal["Team.Create"]],
    ],
) -> Response[dict]:
    """
    Create a new Microsoft Team using the standard template.

    Args:
        team_details: Details of the team to be created.
        token: OAuth2 token to use for the operation.

    Returns:
        Result of the operation. If no ID get
    """
    headers = build_headers(token)

    data = {
        "template@odata.bind": "https://graph.microsoft.com/v1.0/teamsTemplates('standard')",
        "displayName": team_details.display_name,
        "description": team_details.description,
        "visibility": team_details.visibility,
    }

    response = requests.post(f"{BASE_GRAPH_URL}/teams", headers=headers, json=data)

    if response.status_code in [200, 201, 202]:
        try:
            result = response.json()
            if result == {}:
                return Response(
                    result={
                        "message": "Team created successfully, no additional details provided."
                    }
                )
            return Response(result=result)
        except ValueError:
            return Response(
                result={
                    "message": "Team created successfully, but no JSON response returned."
                }
            )
    else:
        error_details = response.text
        raise ActionError(f"Failed to create team: {error_details}")


@action
def create_chat(
    user_id_1: str,
    user_id_2: str,
    token: OAuth2Secret[
        Literal["microsoft"],
        list[Literal["Chat.Create"]],
    ],
) -> Response[dict]:
    """
    Create a new one-on-one chat between two users.

    Args:
        user_id_1: The ID of the first user asking for it.
        user_id_2: The ID of the second user.
        token: OAuth2 token to use for the operation.

    Returns:
        Result of the operation, including chat details if successful.
    """
    headers = build_headers(token)

    members = [
        {
            "@odata.type": "#microsoft.graph.aadUserConversationMember",
            "roles": ["owner"],
            "user@odata.bind": f"https://graph.microsoft.com/v1.0/users('{user_id_1}')",
        },
        {
            "@odata.type": "#microsoft.graph.aadUserConversationMember",
            "roles": ["owner"],
            "user@odata.bind": f"https://graph.microsoft.com/v1.0/users('{user_id_2}')",
        },
    ]

    data = {"chatType": "oneOnOne", "members": members}

    response = requests.post(f"{BASE_GRAPH_URL}/chats", headers=headers, json=data)

    if response.status_code in [200, 201]:
        return Response(result=response.json())
    else:
        raise ActionError(f"Failed to create chat: {response.text}")


@action
def send_message_to_chat(
    chat_id: str,
    message: str,
    token: OAuth2Secret[
        Literal["microsoft"],
        list[Literal["ChatMessage.Send"]],
    ],
) -> Response[dict]:
    """
    Send a message to a specific chat which needs to be created first.

    Args:
        chat_id: The ID of the chat to send the message to.
        message: The message content to send.
        token: OAuth2 token to use for the operation.

    Returns:
        Result of the operation, including message details if successful.
    """
    headers = build_headers(token)

    data = {"body": {"content": message}}

    response = requests.post(
        f"{BASE_GRAPH_URL}/chats/{chat_id}/messages", headers=headers, json=data
    )

    if response.status_code in [200, 201]:
        return Response(result=response.json())
    else:
        raise ActionError(f"Failed to send chat message: {response.text}")
