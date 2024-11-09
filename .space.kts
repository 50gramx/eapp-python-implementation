import java.time.LocalDate
import java.io.File // For working with file paths
import java.lang.ProcessBuilder // To execute commands

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

            // Fetch Commit Messages
            val workingDir = File("/mnt/space/work/eapp-python-implementation") // Specify your source code directory

            val process = ProcessBuilder("git", "-C", workingDir.absolutePath, "rev-parse", "HEAD")
                .redirectOutput(ProcessBuilder.Redirect.PIPE)
                .start()

            val output = process.inputStream.bufferedReader().readLine() ?: ""
            val commitHash = output.trim()

            println("Current commit hash: $commitHash")
        }

        requirements {
            workerTags("windows-pool")
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

        requirements {
            workerTags("windows-pool")
        }
    }

    host("Build Python Implementations Images") {
        // Before running the scripts, the host machine will log in to
        // the registries specified in connections.
        // dockerRegistryConnections {
            // specify connection key
            // +"khetana_docker_hub_private_registry"
            // multiple connections are supported
            // +"one_more_connection"
        // }

        shellScript {
            content = """
                docker login -u ethosindia -p dckr_pat_4S0EcsM5lO5Z1gxDT-q5NUkKf4U
            """
        }


        dockerBuildPush {
            file = "Dockerfile"

            // Add a cache-busting argument to force `apt-get update`
            extraArgsForBuildCommand = listOf("--build-arg", "CACHEBUST=${System.currentTimeMillis()}")

           // image tags
            val spaceRepo = "50gramx.registry.jetbrains.space/p/main/ethosindiacontainers/eapp-python-implementations"
            val dockerHubRepo = "docker.io/ethosindia/eapp-python-implementations"
            tags {
                // use current job run number as a tag - '0.0.run_number'
                +"$dockerHubRepo:{{ VERSION_NUMBER }}"
                +"$dockerHubRepo:latest"
            }
        }

        requirements {
            workerTags("windows-pool")
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

        requirements {
            workerTags("windows-pool")
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

        requirements {
            workerTags("windows-pool")
            workerTags("amitkumarkhetan15-user")
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

        requirements {
            workerTags("windows-pool")
            workerTags("amitkumarkhetan15-user")
        }
    }

    container("Finish Deployment", image = "amazoncorretto:17-alpine") {

        kotlinScript { api ->
            api.space().projects.automation.deployments.finish(
                project = api.projectIdentifier(),
                targetIdentifier = TargetIdentifier.Key("python-implementation-deployment"),
                version = api.parameters["VERSION_NUMBER"],
            )
        }

        requirements {
            workerTags("windows-pool")
        }
    }

}


job("Build Cache Invalidated Python Implementations Image") {

    startOn {
        gitPush {
            enabled = false
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

            // Fetch Commit Messages
            val workingDir = File("/mnt/space/work/eapp-python-implementation") // Specify your source code directory

            val process = ProcessBuilder("git", "-C", workingDir.absolutePath, "rev-parse", "HEAD")
                .redirectOutput(ProcessBuilder.Redirect.PIPE)
                .start()

            val output = process.inputStream.bufferedReader().readLine() ?: ""
            val commitHash = output.trim()

            println("Current commit hash: $commitHash")
        }

        requirements {
            workerTags("windows-pool")
        }
    }

    host("Build Python Implementations Images") {
        // Before running the scripts, the host machine will log in to
        // the registries specified in connections.
        // dockerRegistryConnections {
            // specify connection key
            // +"khetana_docker_hub_private_registry"
            // multiple connections are supported
            // +"one_more_connection"
        // }

        shellScript {
            content = """
                docker login -u ethosindia -p dckr_pat_4S0EcsM5lO5Z1gxDT-q5NUkKf4U
            """
        }


        dockerBuildPush {
            file = "Dockerfile"
            // image tags
            val spaceRepo = "50gramx.registry.jetbrains.space/p/main/ethosindiacontainers/eapp-python-implementations"
            val dockerHubRepo = "docker.io/ethosindia/eapp-python-implementations"


            // Add a cache-busting argument to force `apt-get update`
            extraArgsForBuildCommand = listOf("--build-arg", "CACHEBUST=${System.currentTimeMillis()}")

            tags {
                // use current job run number as a tag - '0.0.run_number'
                +"$dockerHubRepo:{{ VERSION_NUMBER }}"
                +"$dockerHubRepo:latest"
            }
        }

        requirements {
            workerTags("windows-pool")
        }
    }
}

job("Deploy Python Implementations") {

    startOn {
        gitPush {
            enabled = false
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

            // Fetch Commit Messages
            val workingDir = File("/mnt/space/work/eapp-python-implementation") // Specify your source code directory

            val process = ProcessBuilder("git", "-C", workingDir.absolutePath, "rev-parse", "HEAD")
                .redirectOutput(ProcessBuilder.Redirect.PIPE)
                .start()

            val output = process.inputStream.bufferedReader().readLine() ?: ""
            val commitHash = output.trim()

            println("Current commit hash: $commitHash")
        }

        requirements {
            workerTags("windows-pool")
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

        requirements {
            workerTags("windows-pool")
            workerTags("amitkumarkhetan15-user")
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

        requirements {
            workerTags("windows-pool")
            workerTags("amitkumarkhetan15-user")
        }
    }
}

job("Build Capabilities Proxy Image") {
    startOn {
        gitPush {
            pathFilter {
                +"Dockerfile.proxy"
                +"envoy.yaml"
            }
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

        requirements {
            workerTags("windows-pool")
        }
    }

    host("Build and push capabilities proxy image") {
        
        shellScript {
            content = """
                docker login -u ethosindia -p dckr_pat_4S0EcsM5lO5Z1gxDT-q5NUkKf4U
            """
        }

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
            val dockerHubRepo = "docker.io/ethosindia/eapp-capabilities-proxy"
            tags {
                // use current job run number as a tag - '0.0.run_number'
                +"$dockerHubRepo:{{ VERSION_NUMBER }}"
                +"$dockerHubRepo:latest"
            }
        }

        requirements {
            workerTags("windows-pool")
        }
    }
}

job("Build Capabilities Proxy kubernetes Image") {
    startOn {
        gitPush {
            pathFilter {
                +"Dockerfile-kubernetes.proxy"
                +"envoy-kubernetes.yaml"
            }
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

        requirements {
            workerTags("windows-pool")
        }
    }

    host("Build and push capabilities proxy image") {
        
        shellScript {
            content = """
                docker login -u ethosindia -p dckr_pat_4S0EcsM5lO5Z1gxDT-q5NUkKf4U
            """
        }

        dockerBuildPush {
            // by default, the step runs not only 'docker build' but also 'docker push'
            // to disable pushing, add the following line:
            // push = false

            // path to Docker context (by default, context is working dir)
            // context = "docker"
            // path to Dockerfile relative to the project root
            // if 'file' is not specified, Docker will look for it in 'context'/Dockerfile
            file = "Dockerfile-kubernetes.proxy"
            // build-time variables
            // args["HTTP_PROXY"] = "http://10.20.30.2:1234"
            // image labels
            // labels["vendor"] = "mycompany"
            // to add a raw list of additional build arguments, use
            // extraArgsForBuildCommand = listOf("...")
            // to add a raw list of additional push arguments, use
            // extraArgsForPushCommand = listOf("...")
            // image tags
            val dockerHubRepo = "docker.io/ethosindia/eapp-capabilities-proxy-kubernetes"
            tags {
                // use current job run number as a tag - '0.0.run_number'
                +"$dockerHubRepo:{{ VERSION_NUMBER }}"
                +"$dockerHubRepo:latest"
            }
        }

        requirements {
            workerTags("windows-pool")
        }
    }
}

job("Build Nginx Upstream Image") {
    startOn {
        gitPush {
            pathFilter {
                +"Dockerfile.nginx"
                +"nginx.conf"
            }
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

        requirements {
            workerTags("windows-pool")
        }
    }

    host("Build and push nginx upstream image") {


        shellScript {
            content = """
                docker login -u ethosindia -p dckr_pat_4S0EcsM5lO5Z1gxDT-q5NUkKf4U
            """
        }

        
        dockerBuildPush {
            
            file = "Dockerfile.nginx"
            val dockerHubRepo = "docker.io/ethosindia/eapp-capabilities-upstream"
            tags {
                +"$dockerHubRepo:{{ VERSION_NUMBER }}"
                +"$dockerHubRepo:latest"
            }
        }

        requirements {
            workerTags("windows-pool")
        }
    }
}


job("Run EthosPods First Worker") {
    startOn {
        gitPush { enabled = false }
    }

    host(displayName = "Docker List Containers") {
        shellScript {
            content = """
                docker ps
            """
        }

        requirements {
            workerTags("windows-pool")
            workerTags("kunalhindocha20-user")
        }
    }
}