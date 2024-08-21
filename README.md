# Microsoft Teams

Action package for interaction with Microsoft Teams resources.

Currently capably of listing details from users Teams, listing members and channels of Team, searching for users, posting channel messages, creating new Teams, creating one on one chats and sending messages to those. 

## Prompt Examples

```
Create a new chat with Tommi, and send a message "Yo, greetings from my Teams Agent!"
```

>A new chat has been created with Tommi, and the message "Yo, greetings from my Teams Agent!" has been sent.

```
Create a Team "Agent Testing"
```

>The team "Agent Testing" has been created successfully. If you need any further assistance, feel free to ask!

```
Post "Hello" to that team's general channel
```

>The message "Hello" has been posted to the General channel of the "Agent Testing" team. If you need any further assistance, feel free to ask! 

## Authorization

In order to use the action package you need to go into https://portal.azure.com and register new Azure Entra ID (formerly Azure AD) application. Follow the detailed instructions [here](https://sema4.ai/docs/actions/auth/microsoft).

Grant the application necessary scopes to use actions.

    - Files.Read
    - Files.Read.All
    - Files.ReadWrite
    - Sites.Read.All
    - Sites.ReadWrite.All


