1.  All the files for the "cosine-similarity recommender system for books" is in this GitHub repository, EXCEPT for the actual Docker image (see below)
2.  This Docker image can be retrieved from "Docker Hub" via repository 'glennsbdean/glennrecsys-210706'
3.  If one should want to run their own container using the image: once the container is running, you should type in address 'http://localhost:5000/get_books'
4.  Using AWS/ECS/ECR, I have launched a container using the image - to access the recommender system, go to "3.101.130.204/get_books"