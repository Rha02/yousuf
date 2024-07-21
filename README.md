# YouSuf - Your Personalized Voice Assistant
YouSuf is a chatbot project I and my team are building for our senior design project.

## API Doc
#### Login
`POST`: `/login`<br>
`cUrl`:
```sh
curl --location 'https://yousuf195.azurewebsites.net/login' \
--form 'email="<enter email>"' \
--form 'password="<enter password>"'
```
On successful login, response has the authentication token in `Authorization` header.

#### Register
`POST`: `/register`<br>
```sh
curl --location 'https://yousuf195.azurewebsites.net/register' \
--form 'first_name="<enter first name>"' \
--form 'last_name="<enter last name>"' \
--form 'email="<enter email>"' \
--form 'password="<enter password>"'
```
On successful register, response has the authentication token in `Authorization` header.

#### Get User
`GET`: `/user`
```sh
curl --location 'https://yousuf195.azurewebsites.net/user' \
--header 'Authorization: Bearer <token>'
```

#### Get Chats
Get a list of user's chats. This returns only chat meta-data and not the actual conversation history.<br>
`GET`: `/chats`
```sh
curl --location 'https://yousuf195.azurewebsites.net/chats' \
--header 'Authorization: Bearer <token>'
```

#### Create Chat
Create a new chat.<br>
`POST`: `/chats`
```sh
curl --location 'https://yousuf195.azurewebsites.net/chats' \
--header 'Authorization: Bearer <token>' \
--form 'title="<chat title>"'
```

#### Get Messages
Get a list of messages from the chat. Use this route to fetch conversation history<br>
`GET`: `/chats/<chat_id>`
```sh
curl --location 'https://yousuf195.azurewebsites.net/chats/6685e575b659017d1370b735?limit=16&offset=0' \
--header 'Authorization: Bearer <token>'
```

### Send Prompt
`POST`: `/chats/<chat_id>/message`
```sh
curl --location 'https://yousuf195.azurewebsites.net/chats/6685e575b659017d1370b735/message' \
--header 'Authorization: Bearer <token>' \
--form 'prompt="<enter prompt>"'
```