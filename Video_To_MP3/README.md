This is a project to create a microservices based architecture to convert user provided Video files to Mp3 and send notifications back to User once completed.
It uses a combination of a gateway, rabbitMQ, Docker, Kubernetes, K9s/MiniKube, MongoDB, JWTs and Python as the glue between them.

I created this while watching a similar project on FreeCodeCamp ( So all thanks to them )

User input Vide Files --> gateway --> MySQL DB for Authentication --> JWT tokens for user --> On authentication store Video(s) to MongoDB --> Send notification through rabbitMQ to convert it to MP3 --> Once completed send notificationa nd file ID back to user

Contact Info : Feel free to contact me to discuss any issues, questions, or comments. My contact info can be found on my GitHub page.

License : I am providing code and resources in this repository to you under an open source license. Because this is my personal repository, the license you receive to my code and resources is from me and not my employer (Morgan Stanley Asia Bank Ltd).

Copyright : Copyright 2022 Kaushik Banerjee

Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)

https://creativecommons.org/licenses/by-sa/4.0/