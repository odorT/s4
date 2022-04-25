## NOTES
- You should generate key.json from gcloud with full permissions to Cloud SQL and paste it into S4 Source Code folder

- Build with in source directory:  
    `docker build -t <image:tag>--build-arg DB_HOST=<db-host> --build-arg DB_PASS=<db-pass> .`