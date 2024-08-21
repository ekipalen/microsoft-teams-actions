import requests
from sema4ai.actions import action, OAuth2Secret, Response, ActionError
from typing import Literal
from microsoft_teams.support import (
    BASE_GRAPH_URL,
    build_headers,
)
from microsoft_teams.models import UserSearch


@action
def get_joined_teams(
    token: OAuth2Secret[
        Literal["microsoft"],
        list[Literal["Team.ReadBasic.All"]],
    ],
) -> Response[dict]:
    """
    Get all Teams the user is joined to with the full details.

    Args:
        token: OAuth2 token to use for the operation.

    Returns:
        Result of the operation
    """
    headers = build_headers(token)
    response = requests.get(
        f"{BASE_GRAPH_URL}/me/joinedTeams",
        headers=headers,
    )
    if response.status_code in [200, 201]:
        return Response(result=response.json())
    else:
        raise ActionError(f"Failed to get joined teams: {response.text}")


@action
def get_team_members(
    token: OAuth2Secret[
        Literal["microsoft"],
        list[Literal["TeamMember.Read.All"]],
    ],
    team_id: str,
) -> Response[dict]:
    """
    Get the members of a specific Microsoft Team.

    Args:
        token: OAuth2 token to use for the operation.
        team_id: The ID of the Microsoft Team.

    Returns:
        Result of the operation
    """
    if not team_id:
        raise ActionError("The team_id must be provided")

    headers = build_headers(token)
    response = requests.get(
        f"{BASE_GRAPH_URL}/teams/{team_id}/members",
        headers=headers,
    )
    if response.status_code in [200, 201]:
        return Response(result=response.json())
    else:
        raise ActionError(f"Failed to get team members: {response.text}")


@action
def get_team_channels(
    token: OAuth2Secret[
        Literal["microsoft"],
        list[Literal["Channel.ReadBasic.All"]],
    ],
    team_id: str,
) -> Response[dict]:
    """
    Get the channels of a specific Microsoft Team.

    Args:
        token: OAuth2 token to use for the operation.
        team_id: The ID of the Microsoft Team.

    Returns:
        Result of the operation
    """
    if not team_id:
        raise ActionError("The team_id must be provided")

    headers = build_headers(token)
    response = requests.get(
        f"{BASE_GRAPH_URL}/teams/{team_id}/channels",
        headers=headers,
    )
    if response.status_code in [200, 201]:
        return Response(result=response.json())
    else:
        raise ActionError(f"Failed to get team channels: {response.text}")


@action
def search_user(
    user_search: UserSearch,
    token: OAuth2Secret[
        Literal["microsoft"],
        list[Literal["User.Read.All"]],
    ],
) -> Response[list]:
    """
    Search for a user by email, first name, or last name, and include the details
    of the user making the request to be used in Chat's.

    Args:
        user_search: The search criteria (email, first name, or last name).
        token: OAuth2 token to use for the operation.

    Returns:
        Result of the operation, including user details if found, and the details of the requesting user.
    """
    headers = build_headers(token)
    results = []

    me_response = requests.get(f"{BASE_GRAPH_URL}/me", headers=headers)
    if me_response.status_code in [200, 201]:
        my_details = me_response.json()
        results.append(my_details)
    else:
        raise ActionError(
            f"Failed to retrieve current user details: {me_response.text}"
        )

    if user_search.email:
        response = requests.get(
            f"{BASE_GRAPH_URL}/users/{user_search.email}",
            headers=headers,
        )
    else:
        search_query = []
        if user_search.first_name:
            search_query.append(f"startswith(givenName,'{user_search.first_name}')")
        if user_search.last_name:
            search_query.append(f"startswith(surname,'{user_search.last_name}')")

        filter_query = " and ".join(search_query)
        response = requests.get(
            f"{BASE_GRAPH_URL}/users?$filter={filter_query}",
            headers=headers,
        )

    if response.status_code in [200, 201]:
        search_results = response.json().get("value", [])
        results.extend(search_results)
        return Response(result=results)
    else:
        raise ActionError(f"Failed to search for user: {response.text}")
