# Password Example

This is a very basic example to deploy microservices. It consists of 4
services:
* A frontend asking for a password and showing the results from the other
  services (`server`)
* A password-checker that calculates the password strengths (`password-checker`)
* A service that checks against a list of known passwords (`known-passwords`)
* A service that uses a redis backend to check if the given password is in
  the last 10 checked passwords (`password-dedup`).



## Easy testing:
The setup can be tested without K8s using `docker-compose up --build` from the main directory.
