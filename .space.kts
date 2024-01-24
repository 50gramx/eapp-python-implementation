import java.time.LocalDate

job("Build & Deploy Python Implementations") {

    startOn {
        gitPush {
            anyBranchMatching {
                +"release-*"
                +"master"
                +"main"
            }
        }
    }

   // To check a condition, basically, you need a kotlinScript step
    host(displayName = "Setup Version") {
        kotlinScript { api ->
            // Get the current year and month
            val currentYear = (LocalDate.now().year % 100).toString().padStart(2, '0')
            val currentMonth = LocalDate.now().monthValue.toString()

            // Get the execution number from environment variables
            val currentExecution = System.getenv("JB_SPACE_EXECUTION_NUMBER")

            // Set the VERSION_NUMBER parameter
            api.parameters["VERSION_NUMBER"] = "$currentYear.$currentMonth.$currentExecution"
        }
    }

    container("Schedule Deployment", image = "amazoncorretto:17-alpine") {
        kotlinScript { api ->
            api.space().projects.automation.deployments.schedule(
                project = api.projectIdentifier(),
                targetIdentifier = TargetIdentifier.Key("python-implementation-deployment"),
                version = api.parameters["VERSION_NUMBER"],
            )
        }
    }

    host("Build Python Implementations Images") {
        dockerBuildPush {
            // by default, the step runs not only 'docker build' but also 'docker push'
            // to disable pushing, add the following line:
            // push = false

            // path to Docker context (by default, context is working dir)
            // context = "docker"
            // path to Dockerfile relative to the project root
            // if 'file' is not specified, Docker will look for it in 'context'/Dockerfile
            file = "Dockerfile"
            // build-time variables
            // args["HTTP_PROXY"] = "http://10.20.30.2:1234"
            // image labels
            // labels["vendor"] = "mycompany"
            // to add a raw list of additional build arguments, use
            // extraArgsForBuildCommand = listOf("...")
            // to add a raw list of additional push arguments, use
            // extraArgsForPushCommand = listOf("...")
            // image tags
            tags {
                // use current job run number as a tag - '0.0.run_number'
                +"50gramx.registry.jetbrains.space/p/main/ethosindiacontainers/eapp-python-implementations:{{ VERSION_NUMBER }}"
                +"50gramx.registry.jetbrains.space/p/main/ethosindiacontainers/eapp-python-implementations:latest"
            }
        }
    }

    container("Start Deployment", image = "amazoncorretto:17-alpine") {
        kotlinScript { api ->
            api.space().projects.automation.deployments.start(
                project = api.projectIdentifier(),
                targetIdentifier = TargetIdentifier.Key("python-implementation-deployment"),
                version = api.parameters["VERSION_NUMBER"],
                // automatically update deployment status based on a status of a job
                syncWithAutomationJob = true
            )
        }
    }

    host("Trigger Python Implementations Backups") {

      shellScript {
        content = """
            # Trigger backups before bringing down the services

            export CONTAINER_NAME='eapp-python-implementation-postgres-1'
            export CID=$(docker ps -q -f status=running -f name=^/${"$"}CONTAINER_NAME$)
            if [ ! "${"$"}CID" ]; then
                echo "PostgreSQL container is not running. Skipping backup."
            else
                echo "PostgreSQL container is running. Backing up..."
                docker-compose exec postgres /bin/sh -c "sh /psql_backup.sh instant"
            fi
            unset CID

            export CONTAINER_NAME='eapp-python-implementation-redis-1'
            export CID=$(docker ps -q -f status=running -f name=^/${"$"}CONTAINER_NAME$)
            if [ ! "${"$"}CID" ]; then
                echo "Redis container is not running. Skipping backup."
            else
                echo "Redis container is running. Backing up..."
                docker-compose exec redis /bin/sh -c "sh /redis_backup.sh instant"
            fi
            unset CID
        """
      }
    }

    host("Deploy Python Implementations Containers") {

      shellScript {
        content = """
            # Bring down the services
            docker-compose down --remove-orphans

            # Bring up the services
            docker-compose up -d
        """
      }
    }

    container("Finish Deployment", image = "amazoncorretto:17-alpine") {
        kotlinScript { api ->
            api.space().projects.automation.deployments.finish(
                project = api.projectIdentifier(),
                targetIdentifier = TargetIdentifier.Key("python-implementation-deployment"),
                version = api.parameters["VERSION_NUMBER"],
            )
            // to fail the deployment, use ...deployments.fail()
        }
    }
    
    // run this job only on
    // a Windows worker
    // that is tagged as 'pool-1'
    requirements {
        workerTags("windows-pool")
    }
}

job("Build Capabilities Proxy Image") {
    startOn {
        gitPush {
            pathFilter {
                +"Dockerfile.proxy"
            }
        }
    }

    // To check a condition, basically, you need a kotlinScript step
    host(displayName = "Setup Version") {
        kotlinScript { api ->
            // Get the current year and month
            val currentYear = (LocalDate.now().year % 100).toString().padStart(2, '0')
            val currentMonth = LocalDate.now().monthValue.toString()

            // Get the execution number from environment variables
            val currentExecution = System.getenv("JB_SPACE_EXECUTION_NUMBER")

            // Set the VERSION_NUMBER parameter
            api.parameters["VERSION_NUMBER"] = "$currentYear.$currentMonth.$currentExecution"
        }

        requirements {
            workerTags("windows-pool")
        }
    }

    host("Build and push capabilities proxy image") {
        dockerBuildPush {
            // by default, the step runs not only 'docker build' but also 'docker push'
            // to disable pushing, add the following line:
            // push = false

            // path to Docker context (by default, context is working dir)
            // context = "docker"
            // path to Dockerfile relative to the project root
            // if 'file' is not specified, Docker will look for it in 'context'/Dockerfile
            file = "Dockerfile.proxy"
            // build-time variables
            // args["HTTP_PROXY"] = "http://10.20.30.2:1234"
            // image labels
            // labels["vendor"] = "mycompany"
            // to add a raw list of additional build arguments, use
            // extraArgsForBuildCommand = listOf("...")
            // to add a raw list of additional push arguments, use
            // extraArgsForPushCommand = listOf("...")
            // image tags
            tags {
                // use current job run number as a tag - '0.0.run_number'
                +"50gramx.registry.jetbrains.space/p/main/ethosindiacontainers/capabilities-proxy:{{ VERSION_NUMBER }}"
                +"50gramx.registry.jetbrains.space/p/main/ethosindiacontainers/capabilities-proxy:latest"
            }
        }

        requirements {
            workerTags("windows-pool")
        }
    }
}