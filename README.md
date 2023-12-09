# Work Time Tracker API

### Environment variables:
```commandline
DATABASE_HOST="localhost" | "database" (depending if you're working on IDE run app 
                                        or docker built app)
ENVIRONMENT="PRODUCTION" | "STAGING" | "DEVELOPMENT"
```

### Docker:
1. If you want to run the database only, run `docker-compose up database`.
2. If you want to build the whole app, run `docker-compose build` then `docker-compose up` to make sure all changes are taken.

## !!! DEV NOTES:
### Dependencies:
1. Every new dependency that's added should be put into `requirements.txt` along with its last version