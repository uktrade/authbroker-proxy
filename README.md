
# ABC proxy (initial POC) 

### Notes 

The proxy requires nginx compiled with support for the auth_request directive. This is available in the official nginx docker image.

The access token should not be exposed beyond the proxy as we use the authorization code grant type, which is for machine-machine access.

For every request made to the application, nginx first hits the auth_request url. If a 401 response is received, it redirects the user to the ABC login page.

### Set-up

You can run a local environment using docker-compose

`cd proxy; cp env.template .env`

Put the OAuth2 client id, secret and url into the .env file.

Run `docker-compose up`

navigate to `https://localhost` which should present you with the auth broker login screen

Ensure that the correct redirect uri is whitelisted for your OAuth2 application, e.g `https://localhost/auth/response`
