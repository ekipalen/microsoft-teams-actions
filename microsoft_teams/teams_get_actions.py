import requests
from sema4ai.actions import action, OAuth2Secret, Response, ActionError
from typing import Literal
from microsoft_teams.support import (
    BASE_GRAPH_URL,
    build_headers,
)
from microsoft_teams.models import UserSearch, TeamSearchRequest


@action
def get_joined_teams(
    token: OAuth2Secret[
        Literal["microsoft"],
        list[Literal["Team.ReadBasic.All"]],
    ],
) -> Response[dict]:
    """
    Get all Teams the user is joined to with the full details. Can be used to search Teams as well.

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
def search_team_by_name(
    token: OAuth2Secret[
        Literal["microsoft"],
        list[Literal["Group.Read.All"]],
    ],
    search_request: TeamSearchRequest,
) -> Response[dict]:
    """
    Search for a Microsoft Team by its name.

    Args:
        token: OAuth2 token to use for the operation.
        search_request: Pydantic model containing the team name to search for.

    Returns:
        Result of the search operation, including details of matching teams.
    """
    headers = build_headers(token)
    team_name = search_request.team_name

    response = requests.get(
        f"{BASE_GRAPH_URL}/groups?$filter=displayName eq '{team_name}' and resourceProvisioningOptions/Any(x:x eq 'Team')",
        headers=headers,
    )

    if response.status_code in [200, 201]:
        teams = response.json().get("value", [])
        return Response(result=teams)
    else:
        raise ActionError(f"Failed to search for team: {response.text}")


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
) -> Response[dict]:
    """
    Search for a user by email, first name, or last name.

    Args:
        user_search: The search criteria (email, first name, or last name).
        token: OAuth2 token to use for the operation.

    Returns:
        Result of the operation with user details if found.
    """
    headers = build_headers(token)

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
        return Response(result=search_results)
    else:
        raise ActionError(f"Failed to search for user: {response.text}")
